"""
Order module has been split for its complexity.
Proposed clean hierarchy for GASSupplierOrder that
can be used in many contexts such as:

    DES:             ChooseSupplier  ChooseGAS ChooseReferrer
    GAS:             ChooseSupplier  OneGAS    ChooseReferrer
    Supplier:        OneSupplier     ChooseGAS ChooseReferrer
    Solidal Pact:    OneSupplier     OneGAS    ChooseReferrer

* BaseOrderForm: base for add and edit
|
|---* AddOrderForm: encapsulate Add logic.
|         Just this class is enough if Resource API encapsulate
|         logic behind specific resource. Otherwise we need to write
|         subclasses XAddOrderForm where X is one of DES, GAS, Supplier, Pact.
|
|        It manages:
|        * common attributes
|        * setting of withdrawal and deliveries
|   
----* EditOrderForm

* PlannedAddOrderForm: mix-in class to add planning facilities

#TODO LEFT OUT NOW InterGASAddOrderForm: it requires some considerations and
#TODO LEFT OUT NOW     so probably it should be managed as a separated module.
#TODO LEFT OUT NOW     P.e: deliveries and withdrawals MUST be always specified.
#TODO LEFT OUT NOW     It also would need multiple delivery and withdrawal places,
#TODO LEFT OUT NOW     but this will be a FUTURE module update
    
Factory function `form_class_factory_for_request` is there for:
    * composition of final classes 
        (XAddOrderForm, PlannedAddOrderForm, InterGASAddOrderForm) 
    * follows GAS configuration options and prepare delivery and withdrawal fields

Where can you find above classes:

    * base.BaseOrderForm
    * base.AddOrderForm
    * base.EditOrderForm
    * X.XAddOrderForm (where X can be des,gas,supplier,pact)
    * __init__.form_class_factory_for_request
    * extra.PlannedAddOrderForm
#TODO LEFT OUT NOW    * intergas.InterGASAddOrderForm

There are also some other classes that support order interactions:
    * gmo.SingleGASMemberOrderForm
    * gmo.BasketGASMemberOrderForm
    * gsop.GASSupplierOrderProductForm
"""
 
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.gas.models import ( GAS, GASSupplierOrder,
            Delivery, Withdrawal
)

from gasistafelice.supplier.models import Supplier
from gasistafelice.base.models import Place, Person

from django.db import transaction
from django.db.models import Max
from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets
from django.core.exceptions import ValidationError, PermissionDenied

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base import const
from gasistafelice.exceptions import DatabaseInconsistent
from gasistafelice.utils import datetime_round_ten_minutes

from django.conf import settings

import copy
from datetime import timedelta, datetime, date

import logging
log = logging.getLogger(__name__)

FREQUENCY = [ 
    ('7', _('week')), 
    ('14', _('two weeks')), 
    ('21', _('three weeks')), 
    ('28', _('monthly')), 
    ('56', _('two months')), 
    ('84', _('three months')), 
    ('168', _('half year')), 
    ('336', _('year'))
]

def get_day_from_choice(choice):
    day_num = 0
    if choice == 'MONDAY':
        day_num = 0
    elif choice == 'TUESDAY':
        day_num = 1
    elif choice == 'WEDNESDAY':
        day_num = 2
    elif choice == 'THURSDAY':
        day_num = 3
    elif choice == 'FRIDAY':
        day_num = 4
    elif choice == 'SATURDAY':
        day_num = 5
    elif choice == 'SUNDAY':
        day_num = 6
    return day_num

def first_day_on_or_after(daynum, dt):
    days_to_go = daynum - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt

#-------------------------------------------------------------------------------

def GetNewOrder(obj, other_pact):
    #new_obj = obj
    #new_obj.id = None
    new_obj = GASSupplierOrder()
    if other_pact:
        new_obj.pact = other_pact
    else:
        new_obj.pact = obj.pact

    #planification
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

def get_delivery(date, place):
    try:
        obj, created = Delivery.objects.get_or_create(
                date=date,
                place=place
        )
        return obj
    except Exception,e:
        log.debug("get_delivery: %s " % (e))
        objs = Delivery.objects.filter(date=date, place=place)
        if objs and objs.count()>0:
            return objs[objs.count()-1]
        else:
            log.debug("get_delivery cannot retrieve for place: %s and date: %s" % (place, date))
            return None

def form_class_factory_for_request(request, base):
    """Return appropriate form class basing on GAS configuration
    and other request parameters if needed"""

    #log.debug("OrderForm--> form_class_factory_for_request")
    fields = copy.deepcopy(base.Meta.fields)
    gf_fieldsets = copy.deepcopy(base.Meta.gf_fieldsets)
    attrs = {}
    gas = request.resource.gas

    if gas:

        if gas.config.use_withdrawal_place:
            gf_fieldsets[0][1]['fields'].append('withdrawal_referrer_person')
            attrs.update({
                'withdrawal_referrer' : forms.ModelChoiceField(
                    queryset=Person.objects.none(), 
                    required=False
                ),
            })

        if gas.config.can_change_delivery_place_on_each_order:
            gf_fieldsets[0][1]['fields'].append(('delivery_city', 'delivery_addr_or_place'))
            attrs.update({
                'delivery_city' : forms.CharField(required=True, 
                    label=_('Delivery city'), 
                    initial=gas.city
                ),
                'delivery_addr_or_place': forms.CharField(
                    required=True, label=_('Delivery address or place'), 
                    initial=gas.headquarter
                ),
            })

        if gas.config.use_withdrawal_place:

            if gas.config.can_change_withdrawal_place_on_each_order:
                gf_fieldsets[0][1]['fields'].append((
                    'withdrawal_datetime', 'withdrawal_city', 
                    'withdrawal_addr_or_place')
                )
                attrs.update({
                    'withdrawal_datetime' : forms.SplitDateTimeField(
                        required=False, label=_('Withdrawal on/at'), 
                        widget=admin_widgets.AdminSplitDateTime
                    ),
                    'withdrawal_city' : forms.CharField(
                        required=True, label=_('Withdrawal city'), 
                        initial=gas.city
                    ),
                    'withdrawal_addr_or_place': forms.CharField(required=True, 
                        label=_('Withdrawal address or place'), 
                        initial=gas.headquarter
                    ),
                })


        attrs.update(Meta=type('Meta', (), {
            'model' : GASSupplierOrder,
            'fields' : fields,
            'gf_fieldsets' : gf_fieldsets
        }))
    return type('Custom%s' % base.__name__, (base,), attrs)


