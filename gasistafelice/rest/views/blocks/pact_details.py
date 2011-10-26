"""View for block details specialized for a GASSupplierSolidalPact"""

from gasistafelice.rest.views import blocks
from gasistafelice.gas.forms.pact import EditPactForm


class Block(blocks.details.Block):

    BLOCK_NAME = "pact_details"
    BLOCK_DESCRIPTION = _("Details")
    BLOCK_VALID_RESOURCE_TYPES = ["pact"] 

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        return EditPactForm 


