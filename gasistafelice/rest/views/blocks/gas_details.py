"""View for block details specialized for a GAS"""

from django.conf import settings
from django.core.urlresolvers import reverse

from flexi_auth.models import ObjectWithContext

from gasistafelice.consts import EDIT, GAS_MEMBER

from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.rest.views import blocks


class Block(blocks.details.Block):

    BLOCK_NAME = "gas_details"
    BLOCK_DESCRIPTION = _("Details")
    BLOCK_VALID_RESOURCE_TYPES = ["gas"] 

    def _get_user_actions(self, request):
        """Who can edit GAS informations, has also the ability to configure it."""

        user_actions = super(Block, self)._get_user_actions(request)

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            
            act_configure = ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="configure", verbose_name=_("Configure"), 
                    popup_form=True,
                    url=
            )

            for i,act in enumerate(user_actions):
                # Change URL for action EDIT, insert "configure" action
                if act.name == EDIT:
                   act.url = reverse('admin:gas_gasconfig_change', args=(request.resource.config.pk,)) 
                   user_actions.insert(i, act_configure)
                   break
                   
        return user_actions

    def _get_roles_to_manage(self):
        """GAS roles management focus also on GAS_REFERRER_SUPPLIERs of its own Pacts"""

        roles = super(Block, self)._get_roles_to_manage()
        
        for pact in self.resource.pacts:
            roles |= pact.roles

        # Exclude GAS_MEMBER role which is managed by "Add gasmember" action
        roles.exclude(role_name=GAS_MEMBER)

        return roles

    def manage_roles(self, request):

        formset_class = self._get_roles_formset_class()

        if request.method == 'POST':

            formset = formset_class(request, request.POST)
            
            if formset.is_valid():
                with transaction.commit_on_success():
                    for form in formset:
                        # Check for data: empty formsets are full of empty data ;)
                        if form.cleaned_data:
                            form.save()
                return self.response_success()
        else:
            data = {}
            roles = request.resource.roles
            #FIXME: fero - refactory details block (this is valid for GAS)
            if request.resource.resource_type == "gas":
                for pact in request.resource.pacts:
                    roles |= pact.roles

            # Roles already assigned to resource
            pprrs = PrincipalParamRoleRelation.objects.filter(role__in=roles)
            # FIXME: see above
            pprrs = pprrs.exclude(role__role__name=GAS_MEMBER)
                

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

            formset = formset_class(request, data)

        context = {
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

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

