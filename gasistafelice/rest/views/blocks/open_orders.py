from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.contrib.auth.models import User

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT
from gasistafelice.gas.forms import order as order_forms
from gasistafelice.gas.models import GASSupplierOrder

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "open_orders"
    BLOCK_DESCRIPTION = _("Open orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact", "stock"] 

    TEMPLATE_RESOURCE_LIST = "blocks/open_orders.xml"

    def _get_add_form_class(self):
        return order_forms.form_class_factory_for_request(self.request, base=order_forms.AddOrderForm)

    def _get_resource_list(self, request):
        return request.resource.orders.open()

    def _get_user_actions(self, request):

        user_actions = []
        ctx = { request.resource.resource_type : request.resource }

        if request.user.has_perm(CREATE, 
            obj=ObjectWithContext(GASSupplierOrder, context=ctx)
        ):
        
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add order"), 
                    popup_form=True
                ),
             ]

        return user_actions


