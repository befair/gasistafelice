"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details
from gasistafelice.gas.forms import order as order_forms


class Block(details.Block):

    BLOCK_NAME = "order_details"
    BLOCK_VALID_RESOURCE_TYPES = ["order"] 

    def _get_edit_form_class(self):
        # TODO: TOVERIFY fero
        """GASSupplierOrder is an atom, so we have to return a formset"""
        return order_forms.form_class_factory_for_request(self.request, base=order_forms.EditOrderForm)


