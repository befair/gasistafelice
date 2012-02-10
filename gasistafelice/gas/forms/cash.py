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
from gasistafelice.lib.widgets import DateFormatAwareWidget

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.lib.fields.forms import CurrencyField

from flexi_auth.models import ParamRole, PrincipalParamRoleRelation
from flexi_auth.models import ObjectWithContext
from gasistafelice.consts import (
        CASH,  #Permission
        GAS_MEMBER,  #Role
        INCOME, EXPENSE  #Transactions
)

from datetime import tzinfo, timedelta, datetime, date

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
        log.debug("cleaned_data %s" % cleaned_data)
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
        log.debug("cleaned_data %s" % cleaned_data)
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
        log.debug("cleaned_data %s" % cleaned_data)
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
    amount = CurrencyField(label=_('Invoice'), required=True, max_digits=8, decimal_places=2,
        error_messages={'required': _(u'You must insert an postive amount for the operation')}
    )
    note = forms.CharField(label=_('Note'), required=False, widget=forms.Textarea)

    def __init__(self, request, *args, **kw):

        #log.debug("InvoiceOrderForm")

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

        if not self.__order.is_closed():
            self.fields['amount'].widget.attrs['readonly'] = True
            self.fields['amount'].widget.attrs['disabled'] = 'disabled'

        self.__loggedusr = request.user
        self.__gas = self.__order.gas
        
    def clean(self):

        cleaned_data = super(InvoiceOrderForm, self).clean()
        try:
            cleaned_data['invoice_amount'] = abs(cleaned_data['amount'])
            cleaned_data['invoice_note'] = cleaned_data['note']
        except KeyError, e:
            log.debug("InvoiceOrderForm: cannot retrieve invoice data: " +  e.message)
            raise

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        if not self.__order:
            return

        #Control logged user
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):
            log.debug("PermissionDenied %s in cash invoice receipt form" % self.__loggedusr)
            raise PermissionDenied("You are not a cash_referrer, you cannot manage receipt invoice cash!")

        if not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied("order is not in good state!")

        self.__order.invoice_amount = self.cleaned_data['invoice_amount']
        self.__order.invoice_note = self.cleaned_data['invoice_note']
        #log.debug("Invoice amount %s---" % self.__order.invoice_amount)

        try:
            self.__order.save()
        except ValueError, e:
            log.debug("retry later " +  e.message)
        else:
            #Update State if possible
            self.__order.control_economic_state()
            #log.debug("Invoice saved")

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
        log.debug("cleaned_data %s" % cleaned_data)
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
        #log.debug("insolute amount %s---" % p_amount)
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
                    log.debug("retry later " +  e.message)
                else:
                    #log.debug("Insolute(%s) saved " % len(refs))
                    for _order in refs:
                        #Update State if possible
                        _order.control_economic_state()


#-------------------------------------------------------------------------------

def get_eco_class(eco_state):
    eco_class = "negative"
    _sold = float(eco_state)
    if _sold > 20:
        eco_class = "positive"
    elif -10 < _sold and _sold < 10:
        eco_class = "stalled"
    return "balance " + eco_class

#-------------------------------------------------------------------------------

class BalanceForm(forms.Form):

    balance = CurrencyField(label=_('Balance'), required=True, max_digits=8, decimal_places=2)

    def __init__(self, request, *args, **kw):

        log.debug("BalanceForm")

        super(BalanceForm, self).__init__(*args, **kw)
        self.__gas_list = request.resource.gas_list

        #self.fields['note'].widget.attrs['class'] = 'input_long'
        eco_state = request.resource.balance
        eco_class = get_eco_class(eco_state)
        self.fields['balance'].initial = ("%.2f" % round(request.resource.balance, 2)).replace('.','€')
        self.fields['balance'].widget.attrs['class'] = eco_class
        self.__loggedusr = request.user

        # LF: Balance is a readonly field
        field_name = 'balance'
        self.fields[field_name].widget.attrs['readonly'] = True
        self.fields[field_name].widget.attrs['disabled'] = 'disabled'

#LF: balance and wallet_*  are always read-only so they MUST NOT be included in form...
class BalanceGASForm(BalanceForm):

    wallet_gasmembers = CurrencyField(label=_('Wallet GASMembers'), required=False, max_digits=8, decimal_places=2)
    wallet_suppliers = CurrencyField(label=_('Wallet Suppliers'), required=False, max_digits=8, decimal_places=2)

    def __init__(self, request, *args, **kw):

        log.debug("BalanceGASForm")
        super(BalanceGASForm, self).__init__(request, *args, **kw)
        eco_state = request.resource.balance_gasmembers
        eco_class = get_eco_class(eco_state)
        self.fields['wallet_gasmembers'].initial = ("%.2f" % round(eco_state, 2)).replace('.','€')
        self.fields['wallet_gasmembers'].widget.attrs['class'] = eco_class

        eco_state = request.resource.balance_suppliers
        eco_class = get_eco_class(eco_state)
        self.fields['wallet_suppliers'].initial = ("%.2f" % round(eco_state, 2)).replace('.','€')
        self.fields['wallet_suppliers'].widget.attrs['class'] = eco_class

        # Set readonly fields for wallet_*
        for field_name in ( 'wallet_gasmembers' , 'wallet_suppliers'):
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['disabled'] = 'disabled'


#-------------------------------------------------------------------------------

#LF: other stuff now may be commented because we have to think
# about more intuitive way to do these operations
#UGLY: fixme when succeed to open popup for cash referrer operations
#class TransationGASForm(forms.Form):
class TransationGASForm(BalanceGASForm):

    amount = CurrencyField(label=_('Operation'), required=True, max_digits=8, decimal_places=2,
        help_text = _('Insert the amount of money (no sign)'),
        error_messages = {'required': _('You must insert an postive or negative amount for the operation')}
    )

    target = forms.ChoiceField(required=True, 
        choices = [(INCOME,_('Income: Event, Donate, Sponsor, Fund... +GAS')), (EXPENSE,_('Expense: Expenditure, Invoice, Bank, Administration, Event, Rent... -GAS'))], 
        widget=forms.RadioSelect, help_text="define the type of the operation", 
        error_messages={'required': _('You must select the type of operation')}
    )

    causal = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
        help_text = _('Reason of the movement'), 
        error_messages={'required': _(u'You must declare the causal of this transaction')}
    )

    date = forms.DateField(initial=date.today, required=True
        , help_text=_("Adjust the operation date if necesary")
        , widget=DateFormatAwareWidget
    )

    def __init__(self, request, *args, **kw):
        log.debug("TransationGASForm")
        super(TransationGASForm, self).__init__(request, *args, **kw)
        self.__loggedusr = request.user
        self.__gas = request.resource.gas
        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'
        self.fields['causal'].widget.attrs['class'] = 'input_long'

    def clean(self):

        cleaned_data = super(TransationGASForm, self).clean()
        log.debug("TransationGASForm cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['economic_amount'] = abs(cleaned_data['amount'])
            cleaned_data['economic_target'] = cleaned_data['target']
            cleaned_data['economic_causal'] = cleaned_data['causal']
            if cleaned_data['economic_causal'] == '':
                log.debug("TransationGASForm: required causal")
                raise ValidationError(_("TransationGASForm: transaction require a causal explanation"))
            cleaned_data['economic_date'] = cleaned_data['date']
        except KeyError, e:
            log.debug("TransationGASForm: cannot retrieve economic data: " + e.message)
            raise

        return cleaned_data

#FIXME: The save routine is not called. Reengineering of the balance_gas.py needed
    @transaction.commit_on_success
    def save(self):

        log.debug("SAVESAVESAVESAVESAVE  TransationGASForm")
        #self.instance.gas = self._gas
        #DT: not needeed all derived class are read only
        super(TransationGASForm, self).save()
        #Do economic work
        if not self.__gas:
            return

        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, 
            obj=ObjectWithContext(self.__gas)
        ):
            log.debug("TransationGASForm: PermissionDenied %s in economic operation form" % self.__loggedusr)
            raise PermissionDenied("TransationGASForm: You are not a cash_referrer, you cannot do economic operation!")
        #Do economic work
        try:
            self.__gas.accounting.extra_operation(
                    cleaned_data['economic_amount'],
                    cleaned_data['economic_target'],
                    cleaned_data['economic_causal'],
                    cleaned_data['economic_date'],
            )
        except ValueError, e:
            log.debug("retry later " +  e.message)

#    class Meta:
##        model = GAS
##        fields = ('...')
#        gf_fieldsets = [(None, { 
#            'fields' : ( '',
#                'amount',
#                'target',
#                'note',
#        )})]


#-------------------------------------------------------------------------------

#LF    target = forms.ChoiceField(choices = [('0',_('only GAS')), ('1',_('GAS <--> GASMember')), ('2',_('GAS <--> Supplier'))], widget=forms.RadioSelect, 

#LF        self.fields['target'].initial = '0'

#-------------------------------------------------------------------------------

#LF    pact = forms.ModelChoiceField(label=_('pact'), queryset=GASSupplierSolidalPact.objects.none(), required=False, error_messages={'required': _(u'You must select one pact (or create it in your GAS details if empty)')})

#LF        # SOLIDAL PACT
#LF        pacts = request.resource.pacts
#LF        if pacts and pacts.count() > 0:
#LF            self.fields['pact'].queryset = pacts
#LF#            self.fields['pact'].initial = pacts[0]

#        try:
#            GASSupplierSolidalPact.objects.get(gas=self._gas, supplier=cleaned_data['supplier'])
#        except GASSupplierSolidalPact.DoesNotExist:
#            #ok
#            pass
#        else:
#            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

#-------------------------------------------------------------------------------

#LF    person = forms.ModelChoiceField(queryset=Person.objects.none(), required=False, label=_("Person"))

#LF        # MEMBERS
#LF        gms = request.resource.gasmembers
#LF        if gms and gms.count() > 0:
#LF            self.fields['person'].queryset = gms
#LF


#    class Meta:
##        model = GAS
##        fields = ('...')
#        gf_fieldsets = [(None, { 
#            'fields' : ( '',
#                'amount',
#                'target',
#                'note',
#        )})]


#-------------------------------------------------------------------------------

#LF    target = forms.ChoiceField(choices = [('0',_('only GAS')), ('1',_('GAS <--> GASMember')), ('2',_('GAS <--> Supplier'))], widget=forms.RadioSelect, 

#LF        self.fields['target'].initial = '0'
#LF        self.__gas = request.resource.gas

#-------------------------------------------------------------------------------

#LF    pact = forms.ModelChoiceField(label=_('pact'), queryset=GASSupplierSolidalPact.objects.none(), required=False, error_messages={'required': _(u'You must select one pact (or create it in your GAS details if empty)')})

#LF        # SOLIDAL PACT
#LF        pacts = request.resource.pacts
#LF        if pacts and pacts.count() > 0:
#LF            self.fields['pact'].queryset = pacts
#LF#            self.fields['pact'].initial = pacts[0]

#        try:
#            GASSupplierSolidalPact.objects.get(gas=self._gas, supplier=cleaned_data['supplier'])
#        except GASSupplierSolidalPact.DoesNotExist:
#            #ok
#            pass
#        else:
#            raise ValidationError(_("Pact between this GAS and this Supplier already exists"))

#-------------------------------------------------------------------------------

#LF    person = forms.ModelChoiceField(queryset=Person.objects.none(), required=False, label=_("Person"))

#LF        # MEMBERS
#LF        gms = request.resource.gasmembers
#LF        if gms and gms.count() > 0:
#LF            self.fields['person'].queryset = gms
#LF


