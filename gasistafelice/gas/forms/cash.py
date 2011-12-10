from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.db import transaction

from gasistafelice.gas.models import GAS, GASMember, GASMemberOrder, GASSupplierOrder
from gasistafelice.supplier.models import Supplier

from django.forms.formsets import formset_factory
from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.lib.fields.forms import CurrencyField

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from flexi_auth.models import ObjectWithContext
from gasistafelice.consts import CASH  #Permission
from gasistafelice.consts import GAS_MEMBER  #Role

from datetime import tzinfo, timedelta, datetime

import logging
log = logging.getLogger(__name__)

from django.core import validators
from django.core.exceptions import ValidationError

#-------------------------------------------------------------------------------


class EcoGASMemberForm(forms.Form):
    """Return form class for row level operation on cash ordered data
    use in Curtail
    Movement between GASMember.account --> GAS.account
    """

    gm_id = forms.IntegerField(widget=forms.HiddenInput)
    original_amounted = CurrencyField(required=False, widget=forms.HiddenInput())
    amounted = CurrencyField(required=False, initial=0) #, widget=forms.TextInput())

    #TODO: domthu: note and delete
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        log.debug("    --------------       EcoGASMemberForm")
        super(EcoGASMemberForm, self).__init__(*args, **kw)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__order = request.resource.order

    def clean(self):

        cleaned_data = super(EcoGASMemberForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug("EcoGASMemberForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug("EcoGASMemberForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__order.gas)
        ):

            log.debug("PermissionDenied %s in cash order form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        gm = self.cleaned_data['gasmember']

        #TODO: Seldon or Fero. Control if Order is in the rigth Workflow STATE

        #Do economic work
        amounted = self.cleaned_data.get('amounted')

        if amounted:
            # This kind of amount is ever POSITIVE!
            amounted = abs(amounted)

            refs = [gm, self.__order]

            original_amounted = self.cleaned_data['original_amounted']

            if original_amounted is not None:
                # A ledger entry already exists
                if original_amounted != amounted:
                    gm.gas.accounting.withdraw_from_member_account_update(
                        gm, amounted, refs
                    )

            else:
                gm.gas.accounting.withdraw_from_member_account(gm, amounted, refs)


class EcoGASMemberRechargeForm(forms.Form):
    """Return form class for row level operation on cash ordered data
    use in Recharge 
    Movement between GASMember.account --> GAS.GASMember.account
    """

    gm_id = forms.IntegerField(widget=forms.HiddenInput)
    recharged = CurrencyField(required=False, initial=0)

    #TODO: domthu: note and delete
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        log.debug("    --------------       EcoGASMemberRechargeForm")
        super(EcoGASMemberRechargeForm, self).__init__(*args, **kw)
        self.fields['recharged'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__gas = request.resource.gas

    def clean(self):

        cleaned_data = super(EcoGASMemberRechargeForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug("EcoGASMemberRechargeForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug("EcoGASMemberRechargeForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        # Do economic work
        recharged = self.cleaned_data.get('recharged')
        if not recharged:
            # Skip without doing anything else
            return

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):

            log.debug("PermissionDenied %s in cash recharge form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        gm = self.cleaned_data['gasmember']
        if not gm in self.__gas.gasmembers:
            log.debug("PermissionDenied %s in cash recharge for gasmember %s not in this gas %s" % self.__loggedusr, gm, self.__gas)
            raise PermissionDenied("You are not a cash_referrer for the GAS of the gasmember, you cannot recharge GASMembers cash!")

        # This kind of amount is ever POSITIVE!
        gm.person.accounting.do_recharge(self.__gas, recharged)

def get_year_choices():
    #DOMTHU: return [ ('2001', '2001'), ('2002', '2002'), ('2003', '2003')]
    dt = datetime.now()
    year = timedelta(days=365)
    last_year = (dt-year).strftime('%Y')
    actual_year = dt.strftime('%Y')
    next_year = (dt+year).strftime('%Y')
    return [ ('0', '----'), (last_year, last_year), (actual_year, actual_year), (next_year, next_year)]


class EcoGASMemberFeeForm(forms.Form):
    """Return form class for row level operation on cash ordered data.

    Used in Fee Movement between GASMember.account --> GAS.GASMember.account
    """

    gm_id = forms.IntegerField(widget=forms.HiddenInput)
    feeed = forms.BooleanField(required=False)
    #year = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=get_year_choices())
    year = forms.ChoiceField(required=False, widget=forms.Select, choices=get_year_choices())

    #TODO: domthu: note
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        log.debug("    --------------       EcoGASMemberFeeForm")
        super(EcoGASMemberFeeForm, self).__init__(*args, **kw)
        self.fields['feeed'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__gas = request.resource.gas

    def clean(self):

        cleaned_data = super(EcoGASMemberFeeForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug("EcoGASMemberFeeForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug("EcoGASMemberFeeForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        feeed = self.cleaned_data.get('feeed')
        year = self.cleaned_data.get('year')

        if not (feeed and year):
            # Skip without doing anything else
            return

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):

            log.debug("PermissionDenied %s in cash fee form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        gm = self.cleaned_data['gasmember']
        if not gm in self.__gas.gasmembers:
            log.debug("PermissionDenied %s in cash fee for gasmember %s not in this gas %s" % self.__loggedusr, gm, self.__gas)
            raise PermissionDenied("You are not a cash_referrer for the GAS of the gasmember, you cannot register fee GASMembers cash!")

        gm.person.accounting.pay_membership_fee(self.__gas, year)




#-------------------------------------------------------------------------------


#class CashOrderForm(forms.ModelForm):
class CashOrderForm(forms.Form):

    log.debug("CashOrderForm")

    def __init__(self, request, *args, **kw):

        super(CashOrderForm, self).__init__(request, *args, **kw)

        #SOLIDAL PACT
        pact = request.resource.pact
        delivery = request.resource.delivery
#        ref = request.resource.referrer_person
#        if ref:
#            #control if queryset not empty.
#            self.fields['referrer_person'].initial = ref
#        if request.resource.datetime_end:
#            self.fields['datetime_end'].initial = request.resource.datetime_end
#        if delivery and delivery.date:
#            self.fields['delivery_datetime'].initial = delivery.date

    @transaction.commit_on_success
    def save(self):

#        if self.cleaned_data.get('delivery_datetime'):
#            d = self.get_delivery()
#            self.instance.delivery = d

#        if self.cleaned_data.get('withdrawal_datetime'):
#            w = self.get_withdrawal()
#            self.instance.withdrawal = w

        return super(CashOrderForm, self).save()

    class Meta:
        model = GASSupplierOrder
        fields = ['invoice_amount', 'invoice_note']

        gf_fieldsets = [(None, {
            'fields' : [ 'current_state'
                         , 'invoice_amount'
                         , 'invoice_note'
            ]
        })]

def form_class_factory_for_request(request, base):
    """Return appropriate form class basing on GAS configuration
    and other request parameters if needed"""

    log.debug("CashOrderForm--> form_class_factory_for_request")
    fields = copy.deepcopy(base.Meta.fields)
    gf_fieldsets = copy.deepcopy(base.Meta.gf_fieldsets)
    attrs = {}
    order = request.resource.order

    if order:

#        refs = gas.cash_referrers
#        if refs and request.user in refs:
#            gf_fieldsets[0][1]['fields'].append('delivery_cost')

        attrs.update(Meta=type('Meta', (), {
            'model' : GASSupplierOrder,
            'fields' : fields,
            'gf_fieldsets' : gf_fieldsets
        }))
    return type('Custom%s' % base.__name__, (base,), attrs)


#-------------------------------------------------------------------------------
