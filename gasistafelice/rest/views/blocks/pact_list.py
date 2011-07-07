from gasistafelice.rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "pact_list"
    BLOCK_DESCRIPTION = _("Solidal Pacts")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "gasmember", "supplier", "person"] 

    def _get_resource_list(self, request):
        return request.resource.pact_list