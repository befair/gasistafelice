from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "gasstocks"
    BLOCK_DESCRIPTION = _("GAS stocks")
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

    def _get_resource_list(self, request):
        return request.resource.gasstocks

