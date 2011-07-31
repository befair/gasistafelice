from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.auth import CREATE, EDIT, EDIT_MULTIPLE

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gasistafelice.supplier.models import Supplier
from gasistafelice.supplier.forms import SingleSupplierStockForm
from django.template.defaultfilters import floatformat

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=Supplier):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit stock"), 
                    popup_form=False,
                )
            )

        return user_actions
        
    def _get_resource_list(self, request):
        return request.resource.stocks

    def _get_edit_multiple_form_record(self, request, el):

        #build form fields
        f = SingleSupplierStockForm(initial={
           'code' : el.code,
           'product' : el.product,
           'price' : floatformat(el.price, 2),
           'availability' : el.availability,
        })

        return {
            'code' : f['code'],
            'product' : f['product'],
            'description' : el.product.description,
            'price' : f['price'],
            'availability' : f['availability'],
        }

