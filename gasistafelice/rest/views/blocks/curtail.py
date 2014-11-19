from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.db import transaction

from rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF

from lib.shortcuts import render_to_xml_response, render_to_context_response

from gf.gas.models import GASMember, GASMemberOrder
from gf.supplier.models import Supplier
from gf.gas.forms.cash import EcoGASMemberForm, NewEcoGASMemberForm
from lib.formsets import BaseFormSetWithRequest
from django.forms.formsets import formset_factory

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import cgi, os
from django.conf import settings

from consts import CASH, VIEW, EDIT_MULTIPLE
from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "curtail"
    BLOCK_DESCRIPTION = _("Curtail gasmember")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'ordered_product__order', 
        1: 'purchaser',
        2: 'sum_amount',
        3: '',
        4: 'apply'
    }
#        2: 'tot_product',
#        3: 'sum_qta',
#        4: 'sum_price',
#        "{{row.tot_product}}",
#        "{{row.sum_qta}}",
#        "{{row.sum_price}}",
#    <th title='{% trans "TOT Ordered Products" %}'>{% trans "n Art." %}</th>
#    <th title='{% trans "SUM Ordered Quantity" %}'>{% trans "Sum Qta" %}</th>
#    <th title='{% trans "SUM ordered Price" %}'>{% trans "Sum Price" %}</th>

    def _get_user_actions(self, request):
  
        user_actions = []

        order = self.resource.order

        if request.user.has_perm(CASH, obj=ObjectWithContext(order.gas)) or \
            request.user == order.referrer_person.user:

            if order.is_closed() or order.is_unpaid():

                user_actions += [
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=VIEW, verbose_name=_("Show"),
                        popup_form=False,
                        method="get",
                    ),
                    ResourceBlockAction(
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=EDIT_MULTIPLE, verbose_name=_("Edit"),
                        popup_form=False,
                        method="get",
                    ),
                ]

        return user_actions

    def _get_resource_list(self, request):
        
        #return GASMember objects
        order = request.resource.order
        #qs = order.ordered_gasmembers.order_by('person__surname', 'person__name')
        #'RawQuerySet' object has no attribute 'order_by'
        qs = order.ordered_gasmembers
        accounted_amounts = order.gas.accounting.accounted_amount_by_gas_member(order)
        gasmembers = set()
        for item in qs:
            gasmember = item
            gasmember.accounted_amount = None
            for member in accounted_amounts:
                if member.pk == item.pk:
                    gasmember.accounted_amount = member.accounted_amount 
                    break
            gasmembers.add(gasmember)

            #log.debug("op = %s, sum = %s, acc= %s" % (
            #    order.ordered_products.filter(purchaser=gasmember), 
            #    gasmember.sum_amount, gasmember.accounted_amount)
            #)
        return gasmembers

        #q_sql = request.resource.ordered_gasmembers_sql
#        i = 0
#        for item in q_sql:
#            i += 1
#            log.debug("Curtails enumerate (%s) - %s" % (i, item))
#            log.debug("---------Curtails sql  (%s) - %s" % (i, item))
#{'gasmember': u'Thual', 'purchaser_id': 1L, 'order_id': 1L, 'sum_amount': Decimal('23.660000'), 'sum_qta': Decimal('1.75'), 'tot_product': 2L, 'sum_price': Decimal('25.4800')}
        #return q_sql

    def _get_edit_multiple_form_class(self):
        return formset_factory(
            form=EcoGASMemberForm,
            formset=BaseFormSetWithRequest,
            extra=1
        )

    def _getItem(self, pairs, colname, default):
        for value, key in pairs:
            if bool(key == colname):
                return value
        return default

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
#       c = querySet.count()

        map_info = { }

        #Retrieve gasmembers orders curtails
        order = request.resource.order
        i = 0
        for i, item in enumerate(querySet):

            key_prefix = 'form-%d' % i

            log.debug("Curtails enumerate (%s) - %s" % (i, item))

            #'GASMember_Deferred_gas_id_id_in_gas_membership_fee' object has no attribute 'accounted_amount'
            log.debug("Accounted amounts: member %s, amount %s" % (item, item.accounted_amount))
            # WARNING: check EXACTLY for None value to know if a transaction is applied
            applied = item.accounted_amount is not None 
            if applied:
                accounted_wallet = item.accounted_amount
            else:
                accounted_wallet = item.sum_amount

            data.update({
               '%s-gm_id' % key_prefix : item.pk,
               '%s-original_amounted' % key_prefix : item.accounted_amount,
               '%s-amounted' % key_prefix : "%.2f" % round(accounted_wallet, 2),
               '%s-applied' % key_prefix : applied,
            })

            map_info[item.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = i + 1
        data['form-INITIAL_FORMS'] = i + 1
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        i = 0
        for i,item in enumerate(querySet):

            form = formset[map_info[item.pk]['formset_index']]

            records.append({
               'purchaser_id' : item.pk,
               'gasmember' : item,
               'sum_amount' : item.sum_amount,
               'amounted' : "%s %s %s" % (form['gm_id'], form['amounted'], form['original_amounted']),
               'apply' : form['applied'],
            })

        form = NewEcoGASMemberForm(request, prefix="new-fam")
        records.append({
           'purchaser_id' : 0,
           'gasmember' : form['gasmember'],
           'sum_amount' : 0,
           'amounted' : form['amounted'],
           'apply' : form['applied'],
        })

        return formset, records, {}

    def _do_post_edit_multiple(self):

        request = self.request
        form_class = self._get_edit_multiple_form_class()

        post_d = request.POST.copy()

        new_fam_d = {}
        for k,v in request.POST.items():
            if k.startswith('new-fam'):
                new_fam_d[k[len('new-fam-'):]] = v
                post_d.pop(k)
                
        try:
            formset = form_class(request, post_d)
        except AttributeError as e:
            # TODO-not-a-priority: fero ... thinking about it....
            # NOTE fero: Form refactory neeeded: 'WSGIRequest' object has no attribute 'get'
            # NOTE fero: Following NOTES-FERO we will do: 
            # NOTE fero: if isinstance(form_class, FormRequestWrapper)
            # NOTE fero:    f = form_class(request, request.POST)
            # NOTE fero:    formset = f.form
            formset = form_class(post_d)

        log.debug("post_d: %s, new_fam_d: %s" % (post_d, new_fam_d))
        new_fam_form = NewEcoGASMemberForm(request, new_fam_d)

        if formset.is_valid() and new_fam_form.is_valid():
            with transaction.commit_on_success():
                for form in formset:
                    # Check for data: empty formsets are full of empty data ;)
                    if form.cleaned_data:
                        try:

                            form.save()

                        except Exception, e:
                            msg = _("Curtail ERROR: ") + e.message
                            form._errors[0] = form.error_class([msg])
                            return self.response_error(form._errors)

                if new_fam_form.cleaned_data:
                    try:

                        new_fam_form.save()

                    except Exception, e:
                        msg = _("Curtail ERROR: ") + e.message
                        new_fam_form._errors[0] = form.error_class([msg])
                        return self.response_error(form._errors)

            return self.response_success()
        else:
            return self.response_error(formset.errors)

