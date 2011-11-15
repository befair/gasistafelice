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
        2: 'tot_product',
        3: 'sum_qta',
        4: 'sum_price',
        5: 'sum_amount',
        6: ''
    }

#        "{{row.ordered_product__order|escapejs}}",
#        "{{row.purchaser|escapejs}}",
#        "{{row.tot_product}}",
#        "{{row.sum_qta}}",
#        "{{row.sum_price}}",
#        "&#8364; {{row.sum_amount|floatformat:"2"}}",
#        "{{row.amounted|escapejs}}",

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
        return request.resource.ordered_gasmembers

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        cnt = 0
        if qs:
            cnt = qs.count()
        return formset_factory(
                    form=EcoGASMemberForm,
                    formset=BaseFormSetWithRequest,
                    extra=cnt
        )

#    def __get_gmos(self, gso):
#        #log.debug("order block __get_gmos (%s)" % (self.request.resource.gasmember))
#        return GASMemberOrder.objects.filter(purchaser=1,ordered_product=1)

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        # [:] forces evaluation of the querySet
        #gmos = self.__get_gmos(querySet)[:]

        data = {}
        i = 0
        c = 0
        log.debug("Curtails enumerate (%s)" % querySet[:])
        if querySet:
            c = querySet.count()
        map_info = { }

        #TODO Retrieve Accounting movments list to set id in hiddenField
        for i,el in enumerate(querySet):
            log.debug("Curtails enumerate (%s) - %s" % (i, el))

            key_prefix = 'form-%d' % i
            #FIXME: in editing --> querySet? 'dict' object has no attribute 'id'
            data.update({
               '%s-id' % key_prefix : el.id, 
               '%s-gm_id' % key_prefix : el.purchaser, 
               '%s-amounted' % key_prefix : 3,
            })

#Cannot resolve keyword 'puchaser' into field. Choices are: id, is_confirmed, note, ordered_amount, ordered_price, ordered_product, purchaser, withdrawn_amount


            map_info[el.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = c #i 
        data['form-INITIAL_FORMS'] = c #0
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        for i, el in enumerate(querySet):

            form = formset[map_info[el.pk]['formset_index']]
            gasmember = GASMember.objects.get(id=el.purchaser)
            records.append({
               'pk' : 1, #el.id,
               'gasmember' : gasmember,
               'tot_product' : el.tot_product,
               'sum_qta' : el.sum_qta,
               'sum_pice' : el.sum_price,
               'sum_amount' : el.sum_amount,
               'amounted' : "%s %s" % (form['id'], form['amounted']),
            })

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

