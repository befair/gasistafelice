from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django import forms
from django.forms import ValidationError
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.gas.models.proxy import GASSupplierSolidalPact
from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier

from gasistafelice.auth import GAS_REFERRER_SUPPLIER
from gasistafelice.auth.models import ParamRole, PrincipalParamRoleRelation

def today():
    return datetime.date.today().strftime(settings.DATE_FMT)


class BasePactForm(forms.ModelForm):
        pass

#-------------------------------------------------------------------------------

class GAS_PactForm(BasePactForm):
    """Form for pact management by a GAS resource"""
    date_signed = forms.DateField(label=_('Date signed'), required=True, 
                    help_text=_("date of first meeting GAS - supplier"), widget=admin_widgets.AdminDateWidget, initial=today)
    gas_supplier_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)

    def __init__(self, request, *args, **kw):
        super(GAS_PactForm, self).__init__(*args, **kw)
        self._gas = request.resource.gas
        self.fields['gas_supplier_referrer'].queryset = self._gas.persons
        des = self._gas.des
        self.fields['supplier'].queryset = des.suppliers.exclude(pk__in=[obj.pk for obj in self._gas.suppliers])

    def clean(self):
        cleaned_data = super(GAS_PactForm, self).clean()

        try:
            GASSupplierSolidalPact.objects.get(gas=self._gas, supplier=cleaned_data['supplier'])
        except GASSupplierSolidalPact.DoesNotExist:
            #ok
            pass
        else:
            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

        return cleaned_data

    def save(self):
        self.instance.gas = self._gas
        super(GAS_PactForm, self).save()

        if self.cleaned_data.get('gas_supplier_referrer'):
            pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=self.instance)
            PrincipalParamRoleRelation.objects.create(role=pr, user=self.cleaned_data['gas_supplier_referrer'].user)

    class Meta:

        model = GASSupplierSolidalPact
        fields = ('supplier', 'date_signed', 
            'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval'
        )

        gf_fieldsets = [(None, { 
            'fields' : (
                'supplier', 'date_signed',  
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
                'gas_supplier_referrer',
        )})]


#-------------------------------------------------------------------------------

class Supplier_PactForm(BasePactForm):
    """Form for pact management by a Supplier resource"""
    
    document = forms.FileField(label=_("Document"), required=False, help_text=_("Document signed by GAS and Supplier"))  
        
    def __init__(self, request, *args, **kw):

        super(Supplier_PactForm, self).__init__(*args, **kw)
        self.__supplier = request.resource.supplier
        if not request.user.is_superuser:
            self.fields['gas'].queryset = request.user.person.gas_list

    def clean(self):
        cleaned_data = super(Supplier_PactForm, self).clean()
        try:
            GASSupplierSolidalPact.objects.get(gas=cleaned_data['gas'], supplier=self.__supplier)
        except GASSupplierSolidalPact.DoesNotExist:
            #ok
            pass
        else:
            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

        return cleaned_data

    def save(self):
        self.instance.supplier = self.__supplier
        return super(Supplier_PactForm, self).save()

    class Meta:

        model = GASSupplierSolidalPact
        fields = ('gas', 'date_signed', 'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval')

        gf_fieldsets = [(None, { 
            'fields' : [
                'gas', 'date_signed', 'document',
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
        ]})]
    
#-------------------------------------------------------------------------------

class EditPactForm(BasePactForm):
    """Form for pact editing.

    Support one GAS_REFERRER_SUPPLIER for each pact"""

    document = forms.FileField(label=_("Document"), required=False, help_text=_("Document signed by GAS and Supplier"))
    gas_supplier_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)

    def __init__(self, request, *args, **kw):
        self.__param_role = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=kw['instance'])
        if self.__param_role.get_users():
            kw['initial'] = kw.get('initial', {}).update({
                'gas_supplier_referrer' : self.__param_role.get_users()[0].person
            })
        super(EditPactForm, self).__init__(*args, **kw)
        self._gas = request.resource.gas
        self.fields['gas_supplier_referrer'].queryset = self._gas.persons

    def save(self):
        super(EditPactForm, self).save()
        
        #TODO placeholder seldon-dev. Replace GAS_SUPPLIER_REFERRER
        #In add stage was: PrincipalParamRoleRelation.objects.create(role=pr, user=self.cleaned_data['gas_supplier_referrer'].user)

    class Meta:

        model = GASSupplierSolidalPact
        fields = ('date_signed', 
            'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval'
        )

        gf_fieldsets = [(None, { 
            'fields' : (
                'date_signed', 'document',
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
                'gas_supplier_referrer',
        )})]

