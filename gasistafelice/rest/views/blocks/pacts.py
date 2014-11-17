from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from rest.views.blocks.base import BlockWithList

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):
    """This is a base block class for pact management.

    See gas_pacts, supplier_pacts, des_pacts block for specific implementation.
    """

    BLOCK_NAME = "pacts"
    BLOCK_DESCRIPTION = _("Solidal pacts")
    # this block is not valid. Please see gas_pacts. des_pacts, supplier_pacts
    BLOCK_VALID_RESOURCE_TYPES = []

    def _get_resource_list(self, request):
        return request.resource.pacts

