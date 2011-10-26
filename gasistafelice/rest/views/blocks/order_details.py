"""View for block details specialized for a GASSupplierOrder"""

from gasistafelice.rest.views import blocks
from gasistafelice.gas.forms import order as order_forms


class Block(blocks.details.Block):

    BLOCK_NAME = "order_details"
    BLOCK_DESCRIPTION = _("Details")
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    def _get_edit_form_class(self):
        # TODO: TOVERIFY fero
        """GASSupplierOrder is an atom, so we have to return a formset"""
        return order_forms.form_class_factory_for_request(self.request, base=order_forms.EditOrderForm)


