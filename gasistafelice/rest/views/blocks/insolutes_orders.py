from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from gasistafelice.rest.views.blocks.open_orders import Block as OpenOrdersBlock

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

EURO_HTML = '&#8364;'  # &amp;euro; &#8364; &euro;  &#128;  &#x80;

class Block(OpenOrdersBlock):

    BLOCK_NAME = "insolutes_orders"
    BLOCK_DESCRIPTION = _("Orders to be payed")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier"] 

    TEMPLATE_RESOURCE_LIST = "blocks/insolutes_orders.xml"

    def _get_resource_list(self, request):
        insolutes = request.resource.insolutes
        for insolute in insolutes:
            insolute.more_details = insolute.display_totals.replace('euro', EURO_HTML)
        return insolutes

    def _get_user_actions(self, request):
    
        return []

