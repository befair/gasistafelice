from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from rest.views.blocks.base import BlockWithList, ResourceBlockAction
from consts import CREATE
from app_gas.models import GAS
from des.models import Siteattr, DES

from app_gas.forms.base import AddGASForm


#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):
    """Render GAS list block with the ability to create a new GAS"""

    BLOCK_NAME = "gas_list"
    BLOCK_DESCRIPTION = _("GAS")
    BLOCK_VALID_RESOURCE_TYPES = ["site"] 

    def _get_resource_list(self, request):
        return request.resource.gas_list

    def _get_user_actions(self, request):

        user_actions = []

        des = Siteattr.get_site()

        if request.user.has_perm(CREATE, obj=ObjectWithContext(GAS, context={'site' : des})):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add GAS"), 
                    #WAS admin: url=urlresolvers.reverse('admin:gas_gas_add')
                )
            )

        return user_actions
        
    def _get_add_form_class(self):
        form_class = AddGASForm
        autoselect_fields_check_can_add(form_class, GAS, self.request.user)
        return form_class

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
