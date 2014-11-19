
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from consts import EDIT, CONFIRM, EDIT_MULTIPLE, VIEW

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from gf.gas.forms.base import SingleUserForm
from django.forms.formsets import formset_factory
from lib.formsets import BaseFormSetWithRequest

from flexi_auth.models import ObjectWithContext
from gf.base.models import Person

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "users" 
    #FIXME minor: BLOCK_DESCRIPTION = _lazy("Users")
    #FIXME minor: _lazy is appropriate, but there is probably some bug elsewhere...now use ugettext it is safe in our case
    BLOCK_DESCRIPTION = _("Users")
    BLOCK_VALID_RESOURCE_TYPES = [] #KO: because we NEED subclasses

    COLUMN_INDEX_NAME_MAP = {
        0: 'pk',
        1: 'username',
        2: 'first_name',
        3: 'last_name',
        4: 'email',
        5: 'last_login',
        6: 'date_joined',
        7: 'is_active',
        8: 'person'
    }

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
        
    def _get_resource_list(self, request):
        """Rather than adding a 'users' method to the resource,
        we compute users list here, because users may be not still bound to
        the correspondent Person. This block is in fact used only for Admin
        purposes during a specific stage of the registration process.
        """
        raise ProgrammingError("You must use a subclass to retrieve users list")


    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
            form=SingleUserForm,
            formset=BaseFormSetWithRequest, 
            extra=qs.count()   #0
        )

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        c = querySet.count()
        map_info = { }
        av = True

        for i,el in enumerate(querySet):

            key_prefix = 'form-%d' % i
            try:
                el._cached_p = el.person
            except Person.DoesNotExist as e:
                el._cached_p = None

            data.update({
               '%s-id' % key_prefix : el.pk, 
               '%s-pk' % key_prefix : el.pk,
               '%s-is_active' % key_prefix : bool(el.is_active),
               '%s-person' % key_prefix : el._cached_p,
            })

            map_info[el.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = c
        data['form-INITIAL_FORMS'] = c
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        for i, el in enumerate(querySet):

            form = formset[map_info[el.pk]['formset_index']]

            if el._cached_p:
                person = el._cached_p
                person_urn = el._cached_p.urn
            else:
                person = form['person']
                person_urn = None

            records.append({
               'id' : "%s %s" % (form['pk'], form['id']),
                'username' : el.username,
                'first_name' : el.first_name,
                'last_name' : el.last_name,
                'email' : el.email,
                'last_login' : el.last_login,
                'date_joined' : el.date_joined,
                'is_active' : form['is_active'],
                'person' : person,
                'person_urn': person_urn,
            })

        return formset, records, {}

