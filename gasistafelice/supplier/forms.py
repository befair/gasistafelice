from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.forms.formsets import formset_factory
from django.forms import ValidationError
from django.db.utils import DatabaseError

from flexi_auth.models import ParamRole
from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.lib.fields.forms import CurrencyField
from gasistafelice.lib.formsets import BaseFormSetWithRequest

from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import SUPPLIER_REFERRER
from gasistafelice.supplier.models import SupplierStock, Product, ProductPU, ProductMU, ProductCategory

from decimal import Decimal
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



#--------------------Supplier Stock-----------------------------------------------------------

class EditStockForm(forms.ModelForm):
    """Edit form for mixed-in Product and SupplierStock attributes.

    WARNIG: this form is valid only in an update-context
        """

    product_pk = forms.IntegerField(required=False, widget=forms.HiddenInput())
    product_name = forms.CharField(required=True, 
            label=_("Name"), widget=forms.TextInput(attrs={'size':'40'})
    )
    price = CurrencyField(label=_("Price (vat included)"))
    product_vat_percent = forms.IntegerField(required=True, initial=20, label=_("VAT percent"))
    availability = forms.BooleanField(required=False, label=_("Availability"))
    product_description = forms.CharField(required=False, label=_("Description"))

    product_pu = forms.ModelChoiceField(ProductPU.objects.all(), 
            label=ProductPU._meta.verbose_name, required=True)
    product_mu = forms.ModelChoiceField(ProductMU.objects.all(), required=False,
            label=ProductMU._meta.verbose_name)
    product_muppu = forms.DecimalField(label=_('Measure unit per product unit'), initial=1)

    product_category = forms.ModelChoiceField(ProductCategory.objects.all(), 
            label=ProductCategory._meta.verbose_name)
    
    def __init__(self, request, *args, **kw):
        super(EditStockForm, self).__init__(*args, **kw)
        self._supplier = request.resource.supplier
        self._product = request.resource.product
        self.fields['product_pk'].initial = self._product.pk
        self.fields['product_name'].initial = self._product.name
        self.fields['product_pu'].initial = self._product.pu
        self.fields['product_mu'].initial = self._product.mu
        self.fields['product_muppu'].initial = self._product.muppu
        self.fields['product_vat_percent'].initial = int(self._product.vat_percent*100)
        self.fields['product_category'].initial = self._product.category

        # If Supplier is not the Producer ==>
        # can't change product info!
        if self._supplier != self._product.producer:
            for k,v in self.fields.items():
                 if k.startswith('product_'):
                    self.fields[k].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = super(EditStockForm, self).clean()
        cleaned_data['supplier'] = self._supplier
        cleaned_data['amount_available'] = [0,ALWAYS_AVAILABLE][self.cleaned_data.get('availability')]
        cleaned_data['product_vat_percent'] = Decimal(cleaned_data['product_vat_percent'])/100

        #MU and PU settings must be compatible with UnitsConversion table
        pu = cleaned_data['product_pu']
        mu = cleaned_data.get('product_mu')
        mu_qs = ProductMU.objects.filter(symbol__exact=pu.symbol) 

        if mu:
            
            if mu_qs.count() == 1:
                src_mu = mu_qs[0]
                muppu = cleaned_data['product_muppu']
                if muppu != UnitsConversion.objects.get(src=src_mu, dst=mu).amount:
                    raise ValidationError(_("Units measure %(mu)s for %(pu)s must be %(amount)s") % {
                            'mu' : mu, 'pu' : pu, 'amount':muppu
                    })
                
            elif not mu_qs.count():
                pass #do nothing whatever written, it is right
            else:
                raise DatabaseError("There are more than one MU for symbol %s" % cleaned_data['pu'].symbol)
            
        else:

            if mu_qs.count() == 1:
                cleaned_data['product_mu'] = mu_qs[0]
                cleaned_data['product_muppu'] = 1
            elif not mu_qs.count():
                cleaned_data['product_mu'] = None
                cleaned_data['product_muppu'] = None
            else:
                raise DatabaseError("There are more than one MU for symbol %s" % cleaned_data['pu'].symbol)

        # Update product with new info
        for k,v in cleaned_data.items():
             if k.startswith('product_'):
                setattr(self._product, k[len('product_'):], v)

        log.debug(self._product.vat_percent)
        cleaned_data['product'] = self._product
        log.debug(self.errors)

        return cleaned_data

    def save(self):
        self.instance.product.save()
        self.instance.save()
        
    class Meta:
        model = SupplierStock
        exclude = ('supplier', 'amount_available', 'product')
        
        gf_fieldsets = (
            (None, {
                'fields': (
                    'product_name',           
                    ('price', 'product_vat_percent'),
                    ('product_pu', 'product_muppu', 'product_mu'),
                    ('units_minimum_amount', 'units_per_box'),
                    ('detail_minimum_amount', 'detail_step'), 
                    'availability',
                    ('code','product_category', 'supplier_category'),
                    'delivery_notes', 'product_pk',
                )
             }),
            )

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



