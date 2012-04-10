from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.forms.formsets import formset_factory
from django.forms import ValidationError
from django.db.utils import DatabaseError
from django.db import transaction

from flexi_auth.models import ParamRole
from gasistafelice.lib.widgets import RelatedFieldWidgetCanAdd
from gasistafelice.lib.fields.forms import CurrencyField
from gasistafelice.lib.formsets import BaseFormSetWithRequest

from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import SUPPLIER_REFERRER
from gasistafelice.supplier.models import SupplierStock, Product, \
    ProductPU, ProductMU, ProductCategory, \
    UnitsConversion, Supplier

from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add

from gasistafelice.base.forms.fields import MultiContactField


from decimal import Decimal
import logging
log = logging.getLogger(__name__)


#--------------------Supplier Stock-----------------------------------------------------------

class SingleSupplierStockForm(forms.Form):

    #For editing
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False)
    #code = forms.CharField(required=False)
    product = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'size':'85'}), 
        max_length=200
    )
#    description = forms.CharField(required=False, widget=forms.TextInput(), max_length=500)
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
#        self.fields['product'].widget.attrs['class'] = 'input_medium'
#        self.fields['description'].widget.attrs['class'] = 'input_long'
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
#                prd.description = self.cleaned_data['description']
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
                raise
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

    product_name = forms.CharField(required=True, 
            label=_("Name"), widget=forms.TextInput(attrs={'size':'40'},), max_length=200
    )
    price = CurrencyField(label=_("Price (vat included)"))
    product_vat_percent = forms.IntegerField(required=True, initial=20, label=_("VAT percent"))
    availability = forms.BooleanField(required=False, label=_("Availability"))
    product_description = forms.CharField(required=False, label=_("Description"), widget=forms.TextInput(), max_length=500)

    product_pu = forms.ModelChoiceField(ProductPU.objects.all(), 
        label=_("Package"), required=True
    )
    product_mu = forms.ModelChoiceField(ProductMU.objects.all(), required=False,
        label=_("Units")
    )
    product_muppu = forms.DecimalField(label=_('of'), initial=1,
        min_value = Decimal('0.01'), max_value = Decimal('10000')
    )

    product_category = forms.ModelChoiceField(ProductCategory.objects.all(), 
            label=ProductCategory._meta.verbose_name)
    
    def __init__(self, request, *args, **kw):
        super(EditStockForm, self).__init__(*args, **kw)
        self._supplier = request.resource.supplier
        self._product = request.resource.product
        self.fields['product_name'].initial = self._product.name
        self.fields['product_name'].widget.attrs['class'] = 'input_medium'
        self.fields['product_description'].widget.attrs['class'] = 'input_long'
        self.fields['product_pu'].initial = self._product.pu
        self.fields['product_mu'].initial = self._product.mu
        self.fields['product_muppu'].initial = self._product.muppu
        self.fields['product_vat_percent'].initial = int(self._product.vat_percent*100)
        self.fields['product_category'].initial = self._product.category
        self.fields['availability'].initial = bool(request.resource.amount_available)

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

        # Update product with new info
        for k,v in cleaned_data.items():
             if k.startswith('product_'):
                setattr(self._product, k[len('product_'):], v)

        log.debug(self._product.vat_percent)
        cleaned_data['product'] = self._product
        log.debug(self.errors)

        return cleaned_data

    def save(self):
        log.debug("Saving updated product: %s" % self.instance.__dict__)
        log.debug("cleaned data = %s" % self.cleaned_data)
        product = self.cleaned_data['product']
        product.save()
        self.instance.product = product
        self.instance.amount_available = self.cleaned_data['amount_available']
        self.instance.save()
        
    class Meta:
        model = SupplierStock
        exclude = ('supplier', 'amount_available', 'product')
        
        gf_fieldsets = (
            (None, {
                'fields': (
                    'product_name',
                    'product_description',
                    ('price', 'product_vat_percent'),
                    'product_category',
                )
             }),
             (_("Distribution info"), {
                'fields' : (
                    ('product_pu', 'product_muppu', 'product_mu'),
                    ('units_minimum_amount', 'units_per_box'),
                    ('detail_minimum_amount', 'detail_step'), 
                    'availability',
                )
             }),
             (_("Supplier info"), {
                'fields' : (
                    ('code', 'supplier_category'),
                )
             })
            )

class AddStockForm(EditStockForm):
    """Add new product and stock"""
    # TODO: refactory with EditStockForm / BaseStockForm nedeed

    def __init__(self, request, *args, **kw):

        #AAA: super(EditStockForm IS RIGHT! Leave it here pls
        super(EditStockForm, self).__init__(*args, **kw)
        self._supplier = request.resource.supplier
        self._product = Product()
        self.fields['product_name'].widget.attrs['class'] = 'input_medium'
        self.fields['product_description'].widget.attrs['class'] = 'input_long'
        self.fields['product_vat_percent'].initial = 21
        self.fields['availability'].initial = True

#        # If Supplier is not the Producer ==>
#        # can't change product info!
#        if self._supplier != self._product.producer:
#            for k,v in self.fields.items():
#                 if k.startswith('product_'):
#                    self.fields[k].widget.attrs['disabled'] = 'disabled'

    def clean(self):

        #AAA fero: super(EditStockForm IS RIGHT! Leave it here pls
        cleaned_data = super(EditStockForm, self).clean()
        cleaned_data['supplier'] = self._supplier
        cleaned_data['amount_available'] = [0,ALWAYS_AVAILABLE][self.cleaned_data.get('availability')]
        cleaned_data['product_vat_percent'] = Decimal(cleaned_data['product_vat_percent'])/100

        #MU and PU settings must be compatible with UnitsConversion table
        if cleaned_data.get('product_pu'):
            # Some other checks that can be performed only if 'product_pu' is set
            pu = cleaned_data['product_pu']
            mu = cleaned_data.get('product_mu')
            mu_qs = ProductMU.objects.filter(symbol__exact=pu.symbol) 

            # Update product with new info
            for k,v in cleaned_data.items():
                 if k.startswith('product_'):
                    setattr(self._product, k[len('product_'):], v)

            log.debug(self._product.vat_percent)
            cleaned_data['product'] = self._product
        log.debug(self.errors)

        return cleaned_data

    def save(self):
        log.debug("Saving new product:")
        log.debug("cleaned data = %s" % self.cleaned_data)
        product = self.cleaned_data['product']
        product.producer = self._supplier
        product.save()

        stock = SupplierStock(
            product = product,
            price = self.cleaned_data['price'],
            units_minimum_amount = self.cleaned_data['units_minimum_amount'],
            units_per_box = self.cleaned_data['units_per_box'],
            detail_minimum_amount = self.cleaned_data['detail_minimum_amount'],
            detail_step = self.cleaned_data['detail_step'],
            supplier = self._supplier,
            code = self.cleaned_data.get('code'),
            amount_available = self.cleaned_data['amount_available'],
            supplier_category = self.cleaned_data.get('supplier_category')
        )
        stock.save()
        

#------------------------------------------------------------------------------

# LF: this is not used anymore. Binding users to Supplier role happens in Supplier --> Admin

#WAS: class SupplierRoleForm(BaseRoleForm):
#WAS: 
#WAS:     def __init__(self, request, *args, **kw):
#WAS: 
#WAS:         self._supplier = request.resource.supplier
#WAS:         kw['initial'] = kw.get('initial',{}).update({
#WAS:             'role' : ParamRole.get_role(SUPPLIER_REFERRER, supplier=self._supplier)
#WAS:         })
#WAS: 
#WAS:         super(SupplierRoleForm, self).__init__(request, *args, **kw)
#WAS: 
#WAS:         if request.user in self._supplier.tech_referrers:
#WAS:             # If user if a supplier referrer tech (i.e: gas referrer)
#WAS:             self.fields['person'].queryset = \
#WAS:                 self.fields['person'].queryset.filter(gasmember__gas=request.user.person.gas) 


#-------------------------------------------------------------------------------


class SupplierForm(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        log.debug("Create SupplierForm")
        super(SupplierForm, self).__init__(*args, **kw)

    #@transaction.commit_on_success
    def save(self):

        #log.debug("Save SupplierForm")
        id = self.cleaned_data.get('id')
        log.debug("Save SupplierForm id(%s)" % id)
        if id:
            enabled = self.cleaned_data.get('enabled')
            #log.debug("Save SupplierForm enabled(%s)" % enabled)
            #TODO: Suspend all pact related to this producer
            #if not enabled:

            self.instance.save()



#-------------------------------------------------------------------------------

class BaseSupplierForm(forms.ModelForm):


    seat = make_ajax_field(Supplier, 
        label = _("seat"),
        model_fieldname='seat',
        channel='placechannel', 
        help_text=_("Search for place by name, by address, or by city")
    )
    contact_set = MultiContactField(n=3,label=_('Contacts'))


    def __init__(self, request, *args, **kw):
        super(BaseSupplierForm, self).__init__(*args, **kw)

        model = self._meta.model
        autoselect_fields_check_can_add(self,model,request.user)

        #TODO: fero to refactory and move in GF Form baseclass...
        self._messages = {
            'error' : [],
            'info' : [],
            'warning' : [],
        }

    def write_down_messages(self):
        """Used to return messages related to form.

        Usually called:
        * in request.method == "GET"
        * when it is "POST" but form is invalid
        """

        # Write down messages only if we are GETting the form
        for level, msg_list in self._messages.items():
            for msg in msg_list:
                getattr(messages, level)(self.request, msg)

    @transaction.commit_on_success
    def save(self, *args, **kw):
        """Save related objects and then save model instance"""


        for contact in self.cleaned_data['contact_set']:

            if contact.value:
                contact.save()
            elif contact.pk:
                self.cleaned_data['contact_set'].remove(contact)

        return super(BaseSupplierForm, self).save(*args, **kw)


    class Meta:
        model = Supplier
        fields = (
            'name', 'seat', 'website', 'contact_set', 'logo', 'flavour','vat_number','certifications'
        )
        gf_fieldsets = [(None, {
            'fields' : (
                'name','seat', 'website', 'contact_set', 'logo','flavour', 'vat_number','certifications'
            )
        })]

class AddSupplierForm(BaseSupplierForm):
    pass

class EditSupplierForm(BaseSupplierForm):
    pass
