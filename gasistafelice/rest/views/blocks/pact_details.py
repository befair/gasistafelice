"""View for block details specialized for a GASSupplierSolidalPact"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from rest.views.blocks import details
from app_gas.forms.pact import EditPactForm


class Block(details.Block):

    BLOCK_NAME = "pact_details"
    BLOCK_VALID_RESOURCE_TYPES = ["pact"] 

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        return EditPactForm 


