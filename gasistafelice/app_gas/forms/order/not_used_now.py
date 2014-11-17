
def get_delivery(date, place):
    # COMMENT fero: this must be debugged since there can't be multiple
    # COMMENT fero: deliveries with the same date/place. If there are,
    # COMMENT fero: Database is corrupt
    # COMMENT fero: TO AVOID PROBLEMS IS NOT THE RIGHT SOLUTION
    try:
        obj, created = Delivery.objects.get_or_create(
            date=date,
            place=place
        )
        return obj
    except Exception as e:
        log.debug("get_delivery: %s " % (e))
        objs = Delivery.objects.filter(date=date, place=place)
        if objs and objs.count()>0:
            return objs[objs.count()-1]
        else:
            log.debug("get_delivery cannot retrieve for place: %s and date: %s" % (place, date))
            return None

#-------------------------------------------------------------------------------

def GetNewOrder(obj, other_pact):
    #new_obj = obj
    #new_obj.id = None
    new_obj = GASSupplierOrder()
    if other_pact:
        new_obj.pact = other_pact
    else:
        new_obj.pact = obj.pact

    #planning
    new_obj.root_plan = obj  #.pk
    new_obj.datetime_start = obj.datetime_start
    new_obj.datetime_end = obj.datetime_end
    if other_pact:
        log.debug("TODO GetNewOrder how to create withdrawal? %s " % other_pact)
    else:
        if obj.withdrawal:
            new_obj.withdrawal = Withdrawal.objects.create(
                    date=obj.withdrawal.date,
                    place=obj.withdrawal.place
            )
    if obj.order_minimum_amount:
        new_obj.order_minimum_amount = obj.order_minimum_amount
    if obj.delivery_cost:
        new_obj.delivery_cost = obj.delivery_cost
    if other_pact:
        #retrieve the first referrer_person
        refs = other_pact.referrers_people
        if refs and refs.count()>0:
            new_obj.referrer_person = refs[0]
        else:
            refs = other_pact.supplier_referrers_people
            if refs and refs.count()>0:
                new_obj.referrer_person = refs[0]
            else:
                #FIXME: 'NoneType' object has no attribute 'user'. Cannot be real. But model permitted
                #Cannot create the order.
                log.debug("FIXME GetNewOrder retrieve almost one referrer_person for a specific pact?")
                #FIXME: for test only
                #return None
                new_obj.referrer_person = obj.referrer_person
        new_obj.delivery_referrer_person = new_obj.referrer_person
        new_obj.withdrawal_referrer_person = new_obj.referrer_person

        #Delivery retrieve a Place. The GAS place if older orders does not exist.
        if obj.delivery:
            #TODO: look for the last order in order to retrieve the last delivery Place
            #new_obj.delivery, created = Delivery.objects.get_or_create(
            #                date=obj.delivery.date,
            #                place=other_pact.gas.headquarter
            #        )
            new_obj.delivery = get_delivery(obj.delivery.date, other_pact.gas.headquarter)

    else:
        if obj.referrer_person:
            new_obj.referrer_person = obj.referrer_person
        if obj.delivery_referrer_person:
            new_obj.delivery_referrer_person = obj.delivery_referrer_person
        if obj.withdrawal_referrer_person:
            new_obj.withdrawal_referrer_person = obj.withdrawal_referrer_person
    if obj.group_id:
        new_obj.group_id = obj.group_id
    elif other_pact:
        log.debug("GetNewOrder cannot create other intergas order without a father group_id")
        return None
    return new_obj

