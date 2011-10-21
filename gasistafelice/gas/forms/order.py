from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.gas.models.proxy import GASSupplierOrder, GASSupplierSolidalPact
from gasistafelice.gas.models import GASMemberOrder
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

def today():
    return datetime.date.today().strftime(settings.DATE_FMT)

class BaseOrderForm(forms.ModelForm):

    date_start = forms.DateField(label=_('Date start'), required=True, 
                    help_text=_("when the order will be opened"), widget=admin_widgets.AdminDateWidget, initial=today)
    date_end = forms.DateField(label=_('Date end'), required=False, 
                    help_text=_("when the order will be closed"), widget=admin_widgets.AdminDateWidget)

    delivery_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)
    withdrawal_referrer = forms.ModelChoiceField(queryset=Person.objects.none(), required=False)

    def __init__(self, request, *args, **kw):
        #Strip request arg
        super(BaseOrderForm, self).__init__(*args, **kw)
        self.fields['delivery_referrer'].queryset = request.resource.gas.persons
        self.fields['withdrawal_referrer'].queryset = request.resource.gas.persons

    def get_appointment_instance(self, name, klass):

        ddt = self.cleaned_data['%s_datetime' % name]
        dc = self.cleaned_data['%s_city' % name] 
        dp = self.cleaned_data['%s_addr_or_place' % name]
        try:
            p = Place.objects.get(city=dc, name__icontains=dp)
        except Place.DoesNotExist:
            try:
                p = Place.objects.get(city=dc, addr__icontains=dp)
            except Place.DoesNotExist:
                p = Place(city=dc, name=dp)
                p.save()

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

    supplier = forms.ModelChoiceField(label=_('Supplier'), queryset=Supplier.objects.none())
    delivery_terms = forms.CharField(label=_('Delivery terms'), required=False, widget=widgets.Textarea)

    def __init__(self, request, *args, **kw):
        super(AddOrderForm, self).__init__(request, *args, **kw)
        self.fields['supplier'].queryset = request.resource.suppliers
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
        fields = ['supplier', 'date_start', 'date_end']

        gf_fieldsets = [(None, { 
            'fields' : ['supplier', 
                            ('date_start', 'date_end'), 
                            ('delivery_referrer', 'withdrawal_referrer'), 
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
        fields = ['date_start', 'date_end']

        gf_fieldsets = [(None, { 
            'fields' : [ ('date_start', 'date_end'), 
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
        gf_fieldsets[0][1]['fields'].append(('delivery_datetime', 'delivery_city', 'delivery_addr_or_place'))
        attrs.update({
            'delivery_datetime' : forms.SplitDateTimeField(required=False, label=_('Delivery on/at'), widget=admin_widgets.AdminSplitDateTime),
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

    def __init__(self, request, *args, **kw):
        super(GASSupplierOrderProductForm, self).__init__(*args, **kw)
        self.__order = request.resource.order

    def save(self):

        if not self.cleaned_data.get('enabled'):
            GASSupplierOrderProduct.objects.get(pk=self.cleaned_data['id']).delete()


GASSupplierOrderProductFormSet = formset_factory(
                                form=GASSupplierOrderProductForm, 
                                formset=BaseFormSetWithRequest, 
                                extra=0
                          )
#-------------------------------------------------------------------------------


class SingleGASMemberOrderForm(forms.Form):
    """Return form class for row level operation on GSOP datatable"""

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    #log.debug('SingleGASMemberOrderForm (%d)' % id)
    gssop_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    ordered_amount = forms.DecimalField(required=False, initial=0)
    ordered_price = forms.DecimalField(required=False, widget=forms.HiddenInput)

    def __init__(self, request, *args, **kw):
        super(SingleGASMemberOrderForm, self).__init__(*args, **kw)
        self.__gm = request.resource.gasmember

    def save(self):

        id = self.cleaned_data.get('id')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
            gmo.ordered_price = self.cleaned_data.get('ordered_price')
            gmo.ordered_amount = self.cleaned_data.get('ordered_amount')
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
    gm_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    gsop_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    ordered_amount = forms.DecimalField(required=False, initial=0)
    ordered_price = forms.DecimalField(required=False, widget=forms.HiddenInput)
    #FIXME: integrate BooleanField in this class and remove DeleteGASMemberOrderForm 
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
            if gmo.ordered_amount == 0 or enabled:
            #if gmo.ordered_amount == 0:
                gmo.delete()
                #log.debug("STO CANCELLANDO un ordine gasista da widget quantita")
            else:
                gmo.save()
                #log.debug("ho aggiornato un ordine gasista")

#        elif self.cleaned_data.get('ordered_amount'):

class DeleteGASMemberOrderForm(forms.Form):

    id = forms.IntegerField(required=True, widget=forms.HiddenInput)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kw):
        super(DeleteGASMemberOrderForm, self).__init__(*args, **kw)

    def save(self):
        id = self.cleaned_data.get('id')
        if id:
            gmo = GASMemberOrder.objects.get(pk=id)
            enabled = self.cleaned_data.get('enabled')
            if enabled:
                gmo.delete()


DeleteGASMemberOrderFormSet = formset_factory(
                                form=DeleteGASMemberOrderForm, 
                                formset=BaseFormSetWithRequest, 
                                extra=0
                          )

