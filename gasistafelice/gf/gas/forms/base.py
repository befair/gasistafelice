from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, Param
from django.contrib.auth.models import User
from django.db import transaction

from lib.formsets import BaseFormSetWithRequest
from gf.base.forms import BaseRoleForm
from consts import GAS_MEMBER
from gf.gas.models import GASSupplierSolidalPact, GASMember, GAS
from gf.base.models import Person

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add

from lib.widgets import DateFormatAwareWidget, RelatedFieldWidgetCanAdd
from gf.base.forms.fields import MultiContactField

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
        # DEBUG: decomment to see how much SLOW it is! print("AAAA", self.fields)

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
        exclude = ('id_in_des',)

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
    id = forms.IntegerField(widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'readonly' : True,
        'disabled' : 'disabled',
        'class' : 'input_small',
    }))
    is_active = forms.BooleanField(required=False)
    person = forms.ModelChoiceField(required=False,
        queryset=Person.objects.filter(user__isnull=True),
        widget=RelatedFieldWidgetCanAdd(Person)
    )

    def __init__(self, request, *args, **kw):
        super(SingleUserForm, self).__init__(*args, **kw)

        #COMMENT LF: we do not need "request" parameter for the following operations
        # so it is better to put them in form class definition
        #WAS: self.fields['pk'].widget.attrs['readonly'] = True
        #WAS: self.fields['pk'].widget.attrs['disabled'] = 'disabled'
        #WAS: self.fields['pk'].widget.attrs['class'] = 'input_small'

    def clean(self):
        is_active = self.cleaned_data.get('is_active')
        person = self.cleaned_data.get('person')
        u = User.objects.get(pk=self.cleaned_data['id'])
        if is_active and not person:
            try:
                assert u.person
            except Person.DoesNotExist as e:
                raise forms.ValidationError(
                    _("You have to bind a person to the active user %s") % u
                )
        if person and person.user and (person.user != u):
            raise forms.ValidationError(
                _("Person %(person)s bound to user %(new_user)s is already bound to user %(user)s") % {
                    'person' : person, 
                    'new_user' : u, 
                    'user' : person.user
                }
            )
        self.cleaned_data['user'] = u
        return self.cleaned_data

    def save(self):

        #log.debug("Save SingleUserForm")
        u = self.cleaned_data['user']
        p = self.cleaned_data.get('person')
        try:
            if p:
                p.user = u
                p.save()
                # COMMENT matteo: now it is not necessary anymore to create GASMEMBER objects, it was
                # already done in des/forms.py DESRegistrationForm  
                # WAS:Retrieve all GAS_MEMBER ParamRoles and creates GASMember objects
                # WAS:for r in p.user.principal_param_role_set.filter(role__role__name__exact=GAS_MEMBER):
                # WAS:   GASMember.objects.get_or_create(person=p, gas=r.role.gas)
            u.is_active = self.cleaned_data.get('is_active', False)
            u.save()
        except Exception as e:
            log.debug("Save SingleUserForm error(%s)" % e)
            raise 

class GASSingleUserForm(SingleUserForm):

    gm_is_active = forms.BooleanField(required=False)
    initial_gm_is_active = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, request, *args, **kw):
        self._gas = request.resource
        super(GASSingleUserForm, self).__init__(request, *args, **kw)

    def clean(self):
        cleaned_data = super(GASSingleUserForm, self).clean()
        person = self.cleaned_data.get('person')
        gm_is_active = self.cleaned_data.get('gm_is_active', False)
        #KO: person field seems not used? 
        #KO: if gm_is_active and not person:
        #KO:    raise forms.ValidationError(_("cannot activate a GASMember not bound to a person")) 
        self.cleaned_data['gm_is_active'] = gm_is_active
        return cleaned_data

    @transaction.atomic
    def save(self):
        super(GASSingleUserForm, self).save()
        # if exception not raised
        u = self.cleaned_data['user']
        gm_is_active = self.cleaned_data['gm_is_active'] #was filled in clean if not present
        initial_gm_is_active = self.cleaned_data.get('initial_gm_is_active', False)
        
        # check if different from initial_gm_is_active
        if initial_gm_is_active != gm_is_active:
            # IMPORTANT! Search in all GASMembers!
            gm = GASMember.all_objects.get(gas=self._gas, person=u.person)   
            gm.is_suspended = not gm_is_active
            gm.save()


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

        #KO #209: can_add MUST be evaluated in form_class, not in form instance
        #KO #209: see: https://github.com/crucialfelix/django-ajax-selects/pull/29
        #KO #209: and: https://github.com/crucialfelix/django-ajax-selects/blob/master/ajax_select/admin.py#L11
        #KO #209: model = self._meta.model
        #KO #209: autoselect_fields_check_can_add(self,model,request.user)

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

    @transaction.atomic
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
