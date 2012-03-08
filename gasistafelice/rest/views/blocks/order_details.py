"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details
from gasistafelice.gas.forms import order as order_forms

from gasistafelice.consts import INCOME, EXPENSE
from gasistafelice.rest.views.blocks.base import ResourceBlockAction

import logging
log = logging.getLogger(__name__)


class Block(details.Block):

    BLOCK_NAME = "order_details"
    BLOCK_VALID_RESOURCE_TYPES = ["order"]

    def _get_edit_form_class(self):
        return order_forms.form_class_factory_for_request(self.request, base=order_forms.EditOrderForm)

    def _get_user_actions(self, request):

        user_actions = super(Block, self)._get_user_actions(request)

        #refs = [] #request.resource.cash_referrers
        #if refs and request.user in refs:

        #UGLY: remove this code when send email transition is done. 
        #REMOVE temporarly un-managed transitions
        new_user_actions = []
        for ua in user_actions:
            #print("User action: %s" % ua.name)
            if ua.name not in [
                'transition/make unpaid',
                'transition/close and send email', #FIXME: disabled actions until implemented
                'transition/archive'
            ]:
                new_user_actions.append(ua)

        return new_user_actions


