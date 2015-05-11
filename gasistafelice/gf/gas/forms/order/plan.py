"""This module holds Mix-in class and final PlannedAddOrderForm class"""

from django import forms
from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.db import transaction
from django.contrib.admin import widgets as admin_widgets

from gf.gas.forms.order.base import AddOrderForm
from lib.widgets import DateFormatAwareWidget
from gf.gas.models.order import GASSupplierOrder, Delivery

from datetime import timedelta, datetime, date
import logging
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

            log.debug("plan info: start_date=%s days=%s, repeat_until_date=%s" % (
                `start_date`, how_many_days, `_repeat_until_date`
            ))
            log.debug("plan info2: frequency=%s, items=%s, min_repeat_until_date=%s" % (
                _repeat_frequency, _repeat_items, `min_repeat_until_date`
            ))

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

    def create_repeated_orders(self):
        return self.instance.plan(self._repeat_items, self._repeat_frequency)

    def delete_planned_orders(self):
        
        #LESSON LF: Left here just to simplify the understanding of the code evolution    
        self.instance.delete_planneds()

#WAS: INTERGAS 5

    @transaction.atomic
    def save(self):

        log.debug("Entering save order %s" % self.__class__)

        super(AddPlannedOrderForm, self).save()

        if self.instance and self.is_planning_order:
            self.delete_planned_orders()
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

