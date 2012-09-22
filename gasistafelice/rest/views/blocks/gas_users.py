from django.contrib.auth.models import User

from gasistafelice.rest.views.blocks import users 

from flexi_auth.models import ParamRole
from gasistafelice.consts import GAS_MEMBER

from registration.models import RegistrationProfile

from gasistafelice.gas.forms.base import GASSingleUserForm
from django.forms.formsets import formset_factory
from gasistafelice.lib.formsets import BaseFormSetWithRequest

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(users.Block):

    BLOCK_NAME = "gas_users"
    BLOCK_VALID_RESOURCE_TYPES = ["gas"]

    COLUMN_INDEX_NAME_MAP = users.Block.COLUMN_INDEX_NAME_MAP
    COLUMN_INDEX_NAME_MAP[9] = 'gm_is_active'

    def _get_resource_list(self, request):
        """Retrieve all users who are GAS Members and have confirmed their emails.

        IMPORTANT: retrieve also suspended GAS Members.
        """

        # User list
        users_email_confirmed = User.objects.filter(registrationprofile__activation_key=RegistrationProfile.ACTIVATED)
        users = users_email_confirmed.filter(person__gasmember__gas=request.resource)
        users = users.extra(select={"is_active_in_this_gas" : "NOT gas_gasmember.is_suspended" })
        # for u in users:
        #    print("%s is_active_in_this_gas=%s" % (u, u.is_active_in_this_gas))
        return users.order_by('last_name', 'first_name')

        # WAS: is a GASMember is suspended -> he has no role
        # WAS: pr = ParamRole.get_role(GAS_MEMBER, gas=request.resource)
        # WAS: users = pr.get_users()
        # WAS: return users.order_by('last_name', 'first_name')

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
            form=GASSingleUserForm,
            formset=BaseFormSetWithRequest, 
            extra=qs.count()   #0
        )

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        #TODO: refactoring needed with superclass method.

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
               '%s-gm_is_active' % key_prefix : el.is_active_in_this_gas,
               '%s-initial_gm_is_active' % key_prefix : el.is_active_in_this_gas,
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
                'is_active_in_this_gas': "%s %s" % (form['gm_is_active'], form['initial_gm_is_active'])
            })

        return formset, records, {}
