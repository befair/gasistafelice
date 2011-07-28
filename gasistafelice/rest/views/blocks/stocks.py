from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "stocks"
    BLOCK_DESCRIPTION = _("Stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"] 

    TEMPLATE_RESOURCE_LIST_WITH_DETAILS = 'blocks/stocks_with_details.xml'

    def _get_resource_list(self, request):
        return request.resource.stocks

