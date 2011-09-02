from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.forms import GASSupplierOrderProductFormSet
from django.template.defaultfilters import floatformat

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "order_report"
    BLOCK_DESCRIPTION = _("Order report")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'product',
        1: 'price', 
        2: 'tot_gasmembers',
        3: 'tot_amount',
        4: 'tot_price',
        5: 'enabled' 
    }

    def _get_resource_list(self, request):
        # Maybe we need to switch args KW_DATA, or EDIT_MULTIPLE
        # to get GASSupplierOrderProduct or GASSupplierStock respectively
        return request.resource.orderable_products

    def _get_edit_multiple_form_class(self):
        return GASSupplierOrderProductFormSet

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        
        for i,el in enumerate(querySet):

            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk,
               '%s-enabled' % key_prefix : True,
            })

        data['form-TOTAL_FORMS'] = i 
        data['form-INITIAL_FORMS'] = 0
        data['form-MAX_NUM_FORMS'] = 0

        formset = GASSupplierOrderProductFormSet(request, data)

        records = []
        c = querySet.count()
        for i,form in enumerate(formset):

            records.append({
               'product' : el.stock.product,
               'price' : floatformat(el.stock.price, 2),
               'tot_gasmembers' : el.tot_gasmembers,
               'tot_amount' : el.ordered_amount,
               'tot_price' : el.tot_price,
               'field_enabled' : "%s %s" % (form['id'], form['enabled']),

            })

        return formset, records, {}

