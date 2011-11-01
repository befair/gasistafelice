from django import forms
from django.forms.formsets import formset_factory

from flexi_auth.models import ParamRole
from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.lib.fields.forms import CurrencyField
from gasistafelice.lib.formsets import BaseFormSetWithRequest

from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import SUPPLIER_REFERRER
from gasistafelice.supplier.models import SupplierStock, Product

import logging
log = logging.getLogger(__name__)

class SingleSupplierStockForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    code = forms.CharField(required=False)
    product = forms.CharField(required=True)
#    product = forms.ModelChoiceField(
#                            queryset = Product.objects.all(), 
#                            widget = RelatedFieldWidgetCanAdd(related_model=Product)
#    )
    
    price = CurrencyField()
    availability = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(SingleSupplierStockForm, self).__init__(*args, **kw)
        self.__supplier = request.resource

    def save(self):

        if self.cleaned_data.get('id'):
            self.instance = SupplierStock.objects.get(pk=self.cleaned_data['id'])
        else:
            self.instance = SupplierStock()

        self.instance.code = self.cleaned_data.get('code')
        self.instance.supplier = self.__supplier
        self.instance.product = self.cleaned_data['product']
        self.instance.price = self.cleaned_data['price']
        self.instance.amount_available = [0, ALWAYS_AVAILABLE][self.cleaned_data.get('availability')]
        self.instance.save()

SingleSupplierStockFormSet = formset_factory(
                                  form=SingleSupplierStockForm, 
                                  formset=BaseFormSetWithRequest, 
                                  extra=5,
                              )





class EditStockForm(forms.ModelForm):

    class Meta:
        model = SupplierStock
        

#------------------------------------------------------------------------------

class SupplierRoleForm(BaseRoleForm):

    def __init__(self, request, *args, **kw):

        self._supplier = request.resource.supplier
        kw['initial'] = kw.get('initial',{}).update({
            'role' : ParamRole.get_role(SUPPLIER_REFERRER, supplier=self._supplier)
        })

        super(SupplierRoleForm, self).__init__(request, *args, **kw)

        if request.user in self._supplier.tech_referrers:
            # If user if a supplier referrer tech (i.e: gas referrer)
            self.fields['person'].queryset = \
                self.fields['person'].queryset.filter(gasmember__gas=request.user.person.gas) 



