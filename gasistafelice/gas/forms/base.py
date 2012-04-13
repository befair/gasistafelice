from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, Param
from django.contrib.auth.models import User
from django.db import transaction

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import GAS_MEMBER
from gasistafelice.gas.models import GASSupplierSolidalPact, GASMember

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add

from gasistafelice.lib.widgets import DateFormatAwareWidget
from gasistafelice.base.forms.fields import MultiContactField
from gasistafelice.gas.models.base import GAS

import logging, datetime
log = logging.getLogger(__name__)

class GASRoleForm(BaseRoleForm):

    def __init__(self, request, *args, **kw):

        super(GASRoleForm, self).__init__(request, *args, **kw)
        self._gas = request.resource.gas
        self.fields['person'].queryset = \
            self._gas.persons.filter(user__isnull=False)

        # GAS Members roles are to be excluded from this management
        self.fields['role'].queryset = self.fields['role'].queryset.exclude(role__name=GAS_MEMBER)

#--------------------GAS member-----------------------------------------------------------

class EditGASMemberForm(forms.ModelForm):
    """Edit form for gas member attributes.

    WARNING: this form is valid only in an update-context
    """

    gm_pk = forms.IntegerField(required=False, widget=forms.HiddenInput())
    gm_name = forms.CharField(required=True, label=_("Name"), widget=forms.TextInput(attrs={'size':'100'}))

    def __init__(self, request, *args, **kw):
        super(EditGASMemberForm, self).__init__(*args, **kw)
        self._gasmember = request.resource.gasmember
        self.fields['gm_name'].initial = self._gasmember.person.name

    def clean(self):
        cleaned_data = super(EditGASMemberForm, self).clean()
        cleaned_data['gasmember'] = self._gasmember
        log.debug(self.errors)
        return cleaned_data

    def save(self):
        self.instance.gasmember.save()
        self.instance.save()

    class Meta:
        model = GASMember
        exclude = ('id_in_des')

        gf_fieldsets = (
            (None, {
                'fields': (
                    'gm_name',
                    ('person', 'membership_fee_payed'),
                    ('person_city', 'person_email'),
                    'id_in_gas',
                )
             }),
            )



#--------------------User-----------------------------------------------------------

class SingleUserForm(forms.Form):

    #For editing
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False)
    is_active = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(SingleUserForm, self).__init__(*args, **kw)
        instance = getattr(self, 'instance', None)
        self.fields['pk'].widget.attrs['readonly'] = True
        self.fields['pk'].widget.attrs['disabled'] = 'disabled'
        self.fields['pk'].widget.attrs['class'] = 'input_small'
        self.__supplier = request.resource

    def save(self):

        log.debug("Save SingleUserForm")
        if self.cleaned_data.get('id'):
            ss = User.objects.get(pk=self.cleaned_data['id'])
            #log.debug("Save SingleUserForm id_ss(%s)" % (ss.pk))
            try:
                ss.is_active = self.cleaned_data.get('is_active')
                ss.save()
            except Exception, e:
                raise
                log.debug("Save SingleUserForm error(%s)" %  str(e))
                Exception("Save SingleUserForm error: %s", str(e))
        else:
            #do not create users here!
            #ss = User()
            log.debug("New SingleUserForm")

#class GASSingleUserForm(SingleUserForm):

#    def __init__(self, request, *args, **kw):
#        super(GASSingleUserForm, self).__init__(*args, **kw)

#class SupplierSingleUserForm(SingleUserForm):

#    def __init__(self, request, *args, **kw):
#        super(SupplierSingleUserForm, self).__init__(*args, **kw)


class BaseGASForm(forms.ModelForm):


    headquarter = make_ajax_field(GAS, 
        label = _("headquarter").capitalize(),
        model_fieldname='headquarter',
        channel='placechannel', 
        help_text=_("Search for place by name, by address, or by city")
    )
    contact_set = MultiContactField(n=2,label=_('Contacts'))

    birthday = forms.DateField(initial=datetime.date.today, required=True
        , label = _("birthday").capitalize()
        , widget=DateFormatAwareWidget
    )

    def __init__(self, request, *args, **kw):
        super(BaseGASForm, self).__init__(*args, **kw)

        model = self._meta.model
        autoselect_fields_check_can_add(self,model,request.user)

        #TODO: fero to refactory and move in GF Form baseclass...
        self._messages = {
            'error' : [],
            'info' : [],
            'warning' : [],
        }

    def write_down_messages(self):
        """Used to return messages related to form.

        Usually called:
        * in request.method == "GET"
        * when it is "POST" but form is invalid
        """

        # Write down messages only if we are GETting the form
        for level, msg_list in self._messages.items():
            for msg in msg_list:
                getattr(messages, level)(self.request, msg)

    @transaction.commit_on_success
    def save(self, *args, **kw):
        """Save related objects and then save model instance"""


        for contact in self.cleaned_data['contact_set']:

            if contact.value:
                contact.save()
            elif contact.pk:
                self.cleaned_data['contact_set'].remove(contact)

        return super(BaseGASForm, self).save(*args, **kw)

    class Meta:
        model = GAS
        fields = (
            'description', 'name','id_in_des','birthday','headquarter','contact_set',
            'logo','association_act','intent_act', 'membership_fee'
        )
        gf_fieldsets = [(None, {
            'fields' : (
                'name','id_in_des','birthday','headquarter', 'membership_fee', 
                'contact_set','logo', 'description', 'association_act','intent_act'
            ),
        })]

class AddGASForm(BaseGASForm):
    pass

class EditGASForm(BaseGASForm):
    pass
