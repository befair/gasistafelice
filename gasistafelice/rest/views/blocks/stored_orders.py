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
        1: 'order'
    }
#        2: 'tot_amount',
#        3: 'tot_gasmembers',
#        4: 'tot_price',
#        5: 'Invoice',
#        6: 'tot_curtail',
#        7: 'Payment'

    def _get_resource_list(self, request):
        #GASSupplierOrder
#        return request.resource.orders.archived()
        return request.resource.orders.closed()

#        "{{gso.tot_amount|escapejs|floatformat:"-2"}}",
#        "{{gso.tot_gasmembers|escapejs}}",
#        "&#8364; {{gso.tot_price|escapejs|floatformat:2}}",
#        "&#8364; {{gso.delivery_cost|escapejs|floatformat:2}}",
#        "&#8364; {{gso.tot_curtail|escapejs|floatformat:2}}",
#        "{{gso.payment|escapejs}}",


#    <th>{% trans "Amount" %}</th>
#    <th>{% trans "Members" %}</th>
#    <th>{% trans "Ordered price" %}</th>
#    <th>{% trans "Invoice" %}</th>
#    <th>{% trans "Gasmember's curtail sum" %}</th>
#    <th>{% trans "Payment" %}</th>

