from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django import forms
from django.forms import ValidationError
from django.contrib.admin import widgets as admin_widgets
from django.conf import settings

from gf.gas.models.base import GASSupplierSolidalPact
from gf.base.models import Person
from gf.supplier.models import Supplier

from consts import GAS_REFERRER_SUPPLIER
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

import datetime
import logging
log = logging.getLogger(__name__)

def today():
    return datetime.date.today().strftime(settings.DATE_FMT)


class BasePactForm(forms.ModelForm):
    """Foundation form for pact management."""

    date_signed = forms.DateField(label=_lazy('Date signed'), required=True, 
        help_text=_("date of first meeting GAS - supplier"), 
        widget=admin_widgets.AdminDateWidget, initial=today
    )

#-------------------------------------------------------------------------------

class GASBasePactForm(BasePactForm):
    """Base form for pact management with GAS set.

    This cover cases:

    * Add by a GAS resource
    * Edit a Pact

    """

    pact_referrers = forms.ModelMultipleChoiceField(
        label=_lazy("Pact referrers"), 
        queryset=Person.objects.none(), required=False
    )

    def __init__(self, request, *args, **kw):
        """Set queryset for available pact referrers."""

        super(GASBasePactForm, self).__init__(*args, **kw)
        # COMMENT LF: The following "if" is just to be very precise. 
        # COMMENT LF: In fact self._gas assumes same value
        if kw.get('instance'):
            self._gas = kw['instance'].gas
        else:
            self._gas = request.resource.gas

        available_ref_people = self._gas.persons.filter(user__isnull=False)
        self.fields['pact_referrers'].queryset = available_ref_people        
        log.debug("GAS %s: available pact referrers: %s" % (self._gas, available_ref_people))

#-------------------------------------------------------------------------------

class GASAddPactForm(GASBasePactForm):
    """Form for ADDing a pact by a GAS resource"""

    def __init__(self, request, *args, **kw):
        """Set available suppliers for this GAS"""

        super(GASAddPactForm, self).__init__(request, *args, **kw)
        des = self._gas.des
        self.fields['supplier'].queryset = des.suppliers.exclude(
            pk__in=[obj.pk for obj in self._gas.suppliers]
        )

    def clean(self):
        cleaned_data = super(GASAddPactForm, self).clean()

        try:
            GASSupplierSolidalPact.objects.get(
                gas=self._gas, supplier=cleaned_data['supplier']
            )
        except GASSupplierSolidalPact.DoesNotExist:
            #ok
            pass
        else:
            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

        return cleaned_data

    def save(self):
        self.instance.gas = self._gas
        super(GASAddPactForm, self).save()

        people = self.cleaned_data.get('pact_referrers', [])
        log.debug("Selected referrers: %s" % people)
        # Set new referrers
        #TODO: refactoring needed in model (referrers_add Pact method or something better...)
        pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=self.instance)
        for p in people:
            PrincipalParamRoleRelation.objects.get_or_create(role=pr, user=p.user)

    class Meta:

        model = GASSupplierSolidalPact
        fields = ('supplier', 'date_signed', 'document', 
            'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval',
            'send_email_on_order_close',
            'order_price_percent_update'
        )

        gf_fieldsets = [(None, { 
            'fields' : (
                'supplier', 'document', 'date_signed',  
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
                'pact_referrers', 'send_email_on_order_close',
                'order_price_percent_update'
        )})]


#-------------------------------------------------------------------------------

class Supplier_PactForm(BasePactForm):
    """Form for pact management by a Supplier resource"""
    
    def __init__(self, request, *args, **kw):

        super(Supplier_PactForm, self).__init__(*args, **kw)
        self.__supplier = request.resource.supplier
        if not request.user.is_superuser:
            self.fields['gas'].queryset = request.user.person.gas_list

    def clean(self):
        cleaned_data = super(Supplier_PactForm, self).clean()
        try:
            GASSupplierSolidalPact.objects.get(
                gas=cleaned_data['gas'], supplier=self.__supplier
            )
        except GASSupplierSolidalPact.DoesNotExist:
            #ok
            pass
        else:
            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

        return cleaned_data

    def save(self):
        self.instance.supplier = self.__supplier
        return super(Supplier_PactForm, self).save()

    class Meta:

        model = GASSupplierSolidalPact
        fields = ('gas', 'date_signed', 'document', 
            'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval',
            'send_email_on_order_close'
        )

        # WARNING: no pact_referrers allowed here because we don't know the GAS
        gf_fieldsets = [(None, { 
            'fields' : [
                'gas', 'date_signed', 'document',
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval', 'send_email_on_order_close'
        ]})]
    
#-------------------------------------------------------------------------------

class EditPactForm(GASBasePactForm):
    """Form for pact editing.

    Inherit from GASPactForm because it has always "the gas" set.
    Furthermore there is no choice of suppliers because also supplier is set. 
    """

    def __init__(self, request, *args, **kw):
        """Set initial value for already set pact referrers."""

        super(EditPactForm, self).__init__(request, *args, **kw)
        self.fields['pact_referrers'].initial = self.instance.referrers_people
        self.fields['is_suspended'].label = _("Temporarily suspend")

    def save(self):

        super(EditPactForm, self).save()
        
        people = self.cleaned_data.get('pact_referrers', [])
        log.debug("Selected referrers: %s" % people)
        pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=self.instance)
        referrers_users = [p.user for p in people]

        for u in pr.get_users():
            if u not in referrers_users:
                PrincipalParamRoleRelation.objects.filter(role=pr, user=u).delete()

        for u in referrers_users:
            p, created = PrincipalParamRoleRelation.objects.get_or_create(role=pr, user=u)


    class Meta:

        model = GASSupplierSolidalPact
        fields = ('date_signed', 'document',
            'order_minimum_amount', 'order_delivery_cost', 'order_deliver_interval',
            'send_email_on_order_close',
            'is_suspended',
            'order_price_percent_update'
        )

        gf_fieldsets = [(None, { 
            'fields' : (
                'date_signed', 'document',
                ('order_minimum_amount', 'order_delivery_cost'),
                'order_deliver_interval',        
                'send_email_on_order_close',
                'pact_referrers',
                'is_suspended',
                'order_price_percent_update'
        )})]

