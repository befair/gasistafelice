from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from gasistafelice.rest.views.blocks.open_orders import Block as OpenOrdersBlock

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(OpenOrdersBlock):

    BLOCK_NAME = "prepared_orders"
    BLOCK_DESCRIPTION = _("Prepared orders")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier", "gas"] 

    def _get_resource_list(self, request):
        return request.resource.orders.prepared()

    def _get_user_actions(self, request):

        return []

