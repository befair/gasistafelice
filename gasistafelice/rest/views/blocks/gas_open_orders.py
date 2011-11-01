from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.contrib.auth.models import User

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, Action, ResourceBlockAction
from gasistafelice.consts import CREATE, EDIT
from gasistafelice.gas.forms import order as order_forms
from gasistafelice.gas.models import GASSupplierOrder, GASSupplierSolidalPact

from gasistafelice.rest.views.blocks import open_orders

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(open_orders.Block):

    BLOCK_NAME = "gas_open_orders"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"] 

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, 
            obj=ObjectWithContext(GASSupplierOrder, context={'gas': request.resource.gas})
        ):
        
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add order"), 
                    popup_form=True
                ),
             ]

        return user_actions

