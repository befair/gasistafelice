"""This module holds Mix-in class and final PlannedAddOrderForm class"""

from django import forms
from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.db import transaction
from django.contrib.admin import widgets as admin_widgets

from workflows.utils import set_initial_state

from gasistafelice.gas.forms.order.base import AddOrderForm
from gasistafelice.lib.widgets import DateFormatAwareWidget
from gasistafelice.gas.models.order import GASSupplierOrder, Delivery, GASMemberOrderPlaned

from gasistafelice.lib.fields.forms import CurrencyField
from django.forms.formsets import formset_factory
from gasistafelice.lib.formsets import BaseFormSetWithRequest

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

        self.is_repeated = cleaned_data['repeat_order']

        if self.is_repeated:

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
                log.debug("CREATE REPEATED ORDERS: repeat some parameter wrong" + 
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

    def delete_previous_planned_orders(self):

        # Delete - Clean all previous planification
        previous_planned_orders = GASSupplierOrder.objects.filter(
            pact=self.instance.pact,
            datetime_start__gt = self.instance.datetime_start
        )
        log.debug("repeat previous_planned_orders: %s" % (previous_planned_orders))
        for order in previous_planned_orders:

            #delete only prepared orders
            if order.is_prepared or order.is_active:

#WAS: INTERGAS 3

                log.debug("AddOrderForm repeat delete previous_planned_orders: %s" % (order))
                order.delete()

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

        self.delete_previous_planned_orders()

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
            #COMMENT fero: save() doesn't ever return True nor False.
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

        if self.instance and self.is_repeated:
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


#--------------------GASMember programmed orders-----------------------------------------------------------

class SinglePlanedOrderForm(forms.Form):

    #For editing
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    pk = forms.IntegerField(required=False)
    planed = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'size':'85'}), 
        max_length=200
    )
    price = CurrencyField()
    is_suspended = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(SinglePlanedOrderForm, self).__init__(*args, **kw)
        instance = getattr(self, 'instance', None)
        self.fields['pk'].widget.attrs['readonly'] = True
        self.fields['pk'].widget.attrs['disabled'] = 'disabled'
        self.fields['pk'].widget.attrs['class'] = 'input_small'
        self.fields['price'].widget.attrs['class'] = 'input_short taright'
        self.__gasmember = request.resource

    def save(self):

        log.debug("Save SinglePlanedOrderForm")
        if self.cleaned_data.get('id'):
            ss = GASMemberOrderPlaned.objects.get(pk=self.cleaned_data['id'])
            prd = ss.planed
            log.debug("Save SinglePlanedOrderForm id_ss(%s) id_prd(%s)" % (ss.pk, prd.pk))
            try:
                prd.name = self.cleaned_data['planed']
                prd.save()
            except Exception, e:
                raise
                log.debug("Save SinglePlanedOrderForm error(%s)" %  str(e))
                Exception("Save SinglePlanedOrderForm error: %s", str(e))
        else:
            log.debug("New SinglePlanedOrderForm")

SingleGASMemberPlanedOrderForm = formset_factory(
    form=SinglePlanedOrderForm, 
    formset=BaseFormSetWithRequest, 
    extra=5,
)

class EditPlanedOrderForm(forms.ModelForm):
    """Edit form for mixed-in Stock and GASMemberOrderPlaned attributes.

    """

    planed_amount = forms.IntegerField(required=True, initial=20, label=_("VAT percent"))
    is_suspended = forms.BooleanField(required=False, label=_("Availability"))
   
    def __init__(self, request, *args, **kw):
        super(EditPlanedOrderForm, self).__init__(*args, **kw)
        self._gasmember = request.resource.gasmember
        self._gasstock = request.resource.planed
        self.fields['planed_amount'].initial = int(self._gasstock.planed_amount)
        self.fields['is_suspended'].initial = bool(request.resource.is_suspended)

        # If Supplier is not the Producer ==>
        # can't change planed info!
        if self._gasmember != self._gasstock.producer:
            for k,v in self.fields.items():
                 if k.startswith('planed_'):
                    self.fields[k].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = super(EditPlanedOrderForm, self).clean()
        cleaned_data['supplier'] = self._gasmember
        cleaned_data['is_suspended'] = [0,ALWAYS_AVAILABLE][self.cleaned_data.get('is_suspended')]
        cleaned_data['planed_amount'] = Decimal(cleaned_data['planed_amount'])

        # Update planed with new info
        for k,v in cleaned_data.items():
             if k.startswith('planed_'):
                setattr(self._gasstock, k[len('planed_'):], v)

        cleaned_data['planed'] = self._gasstock
        log.debug(self.errors)

        return cleaned_data

    def save(self):
        log.debug("Saving updated planed: %s" % self.instance.__dict__)
        log.debug("cleaned data = %s" % self.cleaned_data)
        planed = self.cleaned_data['planed']
        planed.save()
        self.instance.planed = planed
        self.instance.planed_amount = self.cleaned_data['planed_amount']
        self.instance.save()
        
    class Meta:
        model = GASMemberOrderPlaned
        exclude = ('supplier', 'planed_amount', 'planed')
        
        gf_fieldsets = (
            (None, {
                'fields': (
                    'planed_name',
                    'planed_description',
                    ('price', 'planed_amount'),
                )
             }),
             (_("Distribution info"), {
                'fields' : (
                    ('units_minimum_amount', 'units_per_box'),
                    ('detail_minimum_amount', 'detail_step'), 
                    'is_suspended',
                )
             }),
             (_("Supplier info"), {
                'fields' : (
                    ('code', 'supplier_category'),
                )
             })
            )
class AddPlanedOrderForm(EditPlanedOrderForm):
    """Add new planed and stock"""

    def __init__(self, request, *args, **kw):

        super(EditPlanedOrderForm, self).__init__(*args, **kw)
        self._gasmember = request.resource.gasmember
        self._gasstock = Product()
        self.fields['planed_name'].widget.attrs['class'] = 'input_medium'
        self.fields['planed_description'].widget.attrs['class'] = 'input_long'
        self.fields['planed_amount'].initial = 21
        self.fields['is_suspended'].initial = True

        self.fields['supplier_category'].queryset = self.fields['supplier_category'].queryset.filter(
            supplier=self._gasmember
        )

    def clean(self):

        cleaned_data = super(EditPlanedOrderForm, self).clean()
        cleaned_data['supplier'] = self._gasmember
        cleaned_data['planed_amount'] = [0,ALWAYS_AVAILABLE][self.cleaned_data.get('is_suspended')]
        cleaned_data['planed_amount'] = Decimal(cleaned_data['planed_amount'])/100

        cleaned_data['planed'] = self._gasstock
        log.debug(self.errors)

        return cleaned_data

    def save(self):
        log.debug("Saving new planed order:")
        log.debug("cleaned data = %s" % self.cleaned_data)
        planed = self.cleaned_data['planed']
        planed.purchaser = self._gasmember
        planed.gasstock = self.__gasstock
        planed.planed_amount = self.cleaned_data['planed_amount']
        planed.is_suspended = self._gasmember.is_suspended
        planed.save()
