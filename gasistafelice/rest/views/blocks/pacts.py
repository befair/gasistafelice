from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE
from gasistafelice.gas.models.base import GASSupplierSolidalPact
from gasistafelice.gas.forms.pact import GAS_PactForm, Supplier_PactForm

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "pacts"
    BLOCK_DESCRIPTION = _("Solidal pacts")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier"]

    def _get_resource_list(self, request):
        return request.resource.pacts

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, obj=GASSupplierSolidalPact):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add pact"), 
                    popup_form=True
                )
            )

        return user_actions
        
    def _get_add_form_class(self):

        #TODO use content type framework
        ct_name = self.resource.__class__.__name__
        if ct_name == "GAS":
            return GAS_PactForm
        elif ct_name == "Supplier":
            return Supplier_PactForm
        else:
            raise NotImplementedError("No add form for GASSupplierSolidalPact within a %s" % ct_name)

