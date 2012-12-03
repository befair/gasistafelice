"""This module holds Mix-in class and final PlannedAddOrderForm class"""

from django import forms
from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.db import transaction
from django.contrib.admin import widgets as admin_widgets

from workflows.utils import set_initial_state

from gasistafelice.gas.forms.order.base import AddOrderForm
from gasistafelice.lib.widgets import DateFormatAwareWidget
from gasistafelice.gas.models.order import GASSupplierOrder, Delivery

from datetime import timedelta, datetime, date
import copy, logging
log = logging.getLogger(__name__)


FREQUENCY = [ 
    (7, _('week')), 
    (14, _('two weeks')), 
    (21, _('three weeks')), 
    (28, _('monthly')), 
    (56, _('two months')), 
    (84, _('three months')), 
    (168, _('half year')), 
    (336, _('year'))
]

#--------------------------------------------------------------------------------

class AddPlannedOrderForm(AddOrderForm):
    """MixIn class to be used with a forms.Form class to add repeated records"""

    repeat_order = forms.BooleanField(
        label=_('Is this a periodic order?'), required=False,
        help_text=_('Check the little square to plan this order as much times as you want')
    )
    repeat_frequency = forms.TypedChoiceField(required=False, choices=FREQUENCY, coerce=int)
    repeat_until_date = forms.DateField(initial=date.today, required=False
        , help_text=_("Required if you want to plan orders")
        , widget=DateFormatAwareWidget
    )

    def __init__(self, *args, **kw):
        super(AddPlannedOrderForm, self).__init__(*args, **kw)
        self._messages['info'].append(ug("If you want you can plan your orders with some frequency until a specific date"))

    def clean(self):
        """Validate data here. Not in save().

        Here we do not have self.instance, but we have self.cleaned_data

        Validate order planning at these conditions:

        * if repeat_order is set:
            * [DEPRECATED] datetime_end must be set
            * repeat_until_date must be set
            * repeat_until_date must be > datetime_start + _repeat_frequency

        """

        cleaned_data = super(AddPlannedOrderForm, self).clean()

        self.is_planning_order = cleaned_data['repeat_order']

        if self.is_planning_order:

            _repeat_frequency = cleaned_data['repeat_frequency']
            _repeat_items = None
            _repeat_until_date = cleaned_data['repeat_until_date']

            #Domthu: 20120318 can be unknow datetime, see Fero-Orlando directive.
#            if not cleaned_data.get('datetime_end'):
#                raise forms.ValidationError(ug("To plan an order you must set an end date and time"))

#NOTE fero: I do not completely agree. 
#NOTE fero: You can leave an order open for 3 month, but plan it every 1 month,
#NOTE fero: don't you agree?
#NOTE fero: otherwise this stuff is buggy and should add the condition that
#NOTE fero: (datetime_end - datetime_start).days < _repeat_frequency

#WAS           # Calcul _repeat_items
#WAS:            # Calcul _repeat_items
#WAS:            tmp_date = self.instance.datetime_end.date()
#WAS:            log.debug("repeat params: start %s end %s(%s), until: %s desired: %s" % (
#WAS:                self.instance.datetime_start,
#WAS:                self.instance.datetime_end,
#WAS:                tmp_date,
#WAS:                _repeat_until_date,
#WAS:                _repeat_frequency
#WAS:            ))
#WAS:            if _repeat_until_date and tmp_date and _repeat_until_date > tmp_date:

            if not _repeat_until_date:
                raise forms.ValidationError(ug("To plan an order you must set an end planning date"))

            start_date = cleaned_data['datetime_start'].date()
            min_repeat_until_date = start_date + timedelta(days=_repeat_frequency)
            if _repeat_until_date < min_repeat_until_date:
                raise forms.ValidationError(ug("To plan an order you must set an end planning date later than start date + frequency"))

                
#NOTE fero: just be positive and do not rely on self.instance: 
#WAS:                tmp_date = self.instance.datetime_start.date()
#WAS:                tmp_days = (_repeat_until_date - tmp_date).days
#WAS:                log.debug("repeat tmp date: %s days: %s" % (tmp_date, tmp_days))
#WAS:                _repeat_items = tmp_days // _repeat_frequency
#WAS:            log.debug("repeat parameters: %s, items: %s" % (_repeat_frequency, _repeat_items))
            how_many_days = (_repeat_until_date - start_date).days
            _repeat_items = how_many_days // _repeat_frequency

            log.debug("repeat tmp date: %s days: %s" % (start_date, how_many_days))
            log.debug("repeat parameters: %s, items: %s" % (_repeat_frequency, _repeat_items))

            # Verify params request is consistent
            if not _repeat_frequency or not _repeat_items or _repeat_items < 1:
                log.debug("CREATE PLANNED ORDERS: repeat some parameter wrong" + 
                    "_repeat_frequency=%s, _repeat_items=%s" % (
                    _repeat_frequency, _repeat_items  
                ))
                raise forms.ValidationError(ug("Something wrong has happened with planning parameters"))

            self._repeat_items = _repeat_items
            self._repeat_frequency = _repeat_frequency

        return cleaned_data

    def clone_base_order(self):
        """WAS GetNewOrder. This relates to planning.
        
        ....there will be another for InterGAS.
        """

        new_obj = copy.copy(self.instance)
        new_obj.pk = None
        set_initial_state(new_obj)

        return new_obj

    def create_repeated_orders(self):
        """Create other instances of GASSupplierOrder.

        If `repeat_order` field is True:

            1. delete previous repeated orders with the same root
            2. create many GASSupplierOrder with frequecy `repeat_frequency`
               until `repeat_until_date`

        This method must be invoked AFTER self.instance has been set,
        so after the "root" GASSupplierOrder is created
            
        """

#WAS: INTERGAS 2

        #Planning new orders
        for num in range(1, self._repeat_items+1):  #to iterate between 1 to _repeat_items

            #program order
            x_obj = self.clone_base_order()

            # planning
            x_obj.root_plan = self.instance 

            r_q = self._repeat_frequency*num
            if self.instance.delivery and self.instance.delivery.date:
                r_dd = self.instance.delivery.date
            else:
                r_dd = None

            #TODO: withdrawal appointment

            # Set date for open, close and delivery order
            x_obj.datetime_start += timedelta(days=r_q)
            if x_obj.datetime_end:
                x_obj.datetime_end += timedelta(days=r_q)
            if r_dd:
                r_dd += timedelta(days=r_q)

            if self.instance.delivery:
                try:
                    delivery, created = Delivery.objects.get_or_create(
                        date=r_dd,
                        place=self.instance.delivery.place
                    )
                except Delivery.MultipleObjectsReturned as e:
                    log.error("Delivery.objects.get_or_create(%s, %s): returned more than one. Lookup parameters were date=%s, place=%s" % (
                        r_dd, self.instance.delivery.place
                    ))
                    raise
                    
                else:
                    x_obj.delivery = delivery

#WAS: INTERGAS 4

            #create order
            #COMMENT domthu: Don't understand why .save() not return true?
            #WAS: if x_obj.save():
            #COMMENT fero: save() doesn't return True nor False.
            #COMMENT fero: it returns None. Django doc rules

            try:
                x_obj.save()
            except Exception as e:
                log.debug("repeat NOT created: item %s, r_q %s, start %s , end %s , delivery %s" % (
                    num, r_q, x_obj.datetime_start, 
                    x_obj.datetime_end, x_obj.delivery.date
                ))
                raise

            else:
                if not x_obj.pk:
                    raise ProgrammingError("save cannot finish with instance.pk == None")

                #WAS: unneeded code: if here, x_obj has been created. "if x_obj.pk"
                log.debug("repeat created order: %s " % (x_obj))

#WAS: INTERGAS 5

    @transaction.commit_on_success
    def save(self):

        super(AddPlannedOrderForm, self).save()

        if self.instance and self.is_planning_order:
            self.instance.delete_planned_orders()
            self.create_repeated_orders()

    class Meta(AddOrderForm.Meta):

        gf_fieldsets = [(None, {
            'fields' : ['pact'
                , 'datetime_start'
                , ('datetime_end', 'empty_end')
                , ('delivery_datetime', 'empty_delivery')
                , 'referrer_person'
                , ('repeat_order', 'repeat_frequency', 'repeat_until_date')
            ]
        })]

