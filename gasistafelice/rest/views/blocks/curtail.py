from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction, CREATE_PDF
from gasistafelice.consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_xml_response, render_to_context_response

from gasistafelice.gas.models import GASMember, GASMemberOrder
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms.cash import EcoGASMemberForm, BaseFormSetWithRequest, formset_factory

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import cgi, os
from django.conf import settings

from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "curtail"
    BLOCK_DESCRIPTION = _("Curtail purchaser")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'ordered_product__order', 
        1: 'purchaser',
        2: 'sum_amount',
        3: ''
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

        #FIXME: Check if order is in "closed_state"  Not in Open STATE for CASH REFERRER
        #if request.user.has_perm(CASH, obj=ObjectWithContext(request.resource)):
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
        #return request.resource.ordered_gasmembers
        q_sql = request.resource.ordered_gasmembers_sql
#        i = 0
#        for item in q_sql:
#            i += 1
#            log.debug("Curtails enumerate (%s) - %s" % (i, item))
#            print("---------Curtails sql  (%s) - %s" % (i, item))
#{'gasmember': u'Thual', 'purchaser_id': 1L, 'order_id': 1L, 'sum_amount': Decimal('23.660000'), 'sum_qta': Decimal('1.75'), 'tot_product': 2L, 'sum_price': Decimal('25.4800')}
        return q_sql

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        #cnt = qs.count() #QuerySet
        cnt = len(qs)  #List
        return formset_factory(
                    form=EcoGASMemberForm,
                    formset=BaseFormSetWithRequest,
                    extra=cnt
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

#{'purchaser': 7L, 'sum_price': Decimal('98.0400'), 'ordered_product__order': 10L, 'tot_product': 5, 'sum_qta': Decimal('5.00')}

        #Retrieve gasmembers orders curtails
        order = request.resource
        accounting_data = order.pact.gas.accounting.accounted_amount_by_gas_member(order)
        for trx in accounting_data:
            print trx


        #for i,el in enumerate(querySet):
        i = 0
        for item in querySet:
            i += 1
            log.debug("Curtails enumerate (%s) - %s" % (i, item))
            pairs = [(v, k) for (k, v) in item.iteritems()]
            pk = self._getItem(pairs, 'purchaser_id', 0)
            key_prefix = 'form-%d' % i
            #querySet? 'dict' object has no attribute 'id' or 'order_id'

            #TODO: account_amounted must replace sum_amount if exist one accounting transaction
            ordered_tot_price =  self._getItem(pairs, 'sum_amount', 0)
            accounted_wallet =  self._getItem(pairs, 'account_amounted', 0)
            if accounted_wallet == 0:
                accounted_wallet = ordered_tot_price

            data.update({
               '%s-ord_id' % key_prefix : self._getItem(pairs, 'order_id', 0),
               '%s-gm_id' % key_prefix : pk,
               '%s-gm_id' % key_prefix : None,
               '%s-amounted' % key_prefix : accounted_wallet,
            })

            map_info[pk] = {'formset_index' : i}
            #map_info[i] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = i + 1
        data['form-INITIAL_FORMS'] = 0
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        #for i, el in enumerate(querySet):
        i = 0
        for item in querySet:
            i += 1
            log.debug("Curtails enumerate (%s) - %s" % (i, item))
            pairs = [(v, k) for (k, v) in item.iteritems()]
            pk = self._getItem(pairs, 'purchaser_id', 0)

            form = formset[map_info[pk]['formset_index']]
            #form = formset[map_info[i]['formset_index']]
            gasmember = GASMember.objects.get(id=pk)
            log.debug("Curtails gasmember -%s--%s->  %s" % (i, pk, gasmember))
            print "Curtails gasmember -%s--%s-> %s" % (i, pk, gasmember)

            records.append({
               'purchaser_id' : pk, #self._getItem(pairs, 'order_id', 0), #request.ressource.pk
               'gasmember' : gasmember,
               'tot_product' : self._getItem(pairs, 'tot_product', 0),
               'sum_qta' : self._getItem(pairs, 'sum_qta', 0),
               'sum_price' : self._getItem(pairs, 'sum_price', 0),
               'sum_amount' : self._getItem(pairs, 'sum_amount', 0),
               'amounted' : "%s %s %s" % (form['ord_id'], form['gm_id'], form['amounted']),
            })
#"{{row.amounted|escapejs}}"  --> "{{row.amounted|floatformat:"2"}}" cannot be done because is widget input
#               'pk' : el.order_id,
#               'gasmember' : gasmember,
#               'tot_product' : el.tot_product,
#               'sum_qta' : el.sum_qta,
#               'sum_pice' : el.sum_price,
#               'sum_amount' : el.sum_amount,
#               'amounted' : "%s %s" % (form['id'], form['amounted']),
#               'gasmember_pk' : el.purchaser,
#        "{{row.ordered_product__order|escapejs}}",
#        "{{row.purchaser|escapejs}}",
#        "{{row.tot_product}}",
#        "{{row.sum_qta}}",
#        "{{row.sum_price}}",
#        "&#8364; {{row.sum_amount|floatformat:"2"}}",
#        "{{row.amounted|escapejs}}",


        return formset, records, {}


    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = resource = request.resource

        return super(Block, self).get_response(request, resource_type, resource_id, args)

