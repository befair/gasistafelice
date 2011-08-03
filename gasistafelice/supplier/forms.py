from django import forms
from django.forms.formsets import formset_factory

from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.supplier.models import SupplierStock, Product

class SingleSupplierStockForm(forms.Form):

    code = forms.CharField(required=False)
    product = forms.ModelChoiceField(
                            queryset = Product.objects.all(), 
                            widget = RelatedFieldWidgetCanAdd(related_model=Product)
    )
    
    price = forms.DecimalField(min_value=0, decimal_places=2)
    availability = forms.BooleanField()


SingleSupplierStockFormSet = formset_factory(SingleSupplierStockForm, extra=5)

