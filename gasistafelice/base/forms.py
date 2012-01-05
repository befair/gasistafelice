from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base.models import Person
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

        self.fields['role'].queryset = request.resource.roles
        if not self['id'].value():
            self.fields['delete'].widget=forms.HiddenInput()

    def save(self):

        if self.cleaned_data.get('delete'):
            # HACK TODO AFTER 4th nov.
            if not self.instance.user.is_superuser:
                self.instance.user.is_staff = False

            self.instance.delete()
        else:
            self.instance.user = self.cleaned_data['person'].user

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

class EditPersonForm(forms.ModelForm):

    def __init__(self, request, *args, **kw):
        super(EditPersonForm, self).__init__(*args, **kw)

    class Meta:
        model = Person
        fields = (
            'name', 'surname', 'contact_set', 'address'
        )
        gf_fieldsets = [(None, { 
            'fields' : (
                ('name', 'surname'),  
                'address', 'contact_set'),  
        })]
