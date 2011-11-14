"""View for block details specialized for a SupplierStock"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details
from gasistafelice.supplier.forms import EditStockForm

class Block(details.Block):

    BLOCK_NAME = "stock_details"
    BLOCK_VALID_RESOURCE_TYPES = ["stock"] 

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        return EditStockForm 


