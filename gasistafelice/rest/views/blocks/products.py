from rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

# COMMENT fero: Who cares about products? I think we only care about stocks!
# COMMENT fero: See default_settings.py we have no products_block in there

class Block(BlockWithList):

    BLOCK_NAME = "products"
    BLOCK_DESCRIPTION = _("Products")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier"] 

    def _get_resource_list(self, request):
        return request.resource.products

