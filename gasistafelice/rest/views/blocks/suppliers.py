from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers
from django.core.urlresolvers import reverse

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from rest.views.blocks.base import BlockWithList, ResourceBlockAction
from consts import CREATE

from app_supplier.models import Supplier
from des.models import Siteattr

from app_supplier.forms import AddSupplierForm

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

        user_actions += [
            ResourceBlockAction(
                block_name = self.BLOCK_NAME,
                resource = request.resource,
                name="export", verbose_name="GDXP",
                popup_form=False,
                url = "%s?%s" % (
                    reverse('gdxp.views.suppliers'), 
                    "pk__in=%s&opt_catalog=1" % ",".join(
                        map(lambda x: str(x.pk), self._get_resource_list(request)),
                    )
                ),
                method="OPENURL"
            ),
        ]

        return user_actions
        
    def _get_add_form_class(self):
        form_class = AddSupplierForm
        autoselect_fields_check_can_add(form_class, Supplier, self.request.user)
        return form_class

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

