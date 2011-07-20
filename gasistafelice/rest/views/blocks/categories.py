from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "categories"
    BLOCK_DESCRIPTION = _("Categories")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier", "gas", "des"] 

    def _get_resource_list(self, request):
        return request.resource.categories

