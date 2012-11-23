from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.db import transaction
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add

from gasistafelice.base.forms.fields import MultiContactField
from gasistafelice.lib.widgets import (
    RelatedFieldWidgetCanAdd, RelatedMultipleFieldWidgetCanAdd
)
from gasistafelice.base.models import Person, Place, Contact
from gasistafelice.consts import GAS_REFERRER_TECH

class BaseRoleForm(forms.ModelForm):
    """Form for role management"""

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    person = forms.ModelChoiceField(queryset=Person.objects.filter(user__isnull=False), label=_("Person"))
    delete = forms.BooleanField(label=_("delete"), required=False)

    def __init__(self, request, *args, **kw):
        pk = kw['data'].get("%s-id" % kw['prefix'])
        if pk:
            kw['instance'] = PrincipalParamRoleRelation.objects.get(pk=pk)

        super(BaseRoleForm, self).__init__(*args, **kw)

        if self['id'].value() and self['role'].value() != '':
            self.fields['role'].queryset = request.resource.roles.filter(pk=self['role'].value())
        else:
            self.fields['role'].queryset = request.resource.roles

#        if self['id'].value() and self['person'].value() != '':
#            self.fields['person'].queryset = self.fields['person'].queryset.filter(pk=self['person'].value())

        if not self['id'].value():
            self.fields['delete'].widget=forms.HiddenInput()

    def save(self):
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        if self.cleaned_data.get('delete'):
            # HACK TODO AFTER 4th nov.
            if not self.instance.user.is_superuser:
                self.instance.user.is_staff = False

            self.instance.delete()
        else:

            if (self.cleaned_data.get('id') is None or self.cleaned_data.get('id') == '') \
                and self.cleaned_data['person'] != '' \
                and self.cleaned_data['role'] != '':

                self.instance.user = self.cleaned_data['person'].user

                #COMMENT domthu: No
                self.instance.user.is_active = True

                # HACK TODO AFTER 4th nov.
                if self.cleaned_data['role'].role.name == GAS_REFERRER_TECH:
                    self.instance.user.is_staff = True
                self.instance.user.save()

                super(BaseRoleForm, self).save()

    class Meta:

        model = PrincipalParamRoleRelation
        fields = ('role',)

        gf_fieldsets = [(None, {
            'fields' : (
                'role', 'person',
        )})]

#--------------------------------------------------------------------------------

class BasePersonForm(forms.ModelForm):

    address = make_ajax_field(Person,
        label = _("address"),
        model_fieldname='address',
        channel='placechannel',
        help_text=_("Search for place by name, by address, or by city")
    )
    contact_set = MultiContactField(n=3,label=_('Contacts'))

    def __init__(self, request, *args, **kw):
        super(BasePersonForm, self).__init__(*args, **kw)

        model = self._meta.model
        autoselect_fields_check_can_add(self,model,request.user)

    @transaction.commit_on_success
    def save(self, *args, **kw):
        """Save related objects and then save model instance"""

        for contact in self.cleaned_data['contact_set']:
            if contact.value:
                contact.save()
            elif contact.pk:
                self.cleaned_data['contact_set'].remove(contact)

        return super(BasePersonForm, self).save(*args, **kw)

    class Meta:
        model = Person
        fields = (
            'name', 'surname','display_name', 'contact_set',
            'avatar','website', 'address'
        )
        gf_fieldsets = [(None, {
            'fields' : (
                ('name', 'surname'),
                'display_name',
                'address', 'contact_set',
                'avatar','website'),
        })]

class EditPersonForm(BasePersonForm):
    pass

class AddPersonForm(BasePersonForm):
    pass
