
from django.db.models import Max

from gasistafelice.gas.forms.order.plan import PlannedAddOrderForm


def get_group_id():
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

        #WAS: INTERGAS 2
        # InterGAS
        _intergas_pacts = None
        _intergas_number = None
        _intergas = self.cleaned_data.get('intergas')
        if _intergas:

            # InterGAS gas list
            _intergas_gas_list = self.cleaned_data.get('intergas_grd') or []

            if _intergas_gas_list:
                #Add the default order's gas in the list
                _intergas_pacts = set() #GAS.objects.none()
                #_intergas_pacts.add(self.instance.pact)
                for gas in _intergas_gas_list:
                    if gas != self.instance.gas:
                        log.debug("AddOrderForm intergas finding another PACT for GAS %s..." % gas)

                        #retrieve the existing pact for this gas for this supplier. If exist.
                        extra_pact = gas.pacts.get(supplier=self.instance.supplier)
                        log.debug("Pact %s found." % extra_pact)
                        _intergas_pacts.add(extra_pact)

                if _intergas_pacts:
                    _intergas_number = get_group_id()
                    #Set instance as InterGAS
                    self.instance.group_id = _intergas_number
                else:
                    log.debug("Not valid InterGAS almost 2 GAS to be an interGAS's order")


            _intergas_orders = set()
            if _intergas_pacts and _intergas_number:
                log.debug("AddOrderForm interGAS OPEN for other GAS")
                #Repeat this order for the overs GAS
                for other_pact in _intergas_pacts:
                    other_order = GetNewOrder(self.instance, other_pact)
                    try:
                        other_order.save()
                        log.debug("repeat created another order: %s " % (other_order))
                        _intergas_orders.add(other_order)
                    except Exception as e:
                        log.debug("repeat another NOT created: pact %s, start %s , end %s , delivery %s" % (
                            other_order.pact, other_order.datetime_start, other_order.datetime_end, 
                            other_order.delivery.date
                        ))

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



#TODO: delete cascading in model

        #WAS: INTERGAS 3
#        #if InterGAS delete relative group_id others orders.
#        if order.group_id and order.group_id > 0:
#            # COMMENT: do it in Models with def delete(self, *args, **kw)?
#            # LF: Yes
#            planed_intergas_orders = GASSupplierOrder.objects.filter(group_id=order.group_id)
#            if planed_intergas_orders and planed_intergas_orders.count() >0:
#                for intergas_order in planed_intergas_orders:
#                    log.debug("AddOrderForm repeat delete intergas_previous_planed_orders: %s" % (intergas_order))
#                    intergas_order.delete()
#WAS: INTERGAS 4
#                    #get new interGAS number if needed
#                    if _intergas_orders:
#                        x_obj.group_id = get_group_id()
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
#WAS: INTERGAS 6
#                            , ('intergas', 'intergas_grd')


