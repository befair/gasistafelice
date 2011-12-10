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
    amounted = CurrencyField(required=False, initial=0, max_digits=8, decimal_places=2) #, widget=forms.TextInput())

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
    recharged = CurrencyField(required=False, initial=0, max_digits=8, decimal_places=2)

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

    order_info = forms.CharField(label=_('Information'), required=False, widget=widgets.TextInput())
    amount = CurrencyField(label=_('Invoice'), required=True, max_digits=8, decimal_places=2)
    note = forms.CharField(label=_('Note'), required=False, widget=forms.Textarea)

    def __init__(self, request, *args, **kw):

        log.debug("CashOrderForm")

        super(CashOrderForm, self).__init__(*args, **kw)

        #SOLIDAL PACT
        self.__order = request.resource.order
        if self.__order:
            #set order informations
            self.fields['order_info'].initial = ("Fam: %(fam)s &euro; --> Fatt: %(fatt)s &euro; --> Pag: %(eco)s &euro;" % {
                'fam' : "%.2f" % round(self.__order.tot_price, 2)
                , 'fatt' : "%.2f" % (self.__order.invoice_amount or 0)
                , 'eco' : "%.2f" % round(self.__order.tot_curtail, 2)
            })

            #set invoice data
            if self.__order.invoice_amount:
                self.fields['amount'].initial = self.__order.invoice_amount
            if self.__order.invoice_note:
                self.fields['note'].initial = self.__order.invoice_note

        self.fields['order_info'].widget.attrs['class'] = 'info input_long'
        self.fields['order_info'].widget.attrs['readonly'] = True
        self.fields['order_info'].widget.attrs['disabled'] = 'disabled'
        self.__loggedusr = request.user
        self.__gas = self.__order.gas
        
    def clean(self):

        cleaned_data = super(CashOrderForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['invoice'] = abs(cleaned_data['amount'])
        except KeyError:
            log.debug("CashOrderForm: cannot retrieve order identifier. FORM ATTACK!")
            raise 
        except GASSupplierOrder.DoesNotExist:
            log.debug("CashOrderForm: cannot retrieve order instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        return cleaned_data

    @transaction.commit_on_success
    def save(self):
        #raise ValueError("prova")

        #Do economic work
        if not self.__order:
            return

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):

            log.debug("PermissionDenied %s in cash invoice receipt form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot manage receipt invoice cash!")

        self.__order.invoice_amount = self.cleaned_data['amount']
        self.__order.invoice_note = self.cleaned_data['note']
        
        try:
            self.__order.save()
        except ValueError, e:
            print "retry later " +  e.message
        else:
            print "Invoice saved"

#-------------------------------------------------------------------------------


class InsoluteOrderForm(forms.Form):

    order_info = forms.CharField(label=_('Information'), required=False, widget=widgets.TextInput())
    orders = forms.ModelMultipleChoiceField(label=_("Insolute order(s)"), 
        queryset=GASSupplierOrder.objects.none(), required=True, widget=forms.CheckboxSelectMultiple
    )
    orders2 = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    amount = CurrencyField(label=_('Payment'), required=True, max_digits=8, decimal_places=2)
    note = forms.CharField(label=_('Causale'), required=False, widget=forms.TextInput)

    def __init__(self, request, *args, **kw):

        log.debug("InsoluteOrderForm")

        super(InsoluteOrderForm, self).__init__(*args, **kw)

        #SOLIDAL PACT
        self.__order = request.resource.order
        if self.__order:

            #set insolute data
            if self.__order.invoice_amount:
                self.fields['amount'].initial = self.__order.invoice_amount
            if self.__order.invoice_note:
                self.fields['note'].initial = self.__order.invoice_note

            insolutes = self.__order.insolutes
            _choice = []
            tot_ordered = 0
            tot_invoiced = 0
            tot_eco_entries = 0
            for ins in insolutes:
                tot_ordered += ins.tot_price
                tot_invoiced += ins.invoice_amount or 0
                tot_eco_entries += ins.tot_curtail
                _choice.append((ins.pk, ("Total. Fam: %(fam)s &euro; --> Fatt: %(fatt)s &euro; --> Fatt: %(eco)s &euro;" % {
                'fam' : "%.2f" % round(ins.tot_price, 2)
                , 'fatt' : "%.2f" % round(ins.invoice_amount or 0, 2)
                , 'eco' : "%.2f" % round(ins.tot_curtail, 2)
            } )))
            self.fields['orders'].queryset = insolutes
            self.fields['orders2'].choices = _choice

            #set order informations  &euro; &#128; 	&#x80;
            self.fields['order_info'].initial = ("Total. Fam: %(fam)s &euro; --> Fatt: %(fatt)s &euro; --> Fatt: %(eco)s &euro;" % {
                'fam' : "%.2f" % round(tot_ordered, 2)
                , 'fatt' : "%.2f" % round(tot_invoiced, 2)
                , 'eco' : "%.2f" % round(tot_eco_entries, 2)
            } )#.encode('iso-8859-1') ('utf-8')
            self.fields['order_info'].widget.attrs['class'] = 'info input_long'
            self.fields['order_info'].widget.attrs['readonly'] = True
            self.fields['order_info'].widget.attrs['disabled'] = 'disabled'

        self.__loggedusr = request.user
        self.__gas = self.__order.gas
        
    def clean(self):

        cleaned_data = super(InsoluteOrderForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['invoice'] = abs(cleaned_data['amount'])
        except KeyError:
            log.debug("InsoluteOrderForm: cannot retrieve order identifier. FORM ATTACK!")
            raise 
        except GASSupplierOrder.DoesNotExist:
            log.debug("InsoluteOrderForm: cannot retrieve order instance. Identifier (%s)." % cleaned_data['gm_id'])
            raise
           
        return cleaned_data

    @transaction.commit_on_success
    def save(self):
        #raise ValueError("prova")

        #Do economic work
        if not self.__order:
            return

        #Control logged user
        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):

            log.debug("PermissionDenied %s in cash insolute form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot manage insolute order cash!")

        self.__order.invoice_amount = self.cleaned_data['amount']
        self.__order.invoice_note = self.cleaned_data['note']
        
        try:
            self.__order.save()
        except ValueError, e:
            print "retry later " +  e.message
        else:
            print "Invoice saved"



#-------------------------------------------------------------------------------
