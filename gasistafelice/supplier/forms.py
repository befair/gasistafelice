from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.utils.functional import curry

from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.lib.fields.forms import CurrencyField
from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.supplier.models import SupplierStock, Product

class SingleSupplierStockForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    code = forms.CharField(required=False)
    product = forms.ModelChoiceField(
                            queryset = Product.objects.all(), 
                            widget = RelatedFieldWidgetCanAdd(related_model=Product)
    )
    
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

class BaseFormSetWithRequest(BaseFormSet):

    def __init__(self, request, *args, **kw):
        # This trick is needed to pass request in form constructor. Superb python!
        self.form = curry(self.form, request)
        super(BaseFormSetWithRequest, self).__init__(*args, **kw)

SingleSupplierStockFormSet = formset_factory(
                                  form=SingleSupplierStockForm, 
                                  formset=BaseFormSetWithRequest, 
                                  extra=5,
                              )

