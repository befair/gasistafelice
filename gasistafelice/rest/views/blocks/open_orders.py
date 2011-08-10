from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, Action
from gasistafelice.auth import CREATE
from gasistafelice.gas.forms import GASSupplierOrderForm

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "open_orders"
    BLOCK_DESCRIPTION = _("Open orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "supplier", "gas"]

    # Actions
    ACTION_CREATE = Action(
        name=CREATE, 
        verbose_name=_("Open a new order"), 
    )

    def _get_add_form_class(self):
        return GASSupplierOrderForm

    def _get_resource_list(self, request):
        return request.resource.orders.open()

    def _get_user_actions(self, request):

        user_actions = []
        # TODO seldon placeholder: check if a user can create an Order
        if request.user.has_perm(CREATE, obj=request.resource):
            user_actions.append(self.ACTION_CREATE)

        return user_actions

