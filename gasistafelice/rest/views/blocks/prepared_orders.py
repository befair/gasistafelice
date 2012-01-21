from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
#from gasistafelice.rest.views.blocks.open_orders import Block as OpenOrdersBlock
from gasistafelice.rest.views.blocks.base import BlockSSDataTables

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

#class Block(OpenOrdersBlock):
class Block(BlockSSDataTables):

    BLOCK_NAME = "prepared_orders"
    BLOCK_DESCRIPTION = _("Prepared orders")
    #BLOCK_VALID_RESOURCE_TYPES = ["supplier", "gas"]
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "pact"]

    def _get_resource_list(self, request):
        #GASSupplierOrder
        return request.resource.orders.prepared()

#    def _get_user_actions(self, request):
#        return []

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'pact__supplier__name',
        2: 'datetime_start',
        3: 'referrer_person__name',
        4: 'datetime_end',
        5: 'group_id',
        6: 'root_plan__pk'
    }

#        0: 'order', 'pk'
#        1: 'producer',
#        2: 'datetime_start__range',
#        3: 'referrer_person'
#        4: 'datetime_end',
#        5: 'group_id',
#        6: 'root_plan',
