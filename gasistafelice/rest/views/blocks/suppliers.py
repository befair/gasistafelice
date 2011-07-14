from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, Action
from gasistafelice.auth import CREATE

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "suppliers"
    BLOCK_DESCRIPTION = _("Suppliers")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas"] 

    # Actions
    ACTION_CREATE = Action(
        name=CREATE, 
        verbose_name=_("Add Supplier"), 
        url=urlresolvers.reverse('admin:supplier_supplier_add')
    )

    def _get_resource_list(self, request):
        return request.resource.suppliers

    def _get_user_actions(self, request):

        user_actions = []
        # TODO seldon placeholder: check if a user can create a GAS
        if request.user.has_perm(CREATE, obj=request.resource):
            user_actions.append(self.ACTION_CREATE)

        return user_actions
        
    def _get_add_form_class(self):
        raise NotImplementedError("The add form page in use now is the admin interface page.")

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

