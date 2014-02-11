"""View for block details specialized for a GAS"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core.urlresolvers import reverse
from django.conf import settings

from flexi_auth.models import ObjectWithContext

from gasistafelice.consts import EDIT

from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import details

from gasistafelice.lib.shortcuts import render_to_context_response

from gasistafelice.supplier.forms import EditSupplierForm, SupplierRoleForm

import logging
log = logging.getLogger(__name__)

class Block(details.Block):

    BLOCK_NAME = "supplier_details"
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"]
    FORMCLASS_MANAGE_ROLES = SupplierRoleForm

    def _get_user_actions(self, request):
        """Who can edit Supplier informations, has also the ability to configure it."""

        user_actions = super(Block, self)._get_user_actions(request)

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            
            act_configure = ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="configure", verbose_name=_("Configure"),
                    popup_form=True,
                    url = reverse('admin:supplier_supplierconfig_change', args=(request.resource.config.pk,))
            )

            for i,act in enumerate(user_actions):
                # Change URL for action EDIT, insert "configure" action
                if act.name == EDIT:
#                   act.url = reverse('admin:supplier_supplier_change', args=(request.resource.pk,)) 
                   user_actions.insert(i+1, act_configure)
                   break
                   
        return user_actions

    def _get_edit_form_class(self):
        log.debug ("Loading my edit form class...")
        return EditSupplierForm


