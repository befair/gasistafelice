from django import forms
from django.forms.formsets import formset_factory

from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.lib.fields.forms import CurrencyField
from gasistafelice.lib.formsets import BaseFormSetWithRequest

from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.supplier.models import SupplierStock, Product

import logging
log = logging.getLogger(__name__)

class SingleSupplierStockForm(forms.Form):

    #For editing
    #id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    id = forms.IntegerField(required=False)
    #code = forms.CharField(required=False)
    product = forms.CharField(required=True, widget=forms.TextInput(), max_length=200)
    description = forms.CharField(required=False, widget=forms.TextInput(), max_length=500)
#    product = forms.ModelChoiceField(
#                            queryset = Product.objects.all(), 
#                            widget = RelatedFieldWidgetCanAdd(related_model=Product)
#    )
    
    price = CurrencyField()
    availability = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(SingleSupplierStockForm, self).__init__(*args, **kw)
        instance = getattr(self, 'instance', None)
        #if instance and instance.id:
        #    self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget.attrs['disabled'] = 'disabled'
        self.fields['id'].widget.attrs['class'] = 'input_small'
        self.fields['product'].widget.attrs['class'] = 'input_medium'
        self.fields['description'].widget.attrs['class'] = 'input_long'
        self.fields['price'].widget.attrs['class'] = 'input_short taright'
        self.__supplier = request.resource

    def clean_id(self):
        return self.instance.id

    def save(self):

        if self.cleaned_data.get('id'):
            self.instance = SupplierStock.objects.get(pk=self.cleaned_data['id'])
            log.debug("Save SingleSupplierStockForm id(%s)" % self.instance.pk)
        else:
            self.instance = SupplierStock()
            log.debug("New SingleSupplierStockForm")

        try:
            #self.instance.code = self.cleaned_data.get('code')
            self.instance.supplier = self.__supplier
            self.instance.product = self.cleaned_data['product']
            self.instance.product.description = self.cleaned_data['description']
            self.instance.price = self.cleaned_data['price']
            self.instance.amount_available = [0, ALWAYS_AVAILABLE][self.cleaned_data.get('availability')]
            self.instance.product.save()
            self.instance.save()
        except Exception, e:
            log.debug("Save SingleSupplierStockForm error(%s)" %  str(e))
            Exception("Save SingleSupplierStockForm error: %s", str(e))

SingleSupplierStockFormSet = formset_factory(
                                  form=SingleSupplierStockForm, 
                                  formset=BaseFormSetWithRequest, 
                                  extra=5,
                              )

