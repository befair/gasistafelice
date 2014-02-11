"""View for block details specialized for a GAS"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from flexi_auth.models import PrincipalParamRoleRelation, ObjectWithContext

from gasistafelice.consts import EDIT, GAS_MEMBER

from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import details

from gasistafelice.lib.shortcuts import render_to_context_response

from gasistafelice.gas.forms.base import EditGASForm, GASRoleForm


import logging
log = logging.getLogger(__name__)

class Block(details.Block):

    BLOCK_NAME = "gas_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]
    FORMCLASS_MANAGE_ROLES = GASRoleForm

    def get_description(self):
        return _("Details about %(name)s") % {
            'name' : self.resource.gas.name,
        }

    def _get_edit_form_class(self):
        log.debug ("Loading my edit form class...")
        return EditGASForm

    def _get_user_actions(self, request):
        """Who can edit GAS informations, has also the ability to configure it."""

        user_actions = super(Block, self)._get_user_actions(request)

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            
            act_configure = ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="configure", verbose_name=_("Configure"),
                    popup_form=True,
                    url = reverse('admin:gas_gasconfig_change', args=(request.resource.config.pk,))
            )

            for i,act in enumerate(user_actions):
                # Change URL for action EDIT, insert "configure" action
                if act.name == EDIT:
#                   act.url = reverse('admin:gas_gas_change', args=(request.resource.pk,)) 
                   user_actions.insert(i+1, act_configure)
                   break
                   
        return user_actions

