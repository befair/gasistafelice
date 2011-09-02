from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms import GASSupplierStockFormSet
from django.template.defaultfilters import floatformat

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "gasstocks"
    BLOCK_DESCRIPTION = _("GAS Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["pact"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'code', 
        2: 'product', 
        3: 'product__description', 
        4: 'price', 
        5: 'availability',
        6: 'enabled' 
    }

    def _get_resource_list(self, request):
        return request.resource.gasstocks

    def _get_edit_multiple_form_class(self):
        return GASSupplierStockFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        
        for i,el in enumerate(querySet):
            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-enabled' % key_prefix : el.enabled,
            })

        data['form-TOTAL_FORMS'] = i 
        data['form-INITIAL_FORMS'] = 0
        data['form-MAX_NUM_FORMS'] = 0

        formset = GASSupplierStockFormSet(request, data)

        records = []
        c = querySet.count()
        for i,form in enumerate(formset):

            records.append({
               'id' : form['id'],
               'code' : el.stock.code or '',
               'product' : el.stock.product,
               'price' : floatformat(el.stock.price, 2),
               'availability' : bool(el.stock.amount_available),
               'field_enabled' : form['enabled'],

            })

        return formset, records, {}

