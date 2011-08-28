from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "gasmember_list"
    BLOCK_DESCRIPTION = _("GAS Members")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas" , "person", "order", "pact" "delivery", "withdrawal"] 

    def _get_resource_list(self, request):
        return request.resource.gasmember_list

