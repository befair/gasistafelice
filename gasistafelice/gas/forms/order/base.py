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

#WAS: INTERGAS 0

    def __init__(self, request, *args, **kw):

        #log.debug("AddOrderForm")
        super(AddOrderForm, self).__init__(request, *args, **kw)
        self.request = request
        self.set_selectable_pacts()

        pacts = self._pacts

        if pacts.count() > 0:

            one_pact = pacts[0]
            self.fields['pact'].queryset = pacts
            self.fields['pact'].initial = one_pact

#WAS: INTERGAS 1

            self.set_initial_referrer()

            # If we are managing some pacts (even 1) of the same GAS,
            # we can set some additional defaults

            gas = pacts[0].gas

            #Next week by default
            dt = datetime.now()+timedelta(days=7)
            dt = first_day_on_or_after(6, dt)

            dt = self.set_initial_datetime_end(gas, dt)
            dt = self.set_initial_delivery_date(gas, dt)

    def set_selectable_pacts(self):

        """User can select pacts bound to specific resource and available to him.

        Limit pact to the logged user. Do not see pacts from other GAS than mine. 
        Due to "Supplier" resources that was showing pact for another GAS.

        This method set form attribute self._pacts
        """

        self._pacts = GASSupplierSolidalPact.objects.none()
        resource_pacts = self.request.resource.pacts
        user_pacts = self.request.user.person.pacts.values_list('pk')

        #KO by fero unneeded code: "if resource_pacts and user_pacts and "
        if resource_pacts.count() and user_pacts.count():
            self._pacts = resource_pacts.filter(pk__in = user_pacts)

        if not self._pacts.count():
            log.error("Cannot add an order on a resource with no pacts")

    def set_initial_referrer(self):
        """Set initial value for 'referrer_person'. """

        ref_field = self.fields['referrer_person']
        if self.request.user.person in ref_field.queryset:
            # Person is the current user: referrers
            ref_field.initial = self.request.user.person
        elif ref_field.queryset.count() > 0:
            ref_field.initial = ref_field.queryset[0]

    def set_initial_datetime_end(self, gas, dt):
        #Close
        d_c = get_day_from_choice(gas.config.default_close_day)
        if gas.config.default_close_day:
            dt = first_day_on_or_after(d_c, dt)
        if gas.config.default_close_time:
            dt = dt.replace(hour=gas.config.default_close_time.hour, minute=gas.config.default_close_time.minute)
        self.fields['datetime_end'].initial = dt
        return dt

    def set_initial_delivery_date(self, gas, dt):
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
        return dt

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
        super(AddOrderForm, self).save(*args, **kwargs)

#TODO            #send email
#            #COMMENT domthu: Only if opened?  Util? use another politica
#            _send_email = self.cleaned_data['email_gas']
#            if bool(_send_email):
#                TODO: May be we only need to disable the notification if not enabled


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

