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
from gasistafelice.consts import GAS_REFERRER_WITHDRAWAL, GAS_REFERRER_DELIVERY

from django.conf import settings
import datetime, copy
import logging
log = logging.getLogger(__name__)

def gf_now():
    dt = datetime.datetime.now()
    return dt

class GFSplitDateTimeWidget(admin_widgets.AdminSplitDateTime):

    def __init__(self, *args, **kw):
        super(GFSplitDateTimeWidget, self).__init__(*args, **kw)
        self.widgets[0].format=settings.DATE_INPUT_FORMATS[0]
        self.widgets[1].format=settings.TIME_INPUT_FORMATS[0]

class BaseOrderForm(forms.ModelForm):

    datetime_start = forms.SplitDateTimeField(label=_('Date start'), required=True, 
                    help_text=_("when the order will be opened"), widget=GFSplitDateTimeWidget, initial=gf_now)

    datetime_end = forms.SplitDateTimeField(label=_('Date end'), required=False, 
                    help_text=_("when the order will be closed"), widget=GFSplitDateTimeWidget)

    delivery_datetime = forms.SplitDateTimeField(required=False, label=_('Delivery on/at'), widget=GFSplitDateTimeWidget)

    delivery_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)
    withdrawal_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)

    def __init__(self, request, *args, **kw):
        #Strip request arg
        super(BaseOrderForm, self).__init__(*args, **kw)
        self.fields['delivery_referrer'].queryset = request.resource.gas.persons
        self.fields['withdrawal_referrer'].queryset = request.resource.gas.persons
        self.__gas = request.resource.gas

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
            p = getattr(self.__gas.config, "%s_place" % name)

        d, created = klass.objects.get_or_create(date=ddt, place=p)
        return d
        
    def get_delivery(self):
        return self.get_appointment_instance('delivery', Delivery)

    def get_withdrawal(self):
        return self.get_appointment_instance('withdrawal', Withdrawal)

    def save(self):
        if self.cleaned_data.get('withdrawal_referrer'):
            pr = ParamRole.get_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self.instance.withdrawal)
            try:
                ppr = PrincipalParamRoleRelation.objects.get(role=pr)
                u = self.cleaned_data['withdrawal_referrer'].user
                if ppr.user != u:
                    ppr.user = u
                    ppr.save()
                
            except PrincipalParamRoleRelation.DoesNotExist:
                PrincipalParamRoleRelation.objects.create(role=pr, user=self.cleaned_data['withdrawal_referrer'].user)

        if self.cleaned_data.get('delivery_referrer'):
            pr = ParamRole.get_role(GAS_REFERRER_DELIVERY, delivery=self.instance.delivery)
            try:
                ppr = PrincipalParamRoleRelation.objects.get(role=pr)
                u = self.cleaned_data['delivery_referrer'].user
                if ppr.user != u:
                    ppr.user = u
                    ppr.save()
                
            except PrincipalParamRoleRelation.DoesNotExist:
                PrincipalParamRoleRelation.objects.create(role=pr, user=self.cleaned_data['delivery_referrer'].user)

        super(BaseOrderForm, self).save()

#-------------------------------------------------------------------------------

class AddOrderForm(BaseOrderForm):

    supplier = forms.ModelChoiceField(label=_('Supplier'), queryset=Supplier.objects.none(), required=True)
    delivery_terms = forms.CharField(label=_('Delivery terms'), required=False, widget=widgets.Textarea)

    def __init__(self, request, *args, **kw):

        super(AddOrderForm, self).__init__(request, *args, **kw)

        suppliers = request.resource.suppliers
        self.fields['supplier'].queryset = suppliers 
        self.fields['supplier'].initial = suppliers[0] 
        self.__gas = request.resource.gas

    def save(self):
        pact = GASSupplierSolidalPact.objects.get( \
            supplier=self.cleaned_data['supplier'],
            gas=self.__gas
        )
        self.instance.pact = pact

        if self.cleaned_data.get('delivery_datetime'):
            d = self.get_delivery()
            self.instance.delivery =  d
                       
        if self.cleaned_data.get('withdrawal_datetime'):
            w = self.get_withdrawal()
            self.instance.withdrawal =  w
               
        return super(AddOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ['supplier', 'datetime_start', 'datetime_end']

        gf_fieldsets = [(None, { 
            'fields' : ['supplier', 
                            ('datetime_start', 'datetime_end'), 
                            ('delivery_datetime', 'delivery_referrer'),
                        'delivery_terms'
            ] 
        })]

#-------------------------------------------------------------------------------

class EditOrderForm(BaseOrderForm):

    delivery_terms = forms.CharField(label=_('Delivery terms'), required=False, widget=widgets.Textarea)

    def save(self):

        if self.cleaned_data.get('delivery_datetime'):
            d = self.get_delivery()
            self.instance.delivery =  d
               
        if self.cleaned_data.get('withdrawal_datetime'):
            w = self.get_withdrawal()
            self.instance.withdrawal =  w
               
        return super(EditOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ['datetime_start', 'datetime_end']

        gf_fieldsets = [(None, { 
            'fields' : [ ('datetime_start', 'datetime_end'), 
                         ('delivery_referrer', 'withdrawal_referrer'), 
                        'delivery_terms'
            ] 
        })]

def form_class_factory_for_request(request, base):
    """Return appropriate form class basing on GAS configuration
    and other request parameters if needed"""

    fields = copy.deepcopy(base.Meta.fields)
    gf_fieldsets = copy.deepcopy(base.Meta.gf_fieldsets)
    attrs = {}
    gas = request.resource.gas

    if gas.config.can_change_delivery_place_on_each_order:
        gf_fieldsets[0][1]['fields'].append(('delivery_city', 'delivery_addr_or_place'))
        attrs.update({
            'delivery_city' : forms.CharField(required=True, label=_('Delivery city'), initial=gas.city),
            'delivery_addr_or_place': forms.CharField(required=True, label=_('Delivery address or place'), initial=gas.headquarter),
        })

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
                #log.debug("ho aggiornato un ordine gasista")

        elif self.cleaned_data.get('ordered_amount'):
                gssop = GASSupplierOrderProduct.objects.get(pk=self.cleaned_data.get('gssop_id'))
                #retrieve if yet exist. Security to ensure non duplicate entry into database
                #But this is done into GASMemberOrder Model with set unique_together
                gmo = GASMemberOrder(
                        ordered_product = gssop,
                        ordered_price = self.cleaned_data.get('ordered_price'),
                        ordered_amount = self.cleaned_data.get('ordered_amount'),
                        purchaser = self.__gm,
                )
                gmo.save()

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

    def save(self):

        id = self.cleaned_data.get('id')
        gm_id = self.cleaned_data.get('id')
        gsop_id = self.cleaned_data.get('gsop_id')
        ordered_amount = self.cleaned_data.get('ordered_amount')
        ordered_price = self.cleaned_data.get('ordered_price')
        enabled = self.cleaned_data.get('enabled')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
#            if gm_id and gm_id != gmo.purchaser.pk:
#                print "Qualcosa non va con: GASmember"
#                return ""
            gmo.ordered_price = ordered_price
            gmo.ordered_amount = ordered_amount
            #log.debug("BasketGASMemberOrderForm (%s) enabled = %s" % (gmo.pk,enabled))
            if gmo.ordered_amount == 0:
                gmo.delete()
                log.debug("Basket STO CANCELLANDO un ordine gasista da widget quantita")
            elif enabled:
                gmo.delete()
                log.debug("Basket STO CANCELLANDO un ordine gasista da check enabled")
            else:
                gmo.save()
                log.debug("Basket ho aggiornato un ordine gasista")

