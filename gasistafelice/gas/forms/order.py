from django import forms

from gasistafelice.gas.models.proxy import GASSupplierOrder, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.gas.models import GASSupplierOrderProduct

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


#-------------------------------------------------------------------------------


class GASSupplierOrderProductForm(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(GASSupplierOrderProductForm, self).__init__(*args, **kw)
        self.__order = request.resource.order

    def save(self):

        if not self.cleaned_data.get('enabled'):
            GASSupplierOrderProduct.objects.delete(pk=self.cleaned_data['id'])


GASSupplierOrderProductFormSet = formset_factory(
                                form=GASSupplierOrderProductForm, 
                                formset=BaseFormSetWithRequest, 
                                extra=0
                          )
#-------------------------------------------------------------------------------


class SingleGASMemberOrderForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    gssop_id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    ordered_amount = forms.IntegerField(required=False)
    ordered_price = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, request, *args, **kw):
        super(SingleGASMemberOrderForm, self).__init__(*args, **kw)
        self.__gm = request.resource.gasmember

    def save(self):

        id = self.cleaned_data.get('id')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
        else:
            gssop = GASSupplierOrderProduct.objects.get(pk=self.cleaned_data.get('gssop_id'))
            gmo = GASMemberOrder(
                    order_product = gmo,
                    ordered_price = self.cleaned_data.get('ordered_price'),
                    ordered_amount = self.cleaned_data.get('ordered_amount'),
                    purchaser = self.__gm,
            )
            gmo.save()


