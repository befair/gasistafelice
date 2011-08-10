from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "gasmembers"
    BLOCK_DESCRIPTION = _("Lista gasisti")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas"]

    def _get_resource_list(self, request):
        return request.resource.gasmembers

