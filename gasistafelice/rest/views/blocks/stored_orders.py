from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables




#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "stored_orders"
    BLOCK_DESCRIPTION = _("Stored orders")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact"]

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'pk',
        2: 'pk',
        3: 'pk',
        4: 'pk',
        5: 'pk',
        6: 'pk',
        7: 'pk'
    }

#        1: 'order',
#        2: 'tot_amount',
#        3: 'tot_gasmembers',
#        4: 'tot_price'
#        5: 'Invoice',
#        6: 'tot_curtail',
#        7: 'Payment'

    def _get_resource_list(self, request):
        #GASSupplierOrder
        return request.resource.orders.archived()
        #return request.resource.orders.closed()  #Only for test purpose

