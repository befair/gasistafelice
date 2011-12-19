#!/usr/local/bin/python
# coding: utf-8
import os, sys

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.db import transaction

from gasistafelice.base.models import Person
from gasistafelice.gas.models import GAS, GASMember, GASMemberOrder, GASSupplierOrder, GASSupplierSolidalPact
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
        #refs = gas.cash_referrers
        #if refs and request.user in refs:
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__order.gas)
        ):
            log.debug("PermissionDenied %s in cash order form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot update GASMembers cash!")

        if not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied("order is not in good state!")

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
                        gm, amounted, refs, self.__order
                    )

            else:
                gm.gas.accounting.withdraw_from_member_account(gm, amounted, refs, self.__order)


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

EcoGASMemberRechargeFormSet = formset_factory(
                                form=EcoGASMemberRechargeForm,
                                formset=BaseFormSetWithRequest,
                                extra=0 #must be 0 no add form
                          )

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

EcoGASMemberFeeFormSet = formset_factory(
                                form=EcoGASMemberFeeForm,
                                formset=BaseFormSetWithRequest,
                                extra=0 #must be 0 no add form
                          )




#-------------------------------------------------------------------------------

EURO_HTML = '&euro;'  # &amp;euro; &#8364; &euro;  &#128;  &#x80;
EURO_LABEL = 'Eur.'  # €  &amp;euro; &#8364; &euro;  &#128;  &#x80;

class InvoiceOrderForm(forms.Form):

    #order_info = forms.CharField(label=_('Information'), required=False, widget=widgets.TextInput())
    amount = CurrencyField(label=_('Invoice'), required=True, max_digits=8, decimal_places=2)
    note = forms.CharField(label=_('Note'), required=False, widget=forms.Textarea)

    def __init__(self, request, *args, **kw):

        log.debug("InvoiceOrderForm")

        super(InvoiceOrderForm, self).__init__(*args, **kw)

        #SOLIDAL PACT
        self.__order = request.resource.order
        if self.__order:
            #set order informations
            stat = ("%(state)s - Fam: %(fam)s (euro)s --> Fatt: %(fatt)s (euro)s --> Pag: %(eco)s (euro)s" % {
                'fam'    : "%.2f" % round(self.__order.tot_price, 2)
                , 'fatt' : "%.2f" % (self.__order.invoice_amount or 0)
                , 'eco'  : "%.2f" % round(self.__order.tot_curtail, 2)
                , 'state'  : self.__order.current_state.name
            })
            #    , 'euro' : EURO
            #self.fields['order_info'].initial = stat
            self.fields['amount'].help_text = stat.replace('(euro)s',EURO_HTML)


            #set invoice data
            if self.__order.invoice_amount:
                self.fields['amount'].initial = "%.2f" % round(self.__order.invoice_amount, 2)
            if self.__order.invoice_note:
                self.fields['note'].initial = self.__order.invoice_note
        #self.fields['note'].widget.attrs['class'] = 'input_long'
        self.fields['amount'].widget.attrs['class'] = 'input_payment'

        self.fields['amount'].widget.attrs['class'] = 'input_payment'
        if not self.__order.is_closed():
            self.fields['amount'].widget.attrs['readonly'] = True
            self.fields['amount'].widget.attrs['disabled'] = 'disabled'

        self.__loggedusr = request.user
        self.__gas = self.__order.gas
        
    def clean(self):

        cleaned_data = super(InvoiceOrderForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['invoice_amount'] = abs(cleaned_data['amount'])
        except KeyError:
            log.debug("InvoiceOrderForm: cannot retrieve order identifier. FORM ATTACK!")
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

        if not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied("order is not in good state!")

        self.__order.invoice_amount = self.cleaned_data['invoice_amount']
        self.__order.invoice_note = self.cleaned_data['note']
        #print"Invoice amount %s---" % self.__order.invoice_amount

        try:
            self.__order.save()
        except ValueError, e:
            print "retry later " +  e.message
        else:
            #Update State if possible
            self.__order.control_economic_state()
            #print"Invoice saved"

#-------------------------------------------------------------------------------


class InsoluteOrderForm(forms.Form):

#    orders2 = forms.ModelMultipleChoiceField(label=_("Insolute order(s)"), 
#        queryset=GASSupplierOrder.objects.none(), required=True, widget=forms.CheckboxSelectMultiple
#    )
    orders = forms.MultipleChoiceField(label=_("Insolute order(s)"), required=True, widget=forms.CheckboxSelectMultiple)
    amount = CurrencyField(label=_('Payment'), required=True, max_digits=8, decimal_places=2)
    note = forms.CharField(label=_('Causale'), required=False, widget=forms.TextInput)

    def __init__(self, request, *args, **kw):

        log.debug("InsoluteOrderForm")

        super(InsoluteOrderForm, self).__init__(*args, **kw)

        #SOLIDAL PACT
        self.__order = request.resource.order
        self.__gas = request.resource.gas

        if self.__order:

            #set insolute data and informations
            yet_payed, descr =self.__gas.accounting.get_supplier_order_data(self.__order)
            if yet_payed > 0:
                self.fields['amount'].initial = "%.2f" % round(yet_payed, 2)
                self.fields['note'].initial = descr

            insolutes = self.__order.insolutes
            _choice = []
            tot_ordered = 0
            tot_invoiced = 0
            tot_eco_entries = 0
            stat = ''
            for ins in insolutes:
                tot_ordered += ins.tot_price
                tot_invoiced += ins.invoice_amount or 0
                tot_eco_entries += ins.tot_curtail
                stat = _("%(state)s -Fam: %(fam)s (euro)s --> Fatt: %(fatt)s (euro)s --> Pag: %(eco)s (euro)s" % {
                    'fam'    : "%.2f" % round(ins.tot_price, 2)
                    , 'fatt' : "%.2f" % round(ins.invoice_amount or 0, 2)
                    , 'eco'  : "%.2f" % round(ins.tot_curtail, 2)
                    , 'state'  : ins.current_state.name
                    } )
                _choice.append((ins.pk, stat.replace('(euro)s',EURO_LABEL)))
#            self.fields['orders2'].queryset = insolutes
            self.fields['orders'].choices = _choice

            #set order informations
            stat = _("%(state)s - Total --> Fam: %(fam)s (euro)s --> Fatt: %(fatt)s (euro)s --> Pag: %(eco)s (euro)s" % {
                'fam'    : "%.2f" % round(tot_ordered, 2)
                , 'fatt' : "%.2f" % round(tot_invoiced, 2)
                , 'eco'  : "%.2f" % round(tot_eco_entries, 2)
                , 'state'  : self.__order.current_state.name
            })
            self.fields['amount'].help_text = stat.replace('(euro)s',EURO_HTML)

        self.fields['amount'].widget.attrs['class'] = 'input_payment'
        if not self.__order.is_unpaid() and not self.__order.is_closed():
            self.fields['amount'].widget.attrs['readonly'] = True
            self.fields['amount'].widget.attrs['disabled'] = 'disabled'

        self.__loggedusr = request.user
        self.__gas = self.__order.gas

    def clean(self):

        cleaned_data = super(InsoluteOrderForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['insolute_amount'] = abs(cleaned_data['amount'])
        except KeyError:
            #FIXME: if no gmo we don't have to show button.
            log.debug("InsoluteOrderForm: cannot retrieve order identifier. FORM ATTACK!")
            raise

        try:
            cleaned_data['orders_to_pay'] = cleaned_data['orders']
        except KeyError:
            log.debug("InsoluteOrderForm: cannot retrieve orders identifiers. FORM ATTACK!")
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

        if not self.__order.is_unpaid() and not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed or unpaid (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied("order is not in good state!")

        p_amount = self.cleaned_data['insolute_amount']
        p_note = self.cleaned_data['note']
        #print"insolute amount %s---" % p_amount
        #refs=[self.__order]
        refs=[]
        insolutes = self.cleaned_data['orders_to_pay']
        if insolutes:
            for ins_pk in insolutes:
                try:
                    _ins = GASSupplierOrder.objects.get(pk=ins_pk)
                except GASSupplierOrder.DoesNotExist:
                    log.debug("InsoluteOrderForm: cannot retrieve order instance. Identifier (%s)." % ins_pk)
                    raise
                else:
                    if _ins and (_ins.is_unpaid() or _ins.is_closed()):
                        refs.append(_ins)
            if len(refs) > 0:
                try:
                    self.__gas.accounting.pay_supplier_order(order=self.__order, amount=p_amount, descr=p_note, refs=refs)
                except ValueError, e:
                    print "retry later " +  e.message
                else:
                    #print"Insolute(%s) saved " % len(refs)
                    for _order in refs:
                        #Update State if possible
                        _order.control_economic_state()



#-------------------------------------------------------------------------------


class BalanceForm(forms.Form):

    balance = CurrencyField(label=_('Balance'), required=True, max_digits=8, decimal_places=2)

    def __init__(self, request, *args, **kw):

        log.debug("BalanceForm")

        super(BalanceForm, self).__init__(*args, **kw)
        self.__gas_list = request.resource.gas_list

        #self.fields['note'].widget.attrs['class'] = 'input_long'
        eco_state = request.resource.balance
        eco_class = "Negative"
        if eco_state:
            if eco_state > 20:
                eco_class = "Plus"
            elif eco_state < 20 and eco_state >= 0:
                eco_class = "Alert"
        self.fields['balance'].initial = ("%.2f" % round(request.resource.balance, 2)).replace('.','€')
        self.fields['balance'].widget.attrs['class'] = 'balance input_payment ' + eco_class
        self.__loggedusr = request.user

#-------------------------------------------------------------------------------

class BalanceGASForm(BalanceForm):

    Wallet_gasmembers = CurrencyField(label=_('Wallet GASMembers'), required=False, max_digits=8, decimal_places=2)
    Wallet_suppliers = CurrencyField(label=_('Wallet Suppliers'), required=False, max_digits=8, decimal_places=2)

    amount = CurrencyField(label=_('Operation'), required=True, max_digits=8, decimal_places=2,
help_text = _('define the amount with the sign - to debit money from this account'), error_messages={'required': _(u'You must insert an postive or negatibe amount for the operation')})
    note = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
help_text = _('Register the reason of this movment'), error_messages={'required': _(u'You must declare the causal of the movment')})
#    target = forms.ModelChoiceField(label=_("Account"), queryset=Account.objects.none(), required=False)
    target = forms.ChoiceField(choices = [('0',_('only GAS')), ('1',_('GAS <--> GASMember')), ('2',_('GAS <--> Supplier'))], widget=forms.RadioSelect, 
help_text="define the target of the operation")
    pact = forms.ModelChoiceField(label=_('pact'), queryset=GASSupplierSolidalPact.objects.none(), required=False, error_messages={'required': _(u'You must select one pact (or create it in your GAS details if empty)')})
    person = forms.ModelChoiceField(queryset=Person.objects.none(), required=False, label=_("Person"))

    def __init__(self, request, *args, **kw):

        log.debug("BalanceGASForm")
        super(BalanceGASForm, self).__init__(request, *args, **kw)

        self.fields['target'].initial = '0'
        self.__gas = request.resource.gas

        eco_state = request.resource.balance_gasmembers
        eco_class = "Negative"
        if eco_state:
            if eco_state > 20:
                eco_class = "Plus"
            elif eco_state < 20 and eco_state >= 0:
                eco_class = "Alert"
        self.fields['Wallet_gasmembers'].initial = ("%.2f" % round(eco_state, 2)).replace('.','€')
        self.fields['Wallet_gasmembers'].widget.attrs['class'] = 'balance input_payment ' + eco_class

        eco_state = request.resource.balance_suppliers
        eco_class = "Negative"
        if eco_state:
            if eco_state > 20:
                eco_class = "Plus"
            elif eco_state < 20 and eco_state >= 0:
                eco_class = "Alert"
        self.fields['Wallet_suppliers'].initial = ("%.2f" % round(eco_state, 2)).replace('.','€')
        self.fields['Wallet_suppliers'].widget.attrs['class'] = 'balance input_payment ' + eco_class

        self.__loggedusr = request.user

        # SOLIDAL PACT
        pacts = request.resource.pacts
        if pacts and pacts.count() > 0:
            self.fields['pact'].queryset = pacts
#            self.fields['pact'].initial = pacts[0]

        # MEMBERS
        gms = request.resource.gasmembers
        if gms and gms.count() > 0:
            self.fields['person'].queryset = gms

    def clean(self):

        cleaned_data = super(BalanceGASForm, self).clean()
        print("cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['economic_amount'] = abs(cleaned_data['amount'])
        except KeyError:
            log.debug("BalanceGASForm: cannot retrieve economic identifier. FORM ATTACK!")
            raise

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        if not self.__gas:
            return

        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):
            log.debug("PermissionDenied %s in economic operation form" % self.__loggedusr)
            raise PermissionDenied("BalanceGASForm: You are not a cash_referrer, you cannot do economic operation!")
#        #Do economic work
#        try:
#            self.economic_operation()
#        except ValueError, e:
#            print "retry later " +  e.message

