from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
#from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.consts import EDIT, CONFIRM, EDIT_MULTIPLE, VIEW

#from gasistafelice.gas.forms.base import SupplierSingleUserForm
#from django.forms.formsets import formset_factory
#from gasistafelice.lib.formsets import BaseFormSetWithRequest

from gasistafelice.rest.views.blocks import users 

from flexi_auth.models import ObjectWithContext

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(users.Block):

    BLOCK_NAME = "gas_users"
    BLOCK_DESCRIPTION = _("Users")
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"]

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show"), 
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit"), 
                    popup_form=False,
                    method="get",
                ),
            ]

        return user_actions

#    def _get_edit_multiple_form_class(self):
#        qs = self._get_resource_list(self.request)
#        return formset_factory(
#                    form=SupplierSingleUserForm,    #SingleUserForm,
#                    formset=BaseFormSetWithRequest, 
#                    extra=qs.count()   #0
#        )
# 
