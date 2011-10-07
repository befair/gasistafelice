from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE
from gasistafelice.gas.models.base import GASMember

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "gasmembers"
    BLOCK_DESCRIPTION = _("GAS members")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas"] 

    def _get_resource_list(self, request):
        return request.resource.gasmembers

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, obj=GASMember):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add GAS member"), 
                    url=urlresolvers.reverse('admin:gas_gasmember_add')
                )
            )

        return user_actions
        
    def _get_add_form_class(self):
        raise NotImplementedError("The add form page in use now is the admin interface page.")

