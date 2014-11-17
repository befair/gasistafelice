"""View for block details specialized for a GAS"""

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core.urlresolvers import reverse
from django.conf import settings

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from consts import EDIT

<<<<<<< HEAD
from gasistafelice.rest.views.blocks.base import ResourceBlockAction, EXPORT_GDXP
from gasistafelice.rest.views.blocks import details
from gasistafelice.supplier.models import Supplier
=======
from rest.views.blocks.base import ResourceBlockAction
from rest.views.blocks import details
from app_supplier.models import Supplier
>>>>>>> [Django17] Variazione nome delle applicazioni e import

from lib.shortcuts import render_to_context_response

from app_supplier.forms import EditSupplierForm, SupplierRoleForm

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
                   
            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="export", verbose_name="GDXP",
                    popup_form=False,
                    url = "%s?%s" % (
                        reverse('gdxp.views.suppliers'), 
                        "pk=%s&opt_catalog=1" % request.resource.pk
                    ),
                    method="OPENURL"
                ),
            ]

        return user_actions

    def _get_edit_form_class(self):
        form_class = EditSupplierForm
        autoselect_fields_check_can_add(form_class, Supplier, self.request.user)
        return form_class


