from django import forms
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base.models import Person

class BaseRoleForm(forms.ModelForm):
    """Form for role management"""
    param_role = forms.ModelChoiceField(queryset=ParamRole.objects.none())
    person = forms.ModelChoiceField(queryset=Person.objects.filter(user__isnull=False))

    def __init__(self, request, *args, **kw):
        super(BaseRoleForm, self).__init__(*args, **kw)
        params = {
            request.resource.__class__.__name__ : request.resource
        }
        self.fields['param_role'].queryset = \
            ParamRole.objects.get_param_roles.filter(role_name='', **params)

    def save(self):
        self.instance.user = self.cleaned_data['person'].user
        super(BaseRoleForm, self).save()

    class Meta:

        model = PrincipalParamRoleRelation
        fields = ('param_role',)

        gf_fieldsets = [(None, { 
            'fields' : (
                'param_role', 'person',  
        )})]

