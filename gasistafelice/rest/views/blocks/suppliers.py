from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from flexi_auth.models import ObjectWithContext

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.consts import CREATE

from gasistafelice.supplier.models import Supplier
from gasistafelice.des.models import Siteattr

from gasistafelice.supplier.forms import AddSupplierForm

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "suppliers"
    BLOCK_DESCRIPTION = _("Suppliers")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas"]

    def _get_resource_list(self, request):
        return request.resource.suppliers

    def _get_user_actions(self, request):

        user_actions = []
        des = Siteattr.get_site()

        if request.user.has_perm(CREATE, \
            obj=ObjectWithContext(Supplier, context={'site':des})):

            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add supplier"), 
                    #WAS Supplier admin: url=urlresolvers.reverse('admin:supplier_supplier_add')
                )
            )

        return user_actions
        
    def _get_add_form_class(self):
        return AddSupplierForm

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

