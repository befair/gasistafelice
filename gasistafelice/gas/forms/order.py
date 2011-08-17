from django import forms

from gasistafelice.gas.models.proxy import GASSupplierOrder, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

class BaseGASSupplierOrderForm(forms.ModelForm):

    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())

    def __init__(self, request, *args, **kw):
        super(BaseGASSupplierOrderForm, self).__init__(*args, **kw)
        self.fields['supplier'].queryset = request.resource.suppliers
        self.__gas = request.resource.gas

    def save(self):
        pact = GASSupplierSolidalPact.objects.get( \
            supplier=self.cleaned_data['supplier'],
            gas=self.__gas
        )
        self.instance.pact = pact
        return super(BaseGASSupplierOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ('supplier', 'date_start', 'date_end')

        gf_fieldsets = [(None, { 
            'fields' : ('supplier', ('date_start', 'date_end')) 
        })]



class GASSupplierOrderForm(BaseGASSupplierOrderForm):
    pass

#    default_close_day = models.CharField(max_length=16, blank=True, choices=DAY_CHOICES, 
#        help_text=_("default closing order day of the week")
#    )  
#    #TODO: see ticket #65
#    default_delivery_day = models.CharField(max_length=16, blank=True, choices=DAY_CHOICES, 
#        help_text=_("default delivery day of the week")
#    )  
#
#    #Do not provide default for time fields because it has no sense set it to the moment of GAS configuration
#    #TODO placeholder domthu: Default time to be set to 00:00
#    default_close_time = models.TimeField(blank=True, null=True,
#        help_text=_("default order closing hour and minutes")
#    )
#  
#    default_delivery_time = models.TimeField(blank=True, null=True,
#        help_text=_("default delivery closing hour and minutes")
#    )  
#
#    
#    use_single_delivery = models.BooleanField(default=True, 
#        help_text=_("GAS uses only one delivery place")
#    )
#
#    # Do not set default to both places because we want to have the ability
#    # to follow headquarter value if it changes.
#    # Provide delivery place and withdrawal place properties to get the right value
#    default_withdrawal_place = models.ForeignKey(Place, blank=True, null=True, related_name='gas_default_withdrawal_set', help_text=_("to specify if different from headquarter"))
#    default_delivery_place = models.ForeignKey(Place, blank=True, null=True, related_name='gas_default_delivery_set', help_text=_("to specify if different from delivery place"))
#
#    auto_select_all_products = models.BooleanField(default=True, help_text=_("automatic selection of all products bound to a supplier when a relation with the GAS is activated"))
