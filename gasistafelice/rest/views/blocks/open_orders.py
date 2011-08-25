from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, Action, ResourceBlockAction
from gasistafelice.auth import CREATE
from gasistafelice.gas.forms import GASSupplierOrderForm
from gasistafelice.gas.models import GASSupplierOrder

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "open_orders"
    BLOCK_DESCRIPTION = _("Open orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "supplier", "gas"] 

    def _get_add_form_class(self):
        return GASSupplierOrderForm

    def _get_resource_list(self, request):
        return request.resource.orders.open()

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, obj=GASSupplierOrder):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add order"), 
                    popup_form=True
                ),
             ]
        return user_actions

#            user_actions.append(self.ACTION_CREATE)
#
#        if request.user.has_perm(EDIT, obj=Supplier):
#            user_actions += [
#                ResourceBlockAction( 
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=VIEW, verbose_name=_("Show stock"), 
#                    popup_form=False,
#                ),
#                ResourceBlockAction( 
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=EDIT_MULTIPLE, verbose_name=_("Edit stock"), 
#                    popup_form=False,
#                ),
#            ]
#
#
#        # Actions
#        ACTION_CREATE = Action(
#            name=CREATE, 
#            verbose_name=_("Open a new order"), 
#        )

        return user_actions

