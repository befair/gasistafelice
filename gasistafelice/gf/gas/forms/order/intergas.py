
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms

from gf.gas.forms.order.plan import AddPlannedOrderForm
from gf.gas.forms.order.base import AddOrderForm

from gf.gas.models import GAS, GASSupplierOrder, GASSupplierSolidalPact

import logging, copy

log = logging.getLogger(__name__)

#--------------------------------------------------------------------------------

class AddInterGASOrderForm(AddOrderForm):
    """Form to manage InterGAS orders.

    This works only for context resources GAS and Pact
    """

    #WAS: INTERGAS 0
    intergas = forms.BooleanField(label=_('Is this an InterGAS order?'), required=False)
    intergas_grd = forms.ModelMultipleChoiceField(
        label=_('InterGAS order with'), queryset=GAS.objects.none(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )

    #WAS: INTERGAS 1
    def __init__(self, *args, **kw):

        super(AddInterGASOrderForm, self).__init__(*args, **kw)

        pacts_count = self._pacts.count()
        self._gas = self._pacts[0].gas

        # Check needed because exception will be shown just by the end of the execution
        # of the __init__
        if pacts_count:
        
            intergas_gas_qs = self._gas.config.intergas_connection_set.all()
            if pacts_count == 1:

                #log.debug("AddOrderForm only one pact %s" % pacts)
                intergas_gas_qs = intergas_gas_qs & self._pacts[0].supplier.gas_list

        self.fields['intergas_grd'].queryset = intergas_gas_qs

    def clean(self):
        """InterGAS clean() checks for selected GAS and set _involved_extra_pacts attributes."""

        #WAS: INTERGAS 2 (rewritten. It can be factorized along with ordinary GASSupplierOrder clean)

        cleaned_data = super(AddInterGASOrderForm, self).clean()
        self._involved_extra_pacts = set()
        self._intergas_requested = cleaned_data.get('intergas')
        _involved_gas_list = cleaned_data.get('intergas_grd',[]) 
        supplier = cleaned_data['pact'].supplier

        for gas in _involved_gas_list:
            if gas != self._gas:
                log.debug("AddOrderForm intergas finding another PACT for GAS %s..." % gas)

                #retrieve the existing pact for this gas for this supplier. If exist.
                #TODO: Matteo: if not exists -> POST forged -> we should raise specific exception
                extra_pact = None
                try:
                    extra_pact = gas.pacts.get(supplier=supplier)
                    log.debug("Pact %s found." % extra_pact)
                    self._involved_extra_pacts.add(extra_pact)
                except GASSupplierSolidalPact.DoesNotExist as e:
                    #WAS: self._messages['error'].append(ugettext("Please select a gas which has a pact with the same supplier of the pact this order refers to"))
                    log.debug("Not valid InterGAS order: one or more GAS involeved do not have pacts with the same supplier")
                    raise forms.ValidationError("Not valid InterGAS order: one or more GAS involeved do not have pacts with the same supplier")
            
        if self._intergas_requested and not self._involved_extra_pacts:
            log.debug("Not valid InterGAS order: at least 2 GAS needed")
            raise forms.ValidationError("Not valid InterGAS order: at least 2 GAS needed")

        return cleaned_data

    def create_order_for_another_pact(self, other_pact):
        """This relates to InterGAS."""

        new_obj = self.instance.clone()
        new_obj.pact = other_pact

        obj = self.instance

        # retrieve the first referrer_person
        refs = other_pact.referrers_people
        if len(refs):
            log.debug("refs %s found for pact %s" % (refs, other_pact))
            new_obj.referrer_person = refs[0]
            new_obj.delivery_referrer_person = new_obj.referrer_person
            new_obj.withdrawal_referrer_person = new_obj.referrer_person
        else:
            #FIXME: 'NoneType' object has no attribute 'user'. Cannot be real. But model permitted
            #Cannot create the order.
            log.warning("no referrers for pact %s" % other_pact)

        #Delivery set to default delivery Place if gas is configured accordingly
        if obj.delivery:

            dd_place = other_pact.gas.config.default_delivery_place or \
                other_pact.gas.headquarter
            new_obj.delivery, created = Delivery.objects.get_or_create(
                    date=obj.delivery.date, place=dd_place
            )

        return new_obj

    @transaction.commit_on_success
    def save(self):

        #WAS: INTERGAS 4 (rewritten. Set correctly group_id in base order to not repeat in planned orders)

        if self._intergas_requested:
            self.instance.group_id = GASSupplierOrder.objects.get_new_intergas_group_id()

            # Create complementary InterGAS orders

            for extra_pact in self._involved_extra_pacts:
                other_intergas_order = self.create_order_for_another_pact(extra_pact)
                try:
                    other_intergas_order.save()
                    log.debug("created another intergas order: %s " % other_intergas_order)
                except Exception as e:
                    log.debug("repeat another NOT created: pact %s, start %s , end %s , delivery %s" % (
                        other_intergas_order.pact, other_intergas_order.datetime_start, other_intergas_order.datetime_end, 
                        other_intergas_order.delivery.date
                    ))
                    raise

        super(AddInterGASOrderForm, self).save()
            
    class Meta(AddOrderForm.Meta):

        #WAS: INTERGAS 6
        gf_fieldsets = copy.deepcopy(AddOrderForm.Meta.gf_fieldsets)
        gf_fieldsets[0][1]['fields'].append(('intergas', 'intergas_grd'))


class AddInterGASPlannedOrderForm(AddInterGASOrderForm, AddPlannedOrderForm):
    """Form to manage InterGAS and order planning at the same time."""

    
    @transaction.commit_on_success
    def save(self):

        AddInterGASOrderForm.save(self)
        AddPlannedOrderForm.save(self)

    class Meta(AddPlannedOrderForm.Meta):

        gf_fieldsets = copy.deepcopy(AddPlannedOrderForm.Meta.gf_fieldsets)
        gf_fieldsets[0][1]['fields'].append(('intergas', 'intergas_grd'))
