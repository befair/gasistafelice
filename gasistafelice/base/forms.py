from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base.models import Person

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
            self.instance.delete()
        else:
            self.instance.user = self.cleaned_data['person'].user
            super(BaseRoleForm, self).save()

    class Meta:

        model = PrincipalParamRoleRelation
        fields = ('role',)

        gf_fieldsets = [(None, { 
            'fields' : (
                'role', 'person',  
        )})]

