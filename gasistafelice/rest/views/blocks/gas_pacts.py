from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE
from gasistafelice.gas.models.base import GASSupplierSolidalPact
from gasistafelice.gas.forms.pact import GAS_PactForm

from gasistafelice.rest.views.blocks import pacts

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(pacts.Block):

    BLOCK_NAME = "gas_pacts"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, obj=ObjectWithContext(GASSupplierSolidalPact, context={'gas':request.resource.gas})):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource.gas,
                    name=CREATE, verbose_name=_("Add pact"), 
                    popup_form=True
                )
            )

        return user_actions
        
    def _get_add_form_class(self):

        return GAS_PactForm
