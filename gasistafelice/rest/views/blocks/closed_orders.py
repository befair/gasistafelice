from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from rest.views.blocks.open_orders import Block as OpenOrdersBlock

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(OpenOrdersBlock):

    BLOCK_NAME = "closed_orders"
    BLOCK_DESCRIPTION = _("Closed orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "supplier", "gas"] 

    TEMPLATE_RESOURCE_LIST = "blocks/orders.xml"

    def _get_resource_list(self, request):
        return request.resource.orders.closed()

    def _get_user_actions(self, request):

        return []

