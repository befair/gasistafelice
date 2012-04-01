from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from gasistafelice.rest.views.blocks.open_orders import Block as OpenOrdersBlock

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(OpenOrdersBlock):

    BLOCK_NAME = "unpaid_orders"
    BLOCK_DESCRIPTION = _("Unpaid orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier"] 

    #TEMPLATE_RESOURCE_LIST = "blocks/unpaid_orders.xml"

    def _get_resource_list(self, request):
        return request.resource.orders.unpaid()

    def _get_user_actions(self, request):
    
        return []

