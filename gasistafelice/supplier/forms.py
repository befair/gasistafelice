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


#--------------------Supplier Stock-----------------------------------------------------------

class SingleSupplierStockForm(forms.Form):

    #For editing
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False)
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
        self.fields['pk'].widget.attrs['readonly'] = True
        self.fields['pk'].widget.attrs['disabled'] = 'disabled'
        self.fields['pk'].widget.attrs['class'] = 'input_small'
        self.fields['product'].widget.attrs['class'] = 'input_medium'
        self.fields['description'].widget.attrs['class'] = 'input_long'
        self.fields['price'].widget.attrs['class'] = 'input_short taright'
        self.__supplier = request.resource

#    def clean_id(self):
#        return instance.id

    def save(self):

        #log.debug("Save SingleSupplierStockForm")
        if self.cleaned_data.get('id'):
            ss = SupplierStock.objects.get(pk=self.cleaned_data['id'])
            #prd = Product.objects.get(pk=ss.product.pk)
            prd = ss.product
            log.debug("Save SingleSupplierStockForm id_ss(%s) id_prd(%s)" % (ss.pk, prd.pk))
            try:
                #ss.code = self.cleaned_data.get('code')
                #ss.supplier = self.__supplier
                prd.name = self.cleaned_data['product']
                prd.description = self.cleaned_data['description']
                prd.save()
                #"SupplierStock.product" must be a "Product" instance
                #ss.product = self.cleaned_data['product']
                #ss.product.description = self.cleaned_data['description']
                old_price = ss.price
                ss.price = self.cleaned_data['price']
                if old_price != ss.price:
                    #CASCADING price has changed
                    log.debug("Save SingleSupplierStockForm price changed old(%s) new(%s)" % (old_price, ss.price))
                old_amount = ss.amount_available
                ss.amount_available = [0, ALWAYS_AVAILABLE][self.cleaned_data.get('availability')]
                if old_amount != ss.amount_available:
                    #CASCADING product availability has changed
                    log.debug("Save SingleSupplierStockForm product availability has changed old(%s) new(%s)" % (old_amount, ss.amount_available))
                ss.save()
            except Exception, e:
                log.debug("Save SingleSupplierStockForm error(%s)" %  str(e))
                Exception("Save SingleSupplierStockForm error: %s", str(e))
        else:
            #do not create suppliers stock here!
            #ss = SupplierStock()
            log.debug("New SingleSupplierStockForm")

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



