from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from rest.views.blocks.base import BlockWithList, ResourceBlockAction
from consts import CREATE
from gf.gas.models.base import GASMember

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

        try:
            #TODO: block refactory needed!
            # We need this control because gas attribute is a NoSense in "site" resource (DES)
            gas = request.resource.gas
        except NotImplementedError:
            pass
        else:
            if request.user.has_perm(CREATE, 
                obj=ObjectWithContext(GASMember, context={'gas' : gas})):

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

