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
        1: 'gassupplierorder__order',
        2: 'gassupplierorder__order__pact',
        3: 'gassupplierorder__order__pact__supplier__name',
        4: 'gassupplierorder__order__pact__gas',
        5: '',
        6: ''
    }

#KO: Cannot resolve keyword 'order' into field. Choices are: datetime_end, datetime_start, delivery, delivery_cost, delivery_referrer_person, gasstock_set, gassupplierorder, group_id, historicalgassupplierorder, historicalorderable_product_
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
