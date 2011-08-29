from django import forms

from gasistafelice.gas.models.proxy import GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

class GAS_PactForm(forms.ModelForm):

    def __init__(self, request, *args, **kw):
        super(GAS_PactForm, self).__init__(*args, **kw)
        self.__gas = request.resource.gas

    def save(self):
        self.instance.gas = self.__gas
        return super(GAS_PactForm, self).save()

    class Meta:
        model = GASSupplierSolidalPact
        fields = ('supplier', 'date_signed', 'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval')

        gf_fieldsets = [(None, { 
            'fields' : (
                'supplier', 'date_signed', 
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
        )})]


class Supplier_PactForm(forms.ModelForm):

    def __init__(self, request, *args, **kw):
        super(Supplier_PactForm, self).__init__(*args, **kw)
        self.__supplier = request.resource.supplier
        if not request.user.is_superuser:
            self.fields['gas'].queryset = request.user.person.gas_list

    def save(self):
        self.instance.supplier = self.__supplier
        return super(Supplier_PactForm, self).save()

    class Meta:
        model = GASSupplierSolidalPact
        fields = ('gas', 'date_signed', 'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval')

        gf_fieldsets = [(None, { 
            'fields' : (
                'gas', 'date_signed', 
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
        )})]
    

