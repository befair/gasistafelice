from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.gas.models import GASMemberOrder, GASSupplierOrder, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.gas.models import GASSupplierOrderProduct, GASMemberOrder
from gasistafelice.gas.models import Delivery, Withdrawal
from gasistafelice.base.models import Place, Person
from flexi_auth.models import ParamRole, PrincipalParamRoleRelation

from gasistafelice.base import const

from django.conf import settings
import copy
from datetime import tzinfo, timedelta, datetime
import logging
log = logging.getLogger(__name__)

from django.core import validators
from django.core.exceptions import ValidationError, PermissionDenied


def gf_now():
    dt = datetime.now()
    #dt.minutes = (dt.minutes/15)*15
    dt += timedelta(minutes=5)
    dt -= timedelta(minutes=dt.minute % 10,
                     seconds=dt.second,
                     microseconds=dt.microsecond)
    return dt

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

class GFSplitDateTimeWidget(admin_widgets.AdminSplitDateTime):

    def __init__(self, *args, **kw):
        super(GFSplitDateTimeWidget, self).__init__(*args, **kw)
        self.widgets[0].format=settings.DATE_INPUT_FORMATS[0]
        self.widgets[1].widget = admin_widgets.AdminTimeWidget()
        self.widgets[1].format=settings.TIME_INPUT_FORMATS[0]


class BaseOrderForm(forms.ModelForm):

    log.debug("BaseOrderForm")
    datetime_start = forms.SplitDateTimeField(label=_('Date start'), required=True, 
                    help_text=_("when the order will be opened"), widget=GFSplitDateTimeWidget, initial=gf_now)

    datetime_end = forms.SplitDateTimeField(label=_('Date end'), required=False, 
                    help_text=_("when the order will be closed"), widget=GFSplitDateTimeWidget)

    delivery_datetime = forms.SplitDateTimeField(required=False, label=_('Delivery on/at'), widget=GFSplitDateTimeWidget)

    delivery_referrer_person = forms.ModelChoiceField(label=_('referrer'), queryset=Person.objects.none(), required=True, error_messages={'required': _(u'You must select one referrer (or create it in GAS details if empty)')})

    def __init__(self, request, *args, **kw):
        #Strip request arg
        super(BaseOrderForm, self).__init__(*args, **kw)
        #gas_queryset = request.resource.gas.supplier_referrers_people
        referrers = request.resource.supplier_referrers_people
        #Ko: not rendered the form and the relative warning
#        if not referrers.count():
#            raise PermissionDenied(_("You cannot open an order without referrers"))

        self.fields['delivery_referrer_person'].queryset = referrers
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
                 raise forms.ValidationError("some problem with date start and close date [%s<%s]" % (dt_start, dt_end))

        if dt_end and dt_close:
            if dt_end > dt_close:
                 raise forms.ValidationError("some problem with close and delivery date [%s<%s]" % (dt_end, dt_close))

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
                    p = Place.objects.get(city=dc, addr__icontains=dp)
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

        d, created = klass.objects.get_or_create(date=ddt, place=p)
        return d
        
    def get_delivery(self):
        return self.get_appointment_instance('delivery', Delivery)

    def get_withdrawal(self):
        return self.get_appointment_instance('withdrawal', Withdrawal)

#-------------------------------------------------------------------------------

class AddOrderForm(BaseOrderForm):
    """ use in forms:
            des             ChooseSupplier  ChooseGAS ChooseReferrer
            GAS             ChooseSupplier  OneGAS    ChooseReferrer
            Suppplier       OneSupplier     ChooseGAS ChooseReferrer
            Solidal Pact    OneSupplier     OneGAS    ChooseReferrer
    """
    pact = forms.ModelChoiceField(label=_('pact'), queryset=GASSupplierSolidalPact.objects.none(), required=True, error_messages={'required': _(u'You must select one pact (or create it in your GAS details if empty)')})
    email_gas = forms.BooleanField(label=_('Send email to the LIST of the GAS?'), required=False)

    def __init__(self, request, *args, **kw):

        log.debug("AddOrderForm")
        super(AddOrderForm, self).__init__(request, *args, **kw)

        # SOLIDAL PACT
        pacts = request.resource.pacts

#       if not pacts.count():
#            raise PermissionDenied(_("You cannot open an order on a resource with no pacts"))
        #if pacts.count() == pacts.filter(gas=pacts[0].gas):
        if pacts.count() > 0:

            self.fields['pact'].queryset = pacts
            self.fields['pact'].initial = pacts[0]

            # Person is the current user: referrers
            log.debug("AddOrderForm delivery_referrer queryset %s" % self.fields['delivery_referrer_person'].queryset)
            if request.user.person in self.fields['delivery_referrer_person'].queryset:
                self.fields['delivery_referrer_person'].initial = request.user.person
            elif self.fields['delivery_referrer_person'].queryset.count() > 0:
                self.fields['delivery_referrer_person'].initial = self.fields['delivery_referrer_person'].queryset[0]

#        # Order referrer is not needed: pact referrers are enough!
#        if request.user.person in self.fields['referrer_person'].queryset:
#            self.fields['referrer_person'].initial = request.user.person
#        elif self.fields['referrer_person'].queryset.count() > 0:
#            self.fields['referrer_person'].initial = self.fields['referrer_person'].queryset[0]

            # If we are managing some pacts (even 1) of the same GAS,
            # we can set some additional defaults

            gas = pacts[0].gas
            #Next week by default
            dt = datetime.now()+timedelta(days=7)
            dt = first_day_on_or_after(6, dt)

            #Close
            if gas.config.default_close_day:
                dt = first_day_on_or_after(get_day_from_choice(gas.config.default_close_day), dt)
            if gas.config.default_close_time:
                dt = dt.replace(hour=gas.config.default_close_time.hour, minute=gas.config.default_close_time.minute)
            self.fields['datetime_end'].initial = dt

            #Delivery
            if gas.config.default_delivery_day:
                dt = first_day_on_or_after(get_day_from_choice(gas.config.default_delivery_day), dt)
            if gas.config.default_delivery_time:
                dt = dt.replace(hour=gas.config.default_delivery_time.hour, minute=gas.config.default_delivery_time.minute)
            self.fields['delivery_datetime'].initial = dt
            #log.debug("AddOrderForm delivery %s --> %s" % (d, dt))

    #def save(self, commit=True):
    def save(self, *args, **kwargs):
        self.instance.pact = self.cleaned_data['pact']
        _gas = self.instance.pact.gas

        #TODO: Control il delivery referrer is a GAS's referrer

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
            _send_email = self.cleaned_data['email_gas']
            new_id = self.instance.pk
            log.debug("AddOrderForm CREATED Ord. %s" % (new_id))
            if _send_email and bool(_send_email):
                _msg = _('Created order %s' % (new_id))
                log.debug("AddOrderForm CREATED send email %s" % (_msg))

        return _created_order


    class Meta:
        model = GASSupplierOrder
        fields = ['pact', 'datetime_start', 'datetime_end', 'delivery_referrer_person']

        gf_fieldsets = [(None, {
            'fields' : ['pact'
                            , ('datetime_start', 'datetime_end')
                            , 'delivery_datetime'
                            , 'delivery_referrer_person'
                            , 'email_gas'
            ]
        })]

#-------------------------------------------------------------------------------


class EditOrderForm(BaseOrderForm):

    log.debug("EditOrderForm")

    def __init__(self, request, *args, **kw):

        super(EditOrderForm, self).__init__(request, *args, **kw)

        #SOLIDAL PACT
        pact = request.resource.pact
        delivery = request.resource.delivery
        ref = request.resource.delivery_referrer_person
        if ref:
            #control if queryset not empty.
            self.fields['delivery_referrer_person'].initial = ref
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
        fields = ['datetime_start', 'datetime_end', 'delivery_referrer_person', 'delivery_cost']

        gf_fieldsets = [(None, {
            'fields' : [ ('datetime_start', 'datetime_end')
                            , 'delivery_datetime'
                            , 'delivery_referrer_person'
            ]
        })]

def form_class_factory_for_request(request, base):
    """Return appropriate form class basing on GAS configuration
    and other request parameters if needed"""

    log.debug("OrderForm--> form_class_factory_for_request")
    fields = copy.deepcopy(base.Meta.fields)
    gf_fieldsets = copy.deepcopy(base.Meta.gf_fieldsets)
    attrs = {}
    gas = request.resource.gas

    if gas:

        #TODO: ECO 2 way for inserting economic data
        refs = gas.cash_referrers
        if refs and request.user in refs:
            gf_fieldsets[0][1]['fields'].append('delivery_cost')

        if gas.config.use_withdrawal_place:
            gf_fieldsets[0][1]['fields'].append('withdrawal_referrer_person')
            attrs.update({
                'withdrawal_referrer' : forms.ModelChoiceField(queryset=Person.objects.none(), required=False),
            })

        if gas.config.can_change_delivery_place_on_each_order:
            gf_fieldsets[0][1]['fields'].append(('delivery_city', 'delivery_addr_or_place'))
            attrs.update({
                'delivery_city' : forms.CharField(required=True, label=_('Delivery city'), initial=gas.city),
                'delivery_addr_or_place': forms.CharField(required=True, label=_('Delivery address or place'), initial=gas.headquarter),
            })

        if gas.config.use_withdrawal_place:

            if gas.config.can_change_withdrawal_place_on_each_order:
                gf_fieldsets[0][1]['fields'].append(('withdrawal_datetime', 'withdrawal_city', 'withdrawal_addr_or_place'))
                attrs.update({
                    'withdrawal_datetime' : forms.SplitDateTimeField(required=False, label=_('Withdrawal on/at'), widget=admin_widgets.AdminSplitDateTime),
                    'withdrawal_city' : forms.CharField(required=True, label=_('Withdrawal city'), initial=gas.city),
                    'withdrawal_addr_or_place': forms.CharField(required=True, label=_('Withdrawal address or place'), initial=gas.headquarter),
                })


        attrs.update(Meta=type('Meta', (), {
            'model' : GASSupplierOrder,
            'fields' : fields,
            'gf_fieldsets' : gf_fieldsets
        }))
    return type('Custom%s' % base.__name__, (base,), attrs)


#-------------------------------------------------------------------------------


class GASSupplierOrderProductForm(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)
    #log.debug("Create GASSupplierOrderProductForm (%s)" % id)

    def __init__(self, request, *args, **kw):
        super(GASSupplierOrderProductForm, self).__init__(*args, **kw)

    #@transaction.commit_on_success
    def save(self):

        #log.debug("Save GASSupplierOrderProductForm")
        id = self.cleaned_data.get('id')
        log.debug("Save GASSupplierOrderProductForm id(%s)" % id)
        if id:
            enabled = self.cleaned_data.get('enabled')
            log.debug("Save GASSupplierOrderProductForm enabled(%s)" % enabled)
            #Delete is ok for gsop that have gmo but: 
            #FIXME: if no gmo associated to gsop the field enabled remain always True?
            if not enabled:
                gsop = GASSupplierOrderProduct.objects.get(pk=id)
                log.debug("STO rendendo indisponibile (fuori stagione) un prodotto da un ordine aperto")
                log.debug("order(%s) %s  per prodotto(%s): %s |||| ordini gasmember: [Euro %s/Qta %s/Gasisti %s]" % (gsop.order.pk, gsop.order, id, gsop.product, gsop.tot_price, gsop.tot_amount, gsop.tot_gasmembers))
                gsop.delete()



#-------------------------------------------------------------------------------


class SingleGASMemberOrderForm(forms.Form):
    """Return form class for row level operation on GSOP datatable"""

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    #log.debug("Create SingleGASMemberOrderForm (%s)" % id)
    gssop_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    ordered_amount = forms.DecimalField(required=False, initial=0)
    ordered_price = forms.DecimalField(required=False, widget=forms.HiddenInput)
    note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        super(SingleGASMemberOrderForm, self).__init__(*args, **kw)
        self.fields['note'].widget.attrs['class'] = 'input_medium'
        self.__gm = request.resource.gasmember
        self.__gmusr = request.resource.gasmember.person.user
        self.__loggedusr = request.user

    def clean(self):
        cleaned_data = super(SingleGASMemberOrderForm, self).clean()
        if not self.__gmusr or self.__gmusr != self.__loggedusr:
            log.debug("------SingleGASMemberOrderForm (%s) not enabled for %s" % (self.__gmusr,self.__loggedusr))
            raise forms.ValidationError(_("You are not authorized to make an order for %(person)s") % {'person' :self.__gmusr})
        return cleaned_data
    def save(self):

        id = self.cleaned_data.get('id')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
            gmo.ordered_price = self.cleaned_data.get('ordered_price')
            gmo.ordered_amount = self.cleaned_data.get('ordered_amount')
            gmo.note = self.cleaned_data.get('note')
            if gmo.ordered_amount == 0:
                gmo.delete()
                #log.debug("STO CANCELLANDO un ordine gasista da widget quantita")
            else:
                gmo.save()
                log.debug("Product ho aggiornato un ordine gasista (%s) " % id)

        elif self.cleaned_data.get('ordered_amount'):
                gssop = GASSupplierOrderProduct.objects.get(pk=self.cleaned_data.get('gssop_id'))
                #retrieve if yet exist. Security to ensure non duplicate entry into database
                #But this is done into GASMemberOrder Model with set unique_together
                gmo = GASMemberOrder(
                        ordered_product = gssop,
                        ordered_price = self.cleaned_data.get('ordered_price'),
                        ordered_amount = self.cleaned_data.get('ordered_amount'),
                        note = self.cleaned_data.get('note'),
                        purchaser = self.__gm,
                )
                gmo.save()
                log.debug("Product ho creato un ordine gasista (%s) " % gmo.pk)

class BasketGASMemberOrderForm(forms.Form):
    """Return form class for row level operation on GMO datatable"""

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    #log.debug("Create BasketGASMemberOrderForm (%s)" % id)
    gm_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    gsop_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    ordered_amount = forms.DecimalField(required=False, initial=0)
    ordered_price = forms.DecimalField(required=False, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(BasketGASMemberOrderForm, self).__init__(*args, **kw)
        #self.__gm = request.resource.gasmember
        self.__gmusr = request.resource.gasmember.person.user
        self.__loggedusr = request.user


    def save(self):

        if not self.__gmusr or self.__gmusr != self.__loggedusr:
            log.debug("------BasketGASMemberOrderForm (%s) not enabled for %s" % (self.__gmusr,self.__loggedusr))
            return
        id = self.cleaned_data.get('id')
        gm_id = self.cleaned_data.get('gm_id')
        gsop_id = self.cleaned_data.get('gsop_id')
        enabled = self.cleaned_data.get('enabled')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
#            if gm_id and gm_id != gmo.purchaser.pk:
#                print "Qualcosa non va con: GASmember"
#                return ""
            gmo.ordered_price = self.cleaned_data.get('ordered_price')
            gmo.ordered_amount = self.cleaned_data.get('ordered_amount')
            #log.debug("BasketGASMemberOrderForm (%s) enabled = %s" % (gmo.pk,enabled))
            if gmo.ordered_amount == 0:
                gmo.delete()
                log.debug("Basket STO CANCELLANDO un ordine gasista da widget quantita")
            elif enabled:
                gmo.delete()
                log.debug("Basket STO CANCELLANDO un ordine gasista da check enabled")
            else:
                gmo.save()
                log.debug("Basket ho aggiornato un ordine gasista (%s) " % id)

