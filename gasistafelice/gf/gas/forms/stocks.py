from django import forms
from django.forms.formsets import formset_factory

from lib.widgets import RelatedFieldWidgetCanAdd
from lib.fields.forms import CurrencyField
from lib.formsets import BaseFormSetWithRequest

from gf.base.const import ALWAYS_AVAILABLE
from gf.gas.models.base import GASSupplierStock
from gf.supplier.models import SupplierStock, Product

import logging
log = logging.getLogger(__name__)


#----------------------GAS Stock---------------------------------------------------------

class GASSupplierStockForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(GASSupplierStockForm, self).__init__(*args, **kw)
        #instance = getattr(self, 'instance', None)
        #if instance and instance.id:
        #    self.fields['id'].widget.attrs['readonly'] = True
        self.fields['pk'].widget.attrs['readonly'] = True
        self.fields['pk'].widget.attrs['disabled'] = 'disabled'
        self.fields['pk'].widget.attrs['class'] = 'input_small'
        self.__pact = request.resource.pact

    def save(self):
        log.debug("Save GASSupplierStockForm")
        if self.cleaned_data.get('id'):
            gasstock = GASSupplierStock.objects.get(pk=self.cleaned_data['id'])
            try:
                gasstock.enabled = self.cleaned_data.get('enabled', False)
                gasstock.save()
            except Exception, e:
                raise
                log.debug("Save SingleSupplierStockForm error(%s)" %  str(e))
                Exception("Save SingleSupplierStockForm error: %s", str(e))

GASSupplierStockFormSet = formset_factory(
                                form=GASSupplierStockForm,
                                formset=BaseFormSetWithRequest,
                                extra=0 #must be 0 no add form
                          )

