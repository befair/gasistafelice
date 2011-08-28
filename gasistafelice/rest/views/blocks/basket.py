from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import EDIT, CONFIRM

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.lib.http import HttpResponse

from django.template.defaultfilters import floatformat

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "basket"
    BLOCK_DESCRIPTION = _("Basket")
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember"] 

    COLUMN_INDEX_NAME_MAP = { 0: 'product__order__pk', 1 : 'product__stock__supplier_stock__supplier', 2: 'product', 3: 'ordered_amount', 4: 'ordered_price' }

    def _get_user_actions(self, request):

        user_actions = []

        if not request.resource.gas.config.gasmember_auto_confirm_order:

            #TODO seldon: does this work for a GASMember?
            #if request.user.has_perm(EDIT, obj=request.resource):
            if request.user == request.resource.person.user:
                user_actions += [
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=CONFIRM, verbose_name=_("Confirm all"), 
                        popup_form=False,
                    ),
                ]

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.basket

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        records = []
        c = querySet.count()

        for el in querySet:

            records.append({
               'order' : el.product.order.pk,
               'supplier' : el.product.stock.supplier,
               'product' : el.product,
               'amount' : el.ordered_amount,
               'price' : floatformat(el.ordered_price, 2),
            })

        return records

    def _set_records(self, request, records):
        pass

    def get_response(self, request, resource_type, resource_id, args):

        resource = request.resource

        if args == CONFIRM:
            for gmo in resource.basket:
                gmo.confirm()

            #IMPORTANT: unset args to compute table results!
            args = self.KW_DATA

        return super(Block, self).get_response(request, resource_type, resource_id, args)

