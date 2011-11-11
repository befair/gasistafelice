from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, Param

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import GAS_MEMBER
from gasistafelice.gas.models import GASSupplierSolidalPact, GASMember

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

import logging
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

    log.debug("EditGASMemberForm")
    gm_pk = forms.IntegerField(required=False, widget=forms.HiddenInput())
    gm_name = forms.CharField(required=True, label=_("Name"), widget=forms.TextInput(attrs={'size':'100'})
    )

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


#display.Resource(name="gas", verbose_name=_("GAS")),
#display.Resource(name="person", verbose_name=_("Person")),
#membership_fee_payed,
#id_in_gas,
#models.CharField(max_length=32, name="city", verbose_name=_("City")),
#models.CharField(max_length=200, name="email", verbose_name=_("Email")),
#models.CharField(max_length=32, name="economic_state", verbose_name=_("Account")),

