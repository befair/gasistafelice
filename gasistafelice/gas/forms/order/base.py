
from django import forms
from django.db import transaction
from django.utils.translation import ugettext as ug, ugettext_lazy as _

from django.core.exceptions import PermissionDenied
from django.contrib import messages

from gasistafelice.utils import datetime_round_ten_minutes
from gasistafelice.lib.widgets import SplitDateTimeFormatAwareWidget, SplitDateTimeFieldWithClean

from gasistafelice.base.models import Place, Person
from gasistafelice.gas.models import ( 
    GASSupplierSolidalPact, GASSupplierOrder,
    Delivery, Withdrawal
)

import datetime

import logging
log = logging.getLogger(__name__)


#---------------------------------------------------------------------------------
# Specific forms support functions

def now_round_ten_minutes():

    dt = datetime.datetime.now()
    return datetime_round_ten_minutes(dt)

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
        dt += datetime.timedelta(days_to_go)
    return dt

#---------------------------------------------------------------------------------

class BaseOrderForm(forms.ModelForm):

    #KO fero: no log here. This code is executed at import-time
    #KO fero: log.debug("BaseOrderForm")

    datetime_start = forms.SplitDateTimeField(label=_('Date start'), required=True, 
        help_text=_("when the order will be opened"), 
        widget=SplitDateTimeFormatAwareWidget, 
        initial=now_round_ten_minutes
    )

    datetime_end = SplitDateTimeFieldWithClean(label=_('Date end'), required=False, 
        help_text=_("when the order will be closed"), 
        widget=SplitDateTimeFormatAwareWidget
    )

    empty_end = forms.BooleanField(label=_('Do not set date end'), required=False)

    delivery_datetime = forms.SplitDateTimeField(required=False, 
        label=_('Delivery on/at'), widget=SplitDateTimeFormatAwareWidget
    )

    empty_delivery = forms.BooleanField(label=_('Do not set delivery'), required=False)

    referrer_person = forms.ModelChoiceField(label=_('referrer').capitalize(), 
        queryset=Person.objects.none(), required=True, 
        error_messages={'required': _(u'You must select one referrer (or create it in GAS details if empty)')}
    )

    def __init__(self, request, *args, **kw):

        #TODO: fero to refactory and move in GF Form baseclass...
        self._messages = {
            'error' : [],
            'info' : [],
            'warning' : [],
        }

        # Strip request arg and initialize form class
        super(BaseOrderForm, self).__init__(*args, **kw)

        referrers = request.resource.supplier_referrers_people
        if not referrers.count():
            #KO: not rendered the form and the relative warning
            #NOTE fero: it shouldn't arrive here...no matter for me if it is and HARD exception
            #raise PermissionDenied(ug("You cannot open an order without referrers"))
            log.warning("BaseOrderForm.__init__(): trying to create a new order without referrers!")

        self.fields['referrer_person'].queryset = referrers
        if self.fields.get('withdrawal_referrer_person'):
            self.fields['withdrawal_referrer_person'].queryset = referrers

    def write_down_messages(self):
        """Used to return messages related to form.

        Usually called:
        * in request.method == "GET"
        * when it is "POST" but form is invalid
        """

        # Write down messages only if we are GETting the form
        for level, msg_list in self._messages.items():
            for msg in msg_list:
                getattr(messages, level)(self.request, msg)

    def clean(self):

        cleaned_data = self.cleaned_data
        dt_start = cleaned_data.get("datetime_start")
        e_end = self.cleaned_data.get('empty_end')
        e_del = self.cleaned_data.get('empty_delivery')
        if e_end:
            del cleaned_data["datetime_end"]
            del cleaned_data["delivery_datetime"]
        elif e_del:
            del cleaned_data["delivery_datetime"]
        dt_end = cleaned_data.get("datetime_end")
        dt_delivery = cleaned_data.get("delivery_datetime")

        #log.debug("BaseOrderForm compare date [%s<%s<%s]" % (dt_start, dt_end, dt_delivery))
        # Only do something if both fields are valid so far.
        if dt_start and dt_end:
            if dt_start >= dt_end:
                 raise forms.ValidationError(ug(u"Start date can't be later or equal than end date"))

        if dt_end and dt_delivery:
            if dt_end > dt_delivery:
                 raise forms.ValidationError(ug("End date can't be later than delivery date"))

        # Set cleaned data additional keys:
        # pact: needed if we are in EditOrderForm
        pact = cleaned_data.get('pact') or self.instance.pact
        cleaned_data['pact'] = pact

        # delivery_appointment: d would be saved within save()
        if dt_delivery:
            d = self.get_delivery()
            cleaned_data['delivery_appointment'] = d 

        # withdrawal_appointment
        # COMMENT fero: I think that EVERY order SHOULD have withdrawal_place
        # COMMENT fero: ok to not show in form, but programmatically create it anyway
        # see also...
        # https://github.com/feroda/gasistafelice/commit/1209d5390c1a354d24cf8c53add98fbef4b0a55a#commitcomment-935905
        if pact.gas.config.use_withdrawal_place:
            if self.cleaned_data.get('withdrawal_datetime'):
                w = self.get_withdrawal()
                cleaned_data['withdrawal_appointment'] = w 

        # Always return the full collection of cleaned data.
        return cleaned_data

    def get_appointment_instance(self, name, klass):
        """Return a delivery or withdrawal instance.

        If instance already exist in db ==> return it,
        return a non-saved instance otherwise.

        It would be saved in save()
        """

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
            # try to get already existent appointment
            appointment = klass.objects.get(date=ddt, place=p)
        except klass.DoesNotExist as e:
            appointment = klass(date=ddt, place=p)
        except klass.MultipleObjectsReturned as e:

            #FIXME TOVERIFY: get() returned more than one Delivery -- it returned 2!
            log.error("%s.get_appointment_instance(%s, %s): returned more than one. Lookup parameters were date=%s, place=%s" % (
                self.__class__.__name__,
                name, klass, ddt, p
            ))
            raise

        return appointment

    def get_delivery(self):
        return self.get_appointment_instance('delivery', Delivery)

    def get_withdrawal(self):
        return self.get_appointment_instance('withdrawal', Withdrawal)

    @transaction.commit_on_success
    def save(self, *args, **kwargs):

        d = self.cleaned_data.get('delivery_appointment')
        if d and not d.pk:
            d.save()
        self.instance.delivery = d

        w = self.cleaned_data.get('withdrawal_appointment')
        if w and not w.pk:
            w.save()
        self.instance.withdrawal = w

        super(BaseOrderForm, self).save(*args, **kwargs)


#--------------------------------------------------------------------------------

class AddOrderForm(BaseOrderForm):
    """ use in forms:
            DES             ChooseSupplier  ChooseGAS ChooseReferrer
            GAS             ChooseSupplier  OneGAS    ChooseReferrer
            Supplier        OneSupplier     ChooseGAS ChooseReferrer
            Solidal Pact    OneSupplier     OneGAS    ChooseReferrer
    """
    pact = forms.ModelChoiceField(label=_('pact').capitalize(), 
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
            dt = datetime.datetime.now()+datetime.timedelta(days=7)
            dt = first_day_on_or_after(6, dt)
            #Close
            d_c = get_day_from_choice(gas.config.default_close_day)

            dt = self.set_initial_datetime_end(gas, dt, d_c)
            dt = self.set_initial_delivery_date(gas, dt, d_c)

    def set_selectable_pacts(self):

        """User can select pacts bound to specific resource and available to him.

        Limit pact to the logged user. Do not see pacts from other GAS than mine. 
        Due to "Supplier" resources that was showing pact for another GAS.

        This method set form attribute self._pacts
        """

        resource_pacts = self.request.resource.pacts

        if self.request.user.is_superuser:
            self._pacts = resource_pacts
        else:
            self._pacts = GASSupplierSolidalPact.objects.none()
            user_pacts = self.request.user.person.pacts.values_list('pk')

            #KO by fero unneeded code: "if resource_pacts and user_pacts and "
            if resource_pacts.count() and user_pacts.count():
                self._pacts = resource_pacts.filter(pk__in = user_pacts)

        if not self._pacts.count():
            log.error("Cannot add an order on a resource with no pacts")
            self._messages['error'].append(ug("No pacts selectable for you. Please contact staff"))
        else:
            self._messages['info'].append(ug("Please select the pact you want to make an order for"))


    def set_initial_referrer(self):
        """Set initial value for 'referrer_person'. """

        ref_field = self.fields['referrer_person']
        if self.request.user.person in ref_field.queryset:
            # Person is the current user: referrers
            ref_field.initial = self.request.user.person
        elif ref_field.queryset.count() > 0:
            ref_field.initial = ref_field.queryset[0]
        else:
            self._messages['error'].append(ug("No referrers selectable for you. Please add tech referrer to add pact referrers for your GAS"))

    def set_initial_datetime_end(self, gas, dt, d_c):

        if gas.config.default_close_day:
            dt = first_day_on_or_after(d_c, dt)
        if gas.config.default_close_time:
            dt = dt.replace(
                hour=gas.config.default_close_time.hour, 
                minute=gas.config.default_close_time.minute
            )
        self.fields['datetime_end'].initial = dt
        return dt

    def set_initial_delivery_date(self, gas, dt, d_c):
        #Delivery
        d_d = get_day_from_choice(gas.config.default_delivery_day)
        if d_d <= d_c:
            dt = dt+datetime.timedelta(days=7)
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

        #TODO in clean(): Control if delivery referrer is a GAS's referrer

#TODO            #send email
#            #COMMENT domthu: Only if opened?  Util? use another politica
#            _send_email = self.cleaned_data['email_gas']
#            if bool(_send_email):
#                TODO: May be we only need to disable the notification if not enabled

        log.debug("AddOrderForm CREATED pre_save")
        super(AddOrderForm, self).save(*args, **kwargs)


    class Meta:
        model = GASSupplierOrder
        fields = ['pact', 'datetime_start', 'datetime_end', 'referrer_person']

        gf_fieldsets = [(None, {
            'fields' : ['pact'
                            , 'datetime_start'
                            , ('datetime_end', 'empty_end')
                            , ('delivery_datetime', 'empty_delivery')
                            , 'referrer_person'
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

    class Meta:
        model = GASSupplierOrder
        fields = ['datetime_start', 'datetime_end', 'referrer_person']

        gf_fieldsets = [(None, {
            'fields' : [ ('datetime_start', 'datetime_end')
                            , 'delivery_datetime'
                            , 'referrer_person'
            ]
        })]

