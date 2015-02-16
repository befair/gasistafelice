from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from consts import CREATE, EDIT, EDIT_MULTIPLE, VIEW

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from app_supplier.models import Supplier
from app_gas.forms.stocks import GASSupplierStockFormSet

from flexi_auth.models import ObjectWithContext

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "gasstocks"
    BLOCK_DESCRIPTION = _("GAS Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["pact"] 

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'stock__product__name',
        2: 'stock__product__category__name',
        3: 'stock__price',
        4: 'stock__amount_available',
        5: 'enabled',
        6: 'tot_amount',
        7: 'tot_gasmembers',
        8: 'tot_price'
    }
#Cannot resolve keyword 'tot_amount' into field. Choices are: enabled, gassupplierorder, historicalorderable_product_set, id, minimum_amount, orderable_product_set, pact, step, stock

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
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
        #GASSupplierStock
        return request.resource.gasstocks.order_by('stock__product__category__name', 'stock__product__name')

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
               '%s-pk' % key_prefix : el.pk,
               '%s-enabled' % key_prefix : el.enabled,
            })

        data['form-TOTAL_FORMS'] = i + 1
        data['form-INITIAL_FORMS'] = i + 1
        data['form-MAX_NUM_FORMS'] = 0

        formset = GASSupplierStockFormSet(request, data)

        records = []
        for i,form in enumerate(formset):

            enabling = querySet[i].stock.amount_available
            if enabling:
                enabling = form['enabled']
            else:
                enabling = _('not available')

            records.append({
               'id' : "%s %s " % (form['pk'], form['id']),
               'product' : querySet[i].__unicode__(),
               'category' : querySet[i].stock.product.category,
               'price' : querySet[i].report_price,
               'availability' : querySet[i].stock.amount_available,
               'field_enabled' : enabling,
               'tot_amount' : querySet[i].tot_amount,
               'tot_gasmembers' : querySet[i].tot_gasmembers,
               'tot_price' : querySet[i].tot_price,
            })
               #'product' : querySet[i].stock.product,
               #'price' : querySet[i].price,
               #'field_enabled' : [_('not available'),form['enabled']][bool(querySet[i].enabled)],
               #DOMTHU: "&#8364; {{ gss.price|floatformat:2 }}",

        return formset, records, {}

