from django import forms
from django.utils.translation import ugettext as ug, ugettext_lazy as _

from gasistafelice.lib.widgets import SplitDateTimeFormatAwareWidget
from gasistafelice.utils import datetime_round_ten_minutes

import datetime

#---------------------------------------------------------------------------------
# Specific forms support functions

def now_round_ten_minutes():

    dt = datetime.datetime.now()
    return datetime_round_ten_minutes(dt)

#---------------------------------------------------------------------------------

class BaseOrderForm(forms.ModelForm):

    #KO fero: no log here. This code is executed at import-time
    #KO fero: log.debug("BaseOrderForm")

    datetime_start = forms.SplitDateTimeField(label=_('Date start'), required=True, 
        help_text=_("when the order will be opened"), 
        widget=SplitDateTimeFormatAwareWidget, 
        initial=now_round_ten_minutes
    )

    datetime_end = forms.SplitDateTimeField(label=_('Date end'), required=False, 
        help_text=_("when the order will be closed"), 
        widget=SplitDateTimeFormatAwareWidget
    )

    delivery_datetime = forms.SplitDateTimeField(required=False, 
        label=_('Delivery on/at'), widget=SplitDateTimeFormatAwareWidget
    )

    referrer_person = forms.ModelChoiceField(label=_('referrer'), 
        queryset=Person.objects.none(), required=True, 
        error_messages={'required': _(u'You must select one referrer (or create it in GAS details if empty)')}
    )

    def __init__(self, request, *args, **kw):

        # Strip request arg and initialize form class
        super(BaseOrderForm, self).__init__(*args, **kw)

        referrers = request.resource.supplier_referrers_people
        if not referrers.count():
            #KO: not rendered the form and the relative warning
            #raise PermissionDenied(ug("You cannot open an order without referrers"))
            log.warning("AddOrderForm.__init__(): trying to create a new order without referrers!")

        self.fields['referrer_person'].queryset = referrers
        if self.fields.get('withdrawal_referrer_person'):
            self.fields['withdrawal_referrer_person'].queryset = referrers

    def clean(self):

        cleaned_data = self.cleaned_data
        dt_start = cleaned_data.get("datetime_start")
        dt_end = cleaned_data.get("datetime_end")
        dt_close = cleaned_data.get("delivery_datetime")
        #log.debug("AddOrderForm compare date [%s<%s<%s]" % (dt_start, dt_end, dt_close))
        # Only do something if both fields are valid so far.
        if dt_start and dt_end:
            if dt_start >= dt_end:
                 raise forms.ValidationError(ug(u"Start date can't be later or equal than end date"))

        if dt_end and dt_close:
            if dt_end > dt_close:
                 raise forms.ValidationError(ug("End date can't be later than delivery date"))

        # Always return the full collection of cleaned data.
        return cleaned_data

    def get_appointment_instance(self, name, klass):

        ddt = self.cleaned_data['%s_datetime' % name]
        if self.cleaned_data.get('%s_city' % name):
            dc =self.cleaned_data['%s_city' % name]
            dp = self.cleaned_data['%s_addr_or_place' % name]

            try:
                p = Place.objects.get(city=dc, name__icontains=dp)
            except Place.DoesNotExist:
                try:
                    p = Place.objects.get(city=dc, address__icontains=dp)
                except Place.DoesNotExist:
                    p = Place(city=dc, name=dp)
                    p.save()
        else:
            if self.cleaned_data.get('pact'):
                pact = self.cleaned_data['pact']
                if not pact:
                    return None
                p = getattr(pact.gas.config, "%s_place" % name)
            else:
                return None

        try:
            d, created = klass.objects.get_or_create(date=ddt, place=p)
        except klass.MultipleObjectsReturned as e:

            #FIXME TOVERIFY: get() returned more than one Delivery -- it returned 2!
            log.error("%s.get_appointment_instance(%s, %s): returned more than one. Lookup parameters were date=%s, place=%s" % (
                self.__class__.__name__,
                name, klass, ddt, p
            ))
            raise

        return d

    def get_delivery(self):
        return self.get_appointment_instance('delivery', Delivery)

    def get_withdrawal(self):
        return self.get_appointment_instance('withdrawal', Withdrawal)

#--------------------------------------------------------------------------------

class AddOrderForm(BaseOrderForm):
    """ use in forms:
            DES             ChooseSupplier  ChooseGAS ChooseReferrer
            GAS             ChooseSupplier  OneGAS    ChooseReferrer
            Supplier        OneSupplier     ChooseGAS ChooseReferrer
            Solidal Pact    OneSupplier     OneGAS    ChooseReferrer
    """
    pact = forms.ModelChoiceField(label=_('pact'), 
        queryset=GASSupplierSolidalPact.objects.none(), 
        required=True, 
        error_messages={'required': _(u'You must select one pact (or create it in your GAS details if empty)')}
    )
    email_gas = forms.BooleanField(label=_('Send email to the LIST of the GAS?'), required=False)
    repeat_order = forms.BooleanField(label=_('Repeat this order several times?'), required=False)
    repeat_frequency = forms.ChoiceField(required=False, choices=FREQUENCY)
    repeat_until_date = forms.DateField(initial=date.now(), widget=admin_widgets.AdminDateWidget)

#WAS: INTERGAS 0

    def __init__(self, request, *args, **kw):

        #log.debug("AddOrderForm")
        super(AddOrderForm, self).__init__(request, *args, **kw)

        # SOLIDAL PACT
        #pacts = request.resource.pacts
        pacts = GASSupplierSolidalPact.objects.none()
        resource_pacts = request.resource.pacts
        # Limit pact to the logged user. Do not see pacts from other GAS than mine. 
        # Due to "Supplier" resources that was showing pact for another GAS.
        # user_pacts = request.user.person.pacts
        user_pacts = request.user.person.pacts.values_list('pk')
        #KO by fero: not needed "if resource_pacts and user_pacts and "
        if resource_pacts.count() and user_pacts.count():
            pacts = resource_pacts.filter(pk__in = user_pacts)
#       if not pacts.count():
#            raise PermissionDenied(ug("You cannot open an order on a resource with no pacts"))
        #if pacts.count() == pacts.filter(gas=pacts[0].gas):

        if pacts.count() > 0:

            one_pact = pacts[0]
            self.fields['pact'].queryset = pacts
            self.fields['pact'].initial = one_pact

#WAS: INTERGAS 1

            # Person is the current user: referrers
            if request.user.person in self.fields['referrer_person'].queryset:
                self.fields['referrer_person'].initial = request.user.person
            elif self.fields['referrer_person'].queryset.count() > 0:
                self.fields['referrer_person'].initial = self.fields['referrer_person'].queryset[0]

            # If we are managing some pacts (even 1) of the same GAS,
            # we can set some additional defaults

            gas = pacts[0].gas

            #Next week by default
            dt = datetime.now()+timedelta(days=7)
            dt = first_day_on_or_after(6, dt)

            #Close
            d_c = get_day_from_choice(gas.config.default_close_day)
            if gas.config.default_close_day:
                dt = first_day_on_or_after(d_c, dt)
            if gas.config.default_close_time:
                dt = dt.replace(hour=gas.config.default_close_time.hour, minute=gas.config.default_close_time.minute)
            self.fields['datetime_end'].initial = dt

            #Delivery
            d_d = get_day_from_choice(gas.config.default_delivery_day)
            if d_d <= d_c:
                dt = dt+timedelta(days=7)
            if gas.config.default_delivery_day:
                dt = first_day_on_or_after(d_d, dt)
            if gas.config.default_delivery_time:
                dt = dt.replace(
                    hour=gas.config.default_delivery_time.hour, 
                    minute=gas.config.default_delivery_time.minute
                )
            self.fields['delivery_datetime'].initial = dt
            #log.debug("AddOrderForm delivery %s --> %s" % (d, dt))

    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        self.instance.pact = self.cleaned_data['pact']
        _gas = self.instance.pact.gas

        #TODO in clean(): Control if delivery referrer is a GAS's referrer

        if self.cleaned_data.get('delivery_datetime'):
            d = self.get_delivery()
            self.instance.delivery = d

        if _gas.config.use_withdrawal_place:
            if self.cleaned_data.get('withdrawal_datetime'):
                w = self.get_withdrawal()
                self.instance.withdrawal = w

        log.debug("AddOrderForm CREATED pre_save")
        _created_order = super(AddOrderForm, self).save(*args, **kwargs)
        if self.instance:

#            #send email
#            #COMMENT domthu: Only if opened?  Util? use another politica
#            _send_email = self.cleaned_data['email_gas']
#            if bool(_send_email):
#                TODO: May be we only need to disable the notification if not enabled

#WAS: INTERGAS 2

            #Planification
            _repeat_order = self.cleaned_data['repeat_order']
            if bool(_repeat_order):
                _repeat_amount = int(self.cleaned_data['repeat_frequency'])
                _repeat_items = None
                _repeat_until_date = self.cleaned_data['repeat_until_date']
                #Calcul _repeat_items
                tmp_date = self.instance.datetime_end.date()
                log.debug("repeat params: start %s end %s(%s), until: %s desired: %s" % (
                    self.instance.datetime_start,
                    self.instance.datetime_end,
                    tmp_date,
                    _repeat_until_date,
                    _repeat_amount)
                )
                if _repeat_until_date and tmp_date and _repeat_until_date > tmp_date:
                    tmp_date = self.instance.datetime_start.date()
                    tmp_days = (_repeat_until_date - tmp_date).days
                    log.debug("repeat tmp date: %s days: %s" % (tmp_date, tmp_days))
                    _repeat_items = tmp_days // _repeat_amount
                log.debug("repeat parameters: %s, items: %s" % (_repeat_amount, _repeat_items))

                #verify params request is consistent
                if not _repeat_amount or not _repeat_items or _repeat_items < 1:
                    log.debug("repeat some parameter wrong")
                    return _created_order

                #Delete - Clean all previous planification
                previous_planed_orders = GASSupplierOrder.objects.filter(
                    pact=self.instance.pact,
                    datetime_start__gt = self.instance.datetime_start
                )
                log.debug("repeat previous_planed_orders: %s" % (previous_planed_orders))
                for order in previous_planed_orders:

                    #delete only prepared orders
                    if order.is_prepared or order.is_active:

#WAS: INTERGAS 3

                        log.debug("AddOrderForm repeat delete previous_planed_orders: %s" % (order))
                        order.delete()

                #Planificate new orders
                for num in range(1,_repeat_items+1):  #to iterate between 1 to _repeat_items
                    #program order
                    x_obj = GetNewOrder(self.instance, None)
                    r_q = (_repeat_amount*num)
                    r_dd = self.instance.delivery.date

                    #set date for open, close and delivery order
                    x_obj.datetime_start += timedelta(days=+r_q)
                    x_obj.datetime_end += timedelta(days=+r_q)
                    r_dd += timedelta(days=+r_q)

                    x_obj.delivery = get_delivery(r_dd, self.instance.delivery.place)

#WAS: INTERGAS 4

                    #create order
                    #COMMENT domthu: Don't understand why .save() not return true?
                    #WAS: if x_obj.save():
                    x_obj.save()
                    if x_obj.pk:
                        log.debug("repeat created order: %s " % (x_obj))

#WAS: INTERGAS 5

                    else:
                        log.debug("repeat NOT created: item %s, r_q %s, start %s , end %s , delivery %s" % (num, r_q, x_obj.datetime_start, x_obj.datetime_end, x_obj.delivery.date))
        return _created_order


    class Meta:
        model = GASSupplierOrder
        fields = ['pact', 'datetime_start', 'datetime_end', 'referrer_person']

        gf_fieldsets = [(None, {
            'fields' : ['pact'
                            , ('datetime_start', 'datetime_end')
                            , 'delivery_datetime'
                            , 'referrer_person'
                            , ('repeat_order', 'repeat_frequency', 'repeat_until_date')
            ]
        })]
#WAS: INTERGAS 6
#                            , 'email_gas'


#-------------------------------------------------------------------------------

class EditOrderForm(BaseOrderForm):

    def __init__(self, request, *args, **kw):

        # TODO TOVERIFY fero
        # COMMENT fero: This is a bound form, so no need to set initial values.
        # COMMENT fero: values are already bound because we init the form with
        # COMMENT fero: instance=request.resource

        super(EditOrderForm, self).__init__(request, *args, **kw)

        # SOLIDAL PACT
        pact = request.resource.pact
        delivery = request.resource.delivery
        ref = request.resource.referrer_person
        if ref:
            #control if queryset not empty.
            self.fields['referrer_person'].initial = ref
        if request.resource.datetime_end:
            self.fields['datetime_end'].initial = request.resource.datetime_end
        if delivery and delivery.date:
            self.fields['delivery_datetime'].initial = delivery.date

    def save(self):

        if self.cleaned_data.get('delivery_datetime'):
            d = self.get_delivery()
            self.instance.delivery = d

        if self.cleaned_data.get('withdrawal_datetime'):
            w = self.get_withdrawal()
            self.instance.withdrawal = w

        return super(EditOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ['datetime_start', 'datetime_end', 'referrer_person']

        gf_fieldsets = [(None, {
            'fields' : [ ('datetime_start', 'datetime_end')
                            , 'delivery_datetime'
                            , 'referrer_person'
            ]
        })]

