"""View for block details specialized for a GAS"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from flexi_auth.models import PrincipalParamRoleRelation, ObjectWithContext

from gasistafelice.consts import EDIT, GAS_MEMBER

from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views.blocks import details

from gasistafelice.lib.shortcuts import render_to_context_response

from gasistafelice.gas.forms.base import EditGASForm

import logging
log = logging.getLogger(__name__)

class Block(details.Block):

    BLOCK_NAME = "gas_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

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

    def manage_roles(self, request):
        """This method is needed to filter out GAS_MEMBER roles"""

        formset_class = self._get_roles_formset_class()

        if request.method == 'POST':
            return super(Block, self).manage_roles(request)

        else:

            data = {}
            roles = self.resource.roles

            # HACK HERE
            # Exclude GAS_MEMBER role which is managed by "Add gasmember" action
            roles = roles.exclude(role__name=GAS_MEMBER)

            # Roles already assigned to resource
            pprrs = PrincipalParamRoleRelation.objects.filter(role__in=roles)

            i = 0
            for i,pprr in enumerate(pprrs):

                key_prefix = 'form-%d' % i
                data.update({
                   '%s-id' % key_prefix : pprr.pk,
                   '%s-person' % key_prefix : pprr.user.person.pk,
                   '%s-role' % key_prefix : pprr.role.pk,
                })

            data['form-TOTAL_FORMS'] = i + formset_class.extra
            data['form-INITIAL_FORMS'] = i
            data['form-MAX_NUM_FORMS'] = 0

            formset = formset_class(request, {})

        context = {
            #data is delivered directly to the template
            "data" : data,
            "formset": formset,
            'opts' : PrincipalParamRoleRelation._meta,
            'is_popup': False,
            'save_as' : False,
            'save_on_top': False,
            #'errors': helpers.AdminErrorList(form, []),
            #'media': mark_safe(adminForm.media),
            'form_url' : request.build_absolute_uri(),
            'add'  : False,
            'change' : True,
            'has_add_permission': False,
            'has_delete_permission': True,
            'has_change_permission': True,
            'show_delete' : True,

        }

        return render_to_context_response(request, "html/formsets.html", context)

