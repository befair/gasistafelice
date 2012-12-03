
from django.db.models import Max

from gasistafelice.gas.forms.order.plan import PlannedAddOrderForm


def get_group_id():
    #WARNING LF: this is not safe for concurrent requests

    _group_id = 1
    _maxs = GASSupplierOrder.objects.all().aggregate(Max('group_id'))
    log.debug("get_group_id %s " % _maxs)
    if _maxs:
        # get the maximum attribute from the first record and add 1 to it
        _group_id = _maxs['group_id__max']
        if _group_id:
            _group_id += 1
        else:
            _group_id = 1
    return _group_id

#--------------------------------------------------------------------------------

class AddInterGASPlannedOrderForm(AddPlannedOrderForm):

    #WAS: INTERGAS 0
    intergas = forms.BooleanField(label=_('Is this order InterGAS?'), required=False)
    intergas_grd = forms.ModelMultipleChoiceField(
        label=_('gas'), choices=GAS.objects.none(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )

    #WAS: INTERGAS 1
    def __init__(self, *args, **kw):

        super(AddInterGASPlannedOrderForm, self).__init__(*args, **kw)

        if pacts.count() == 1:
            #log.debug("AddOrderForm only one pact %s" % pacts)
            gas_qs = pacts[0].supplier.gas_list
        else:
            gas_qs = GAS.objects.all()

        gas_choices = gas_qs #WAS: gas_qs.values_list('pk','name')
        self.fields['intergas_grd'].choices = gas_choices

    def clean(self):
        """InterGAS clean() checks for selected GAS and set _involved_extra_pacts attributes."""

#WAS: INTERGAS 2 (rewritten. It can be factorized along with ordinary GASSupplierOrder clean)

        cleaned_data = super(AddInterGASPlannedOrderForm, self).clean()
        self._involved_extra_pacts = set()

        self._intergas_requested = cleaned_data.get('intergas')
        _involved_gas_list = cleaned_data.get('intergas_grd',[]) 

        for gas in _involved_gas_list:
            if gas != self.instance.gas:
                log.debug("AddOrderForm intergas finding another PACT for GAS %s..." % gas)

                #retrieve the existing pact for this gas for this supplier. If exist.
                #TODO: Matteo form tainted -> we should raise specific exception
                extra_pact = gas.pacts.get(supplier=self.instance.supplier)
                log.debug("Pact %s found." % extra_pact)
                self._involved_extra_pacts.add(extra_pact)
            
        if self._intergas_requested and not self._involved_extra_pacts:
            log.debug("Not valid InterGAS order: at least 2 GAS needed")
            raise form.ValidationError("Not valid InterGAS order: at least 2 GAS needed")


    def create_order_for_another_pact(self, other_pact):
        """This relates to InterGAS."""

        new_obj = self.clone_base_order()
        new_obj.pact = other_pact

        obj = self.instance

        # retrieve the first referrer_person
        refs = other_pact.referrers_people
        if refs.count():
            new_obj.referrer_person = refs[0]
            new_obj.delivery_referrer_person = new_obj.referrer_person
            new_obj.withdrawal_referrer_person = new_obj.referrer_person
        else:
            #FIXME: 'NoneType' object has no attribute 'user'. Cannot be real. But model permitted
            #Cannot create the order.
            log.debug("WARNING: no referrers for pact %s" % pact)

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

        super(AddInterGASPlannedOrderForm, self).save()
            
#LF: not needed because get_planned_orders is factorized out in model
#LF: not needed   def delete_order(self):
#
#LF: not needed        order = self.instance
#LF: not needed        #WAS: INTERGAS 3
#LF: not needed        #if InterGAS delete relative group_id others orders.
#LF: not needed        if order.group_id:
#LF: not needed            # COMMENT: do it in Models with def delete(self, *args, **kw)?
#LF: not needed            # LF: Yes
#LF: not needed            planned_intergas_orders = order.get_intergas_planned_orders()
#LF: not needed            for intergas_order in planned_intergas_orders:
#LF: not needed                log.debug("AddOrderForm delete cascade intergas_previous_planned_orders: %s" % intergas_order)
#LF: not needed                intergas_order.delete()


        for extra_pact in self._involved_extra_pacts:
            other_intergas_order = self.create_order_for_another_pact(extra_pact)
            try:
                other_intergas_order.save()
                log.debug("created another intergas order: %s " % other_order)
                _intergas_orders.add(other_order)
            except Exception as e:
                log.debug("repeat another NOT created: pact %s, start %s , end %s , delivery %s" % (
                    other_order.pact, other_order.datetime_start, other_order.datetime_end, 
                    other_order.delivery.date
                ))

#WAS: INTERGAS 5
#                        #InterGAS
#                        if _intergas_orders:
#                            for other_order in _intergas_orders:
#                                try:
#                                    other_order.datetime_start = x_obj.datetime_start
#                                    other_order.datetime_end = x_obj.datetime_end
#                                    other_order.delivery.date = x_obj.delivery.date
#                                    x_other_obj = GetNewOrder(other_order, None)
#                                    if x_other_obj:
#                                        #COMMENT domthu: Don't understand why .save() not return true?
#                                        if x_other_obj.save():
#                                            log.debug("another repeat created order: %s " % (x_other_obj))
#                                        else:
#                                            log.debug("another repeat NOT created: pact %s, start %s , end %s , delivery %s" % (x_other_obj.pact, x_other_obj.datetime_start, x_other_obj.datetime_end, x_other_obj.delivery.date))
#                                except Exception,e:
#                                    log.debug("another repeat NOT created order ERROR: %s " % (e))

        class Meta(AddPlannedOrderForm.Meta):

            #WAS: INTERGAS 6
            gf_fieldsets = AddPlannedOrderForm.gf_fieldsets
            gf_fieldsets[0][1]['fields'].append(('intergas', 'intergas_grd'))


