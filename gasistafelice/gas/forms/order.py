from django import forms

from gasistafelice.gas.models.proxy import GASSupplierOrder, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

class BaseGASSupplierOrderForm(forms.ModelForm):

    def __init__(self, request, *args, **kw):
        #Strip request arg
        super(BaseGASSupplierOrderForm, self).__init__(*args, **kw)
        if self.fields.get('delivery'):
            self.fields['delivery'].querySet = request.resource.gas.deliveries
        if self.fields.get('withdrawal'):
            self.fields['withdrawal'].querySet = request.resource.gas.withdrawals


class GASSupplierOrderForm(BaseGASSupplierOrderForm):

    supplier = forms.ModelChoiceField(queryset=Supplier.objects.none())

    def __init__(self, request, *args, **kw):
        super(GASSupplierOrderForm, self).__init__(request, *args, **kw)
        self.fields['supplier'].queryset = request.resource.suppliers
        self.__gas = request.resource.gas

    def save(self):
        pact = GASSupplierSolidalPact.objects.get( \
            supplier=self.cleaned_data['supplier'],
            gas=self.__gas
        )
        self.instance.pact = pact
        return super(GASSupplierOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ('supplier', 'date_start', 'date_end')

        gf_fieldsets = [(None, { 
            'fields' : ('supplier', ('date_start', 'date_end')) 
        })]

class EDIT_OrderForm(BaseGASSupplierOrderForm):

    class Meta:
        model = GASSupplierOrder
        fields = ['date_start', 'date_end']

        gf_fieldsets = [(None, { 
            'fields' : [('date_start', 'date_end')] 
        })]

def form_class_factory_for_request(request):
    """Return appropriate form class basing on GAS configuration
    and other request parameters if needed"""

    base_form_class = EDIT_OrderForm
    fields = EDIT_OrderForm.Meta.fields
    gf_fieldsets = EDIT_OrderForm.Meta.gf_fieldsets

    if request.resource.gas.config.can_change_delivery_place_on_each_order:
        fields.append('delivery')
        gf_fieldsets[0][1]['fields'].append('delivery')
    if request.resource.gas.config.can_change_withdrawal_place_on_each_order:
        fields.append('withdrawal')
        gf_fieldsets[0][1]['fields'].append('withdrawal')

    attrs = {}
    attrs.update(Meta=type('Meta', (), {
        'model' : GASSupplierOrder,
        'fields' : fields,
        'gf_fieldsets' : gf_fieldsets
    }))
    return type('CustomEDIT_OrderForm', (EDIT_OrderForm,), attrs)



