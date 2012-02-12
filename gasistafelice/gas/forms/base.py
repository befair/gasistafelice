from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, Param
from django.contrib.auth.models import User

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import GAS_MEMBER
from gasistafelice.gas.models import GASSupplierSolidalPact, GASMember

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.gas.models.base import GAS

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


class BaseGasForm(forms.ModelForm):
    pass

class AddGasForm(BaseGasForm):
    pass

class EditGasForm(BaseGasForm):
    pass
# se commento la riga sopra, e de-commento la righe sotto, si vede
# l'errore descritto nella mail
#    name = models.CharField(max_length=128, unique=True,verbose_name=_('name'))
#
#    def __init__(self, request, *args, *kw):
#        super(EditGasForm, self).__init__(*args, *kw)
#
#        model = self._meta.model
#
#    class Meta:
#        model = GAS
#        fields = (
#            'name',
#        )
