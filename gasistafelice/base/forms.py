from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base.models import Person

class BaseRoleForm(forms.ModelForm):
    """Form for role management"""
    role = forms.ModelChoiceField(queryset=ParamRole.objects.none(), label=_("Role"))
    person = forms.ModelChoiceField(queryset=Person.objects.filter(user__isnull=False), label=_("Person"))

    delete = forms.BooleanField(label=_("delete"), required=False)

    def __init__(self, request, *args, **kw):
        super(BaseRoleForm, self).__init__(*args, **kw)
        params = {
            request.resource.__class__.__name__ : request.resource
        }
        self.fields['role'].queryset = request.resource.roles

    def save(self):

        if self.cleaned_data['delete']:
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

