"""View for block details specialized for a Person"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin import helpers
from django.utils.html import escape

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from gasistafelice.rest.views.blocks import details
from gasistafelice.base.forms import EditPersonForm
from gasistafelice.base.models import Person
from gasistafelice.consts import EDIT
from gasistafelice.rest.views.blocks.base import ResourceBlockAction
from gasistafelice.lib.shortcuts import render_to_context_response


class Block(details.Block):

    BLOCK_NAME = "person_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember", "person"] 

    def get_description(self):
        return _("Who is %(name)s?") % {
            'name' : self.resource.person.name,
        }

    def _get_edit_form_class(self):
        form_class = EditPersonForm
        autoselect_fields_check_can_add(form_class, Person, self.request.user)
        return form_class

    def _get_user_actions(self, request):
        user_actions = super(Block, self)._get_user_actions(request)
        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):

            user_actions.append(

                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="changepw", verbose_name=_("Change password"), 
                    popup_form=True,
                )
            )

        return user_actions

    @property
    def resource(self):
        return self._resource.person

    @resource.setter
    def resource(self, value):
        self._resource = value

    change_password_form = PasswordChangeForm

    def __change_password(self, request):

        user = self.resource.user
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = _('Password changed successfully.')
                messages.success(request, msg)
                return self.response_success()
        else:
            form = self.change_password_form(user)

        fields = form.base_fields.keys()
        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = helpers.AdminForm(form, fieldsets, {}) 

        context = {
            'title': _('Change password: %s') % escape(user.username),
            'form' : form,
            'adminform' : adminForm,
            'opts' : user.__class__._meta,
            'add'  : False,
            'change' : True,
            'is_popup': False,
            'save_as' : False,
            'save_on_top': False,
            'has_add_permission': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'show_delete' : False,
            'errors': helpers.AdminErrorList(form, []),
        }

        return render_to_context_response(request, 
            #'admin/auth/user/change_password.html', 
            "html/admin_form.html", 
            context
        )

    def get_response(self, request, resource_type, resource_id, args):

        rv = super(Block, self).get_response(request, resource_type, resource_id, args)
        if not rv and args == "changepw":
            if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
                with transaction.commit_on_success():
                    rv = self.__change_password(request)
                return rv
            raise PermissionDenied
        return rv


