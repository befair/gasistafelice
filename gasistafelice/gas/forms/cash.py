# -*- coding: utf-8 -*-

import os, sys

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
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
        INCOME, EXPENSE, INVOICE_COLLECTION, ASSET, LIABILITY, EQUITY,  #Transactions
        FAKE_WITHDRAWN_AMOUNT
)

import datetime
from gasistafelice.utils import short_date

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
    applied = forms.BooleanField(required=False)

    #TODO: domthu: note and delete
    #note = forms.CharField(required=False, widget=forms.TextInput(), max_length=64)

    def __init__(self, request, *args, **kw):
        super(EcoGASMemberForm, self).__init__(*args, **kw)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__order = request.resource.order

    def clean(self):

        cleaned_data = super(EcoGASMemberForm, self).clean()
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError as e:
            log.error("EcoGASMemberForm: cannot retrieve gasmember: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve gasmember: ") + e.message)
        except GASMember.DoesNotExist:
            log.error("EcoGASMemberForm: cannot retrieve gasmember with id " + str(cleaned_data['gm_id']))
            raise forms.ValidationError(ugettext("Cannot retrieve gasmember with id ") + str(cleaned_data['gm_id']))

        amounted = cleaned_data.get('amounted')
        enabled = cleaned_data.get('applied')

        if enabled:
            log.debug("Curtail applied. Amounted = %s" % amounted)
            if amounted is None:
                raise forms.ValidationError(ugettext("You have to write a number (even 0) for a curtail that you want to apply"))

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Control logged user KO if superuser
        #DT: refs = gas.cash_referrers
        #DT: if refs and request.user in refs:
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__order.gas)) and \
            not self.__loggedusr == self.__order.referrer_person.user:
            raise PermissionDenied(ugettext("You are not a cash_referrer or the order's referrer, you cannot update GASMembers cash!"))

        if not self.__order.is_unpaid() and not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed (%s)" % (
                self.__loggedusr, self.__order.current_state.name)
            )
            raise PermissionDenied(ugettext("order is not in the right state!"))

        gm = self.cleaned_data['gasmember']

        #Do economic work
        amounted = self.cleaned_data.get('amounted')
        enabled = self.cleaned_data.get('applied')

        if enabled and amounted is not None:
            log.debug("Save EcoGASMemberForm enabled for %s (amount=%s)" % (gm, amounted))
            # This kind of amount is ever POSITIVE!
            amounted = abs(amounted)

            refs = [gm, self.__order]

            original_amounted = self.cleaned_data['original_amounted']

            # If this is an update -> the amount of the NEW transaction 
            # is the difference between this and the previous one
            comment=u""
            if original_amounted is not None:
                comment = _("[MOD] old_amount=%(old)s -> new_amount=%(new)s") % {
                    'old' : original_amounted, 'new' : amounted
                }
                amounted -= original_amounted
                #KO 14-04-01: # A ledger entry already exists
                #KO 14-04-01: if original_amounted != amounted:
                #KO 14-04-01:     gm.gas.accounting.withdraw_from_member_account_update(
                #KO 14-04-01:         gm, amounted, refs
                #KO 14-04-01:     )

            #KO 14-04-01: else:
            gm.gas.accounting.withdraw_from_member_account(
                gm, amounted, refs, self.__order, comment=comment
            )

#            # Only for test Control if yet exist some transaction for this refs.
#            computed_amount, existing_txs = gm.gas.accounting.get_amount_by_gas_member(gm, self.__order)
#            log.debug("BEFORE %(original_amounted)s %(computed_amount)s %(existing_txs)s" % {
#                    'computed_amount': computed_amount, 
#                    'existing_txs': existing_txs,
#                    'original_amounted': original_amounted
#            })

            #Update State if possible
            self.__order.control_economic_state()

#--------------------------------------------------------------------------------

class NewEcoGASMemberForm(forms.Form):
    """Return an empty form class for row level operation on cash ordered data
    use in Curtail -> ADD FAMILY
    Movement between GASMember.account --> GAS.account
    """

    gasmember = forms.ModelChoiceField(
        queryset=GASMember.objects.none(), 
        required=False
    )
    amounted = CurrencyField(required=False, initial=0, max_digits=8, decimal_places=2)
    applied = forms.BooleanField(required=False, initial=False)

    def __init__(self, request, *args, **kw):
        super(NewEcoGASMemberForm, self).__init__(*args, **kw)
        gm_qs = request.resource.gasmembers
        purchs_ids = map(lambda gm: gm.pk, request.resource.purchasers)
        self.fields['gasmember'].queryset = gm_qs.exclude(pk__in=purchs_ids)
        self.fields['amounted'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__order = request.resource.order

    def create_fake_purchaser(self, purchaser, price, note):

        return GASMemberOrder.objects.create(
            ordered_product = self.__order.orderable_products[0],
            ordered_amount = 1,
            withdrawn_amount = FAKE_WITHDRAWN_AMOUNT,
            is_confirmed = True,
            note = "[NEW FAM] %s" % note,
            #LF: ordered_price should be 0, otherwise expected amount will vary
            ordered_price = 0,
            purchaser = purchaser
        )

    def clean(self):

        cleaned_data = super(NewEcoGASMemberForm, self).clean()
        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Control logged user KO if superuser
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__order.gas)) and \
            not self.__loggedusr == self.__order.referrer_person.user:
            raise PermissionDenied(ugettext("You are not a cash_referrer or the order's referrer, you cannot update GASMembers cash!"))

        if not self.__order.is_unpaid() and not self.__order.is_closed():
            log.debug("PermissionDenied %s Order not in state closed (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied(ugettext("order is not in good state!"))

        #Do economic work
        gm = self.cleaned_data['gasmember']
        amounted = self.cleaned_data.get('amounted') or 0
        enabled = self.cleaned_data.get('applied')

        if amounted > 0 and enabled:

            log.debug("Save NewEcoGASMemberForm enabled(%s) for %s" % (enabled, gm))
            amounted = abs(amounted)
            self.create_fake_purchaser(gm, amounted, 
                note=ugettext("added by: %s") % self.__loggedusr
            )
            refs = [gm, self.__order]
            gm.gas.accounting.withdraw_from_member_account(gm, amounted, refs, self.__order)


#--------------------------------------------------------------------------------

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
        super(EcoGASMemberRechargeForm, self).__init__(*args, **kw)
        self.fields['recharged'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__gas = request.resource.gas

    def clean(self):

        cleaned_data = super(EcoGASMemberRechargeForm, self).clean()
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug(u"EcoGASMemberRechargeForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug(u"EcoGASMemberRechargeForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
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

            raise PermissionDenied(ugettext("You are not a cash_referrer, you cannot update GASMembers cash!"))

        gm = self.cleaned_data['gasmember']
        if not gm in self.__gas.gasmembers:
            log.debug(u"PermissionDenied %s in cash recharge for gasmember %s not in this gas %s" % self.__loggedusr, gm, self.__gas)
            raise PermissionDenied(ugettext("You are not a cash referrer for the GAS, you cannot recharge GASMembers cash!"))

        # This kind of amount is ever POSITIVE!
        gm.person.accounting.do_recharge(self.__gas, recharged)

EcoGASMemberRechargeFormSet = formset_factory(
    form=EcoGASMemberRechargeForm,
    formset=BaseFormSetWithRequest,
    extra=0 #must be 0 no add form
)

def get_year_choices():
    #DOMTHU: return [ ('2001', '2001'), ('2002', '2002'), ('2003', '2003')]
    dt = datetime.datetime.now()
    year = datetime.timedelta(days=365)
    last_year = (dt-year).strftime('%Y')
    actual_year = dt.strftime('%Y')
    next_year = (dt+year).strftime('%Y')
    return [ ('0', '----'), (last_year, last_year), (actual_year, actual_year), (next_year, next_year)]

def add_time(_date):
    if _date == datetime.date.today():
        now = datetime.datetime.now()
        t = now.time()
    else:
        t = datetime.datetime.min.time()   #time(0,0)
    return datetime.datetime.combine(_date, t)

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
        super(EcoGASMemberFeeForm, self).__init__(*args, **kw)
        self.fields['feeed'].widget.attrs['class'] = 'taright'
        self.__loggedusr = request.user
        self.__gas = request.resource.gas

    def clean(self):

        cleaned_data = super(EcoGASMemberFeeForm, self).clean()
        try:
            cleaned_data['gasmember'] = GASMember.objects.get(pk=cleaned_data['gm_id'])
        except KeyError:
            log.debug(u"EcoGASMemberFeeForm: cannot retrieve GASMember identifier. FORM ATTACK!")
            raise 
        except GASMember.DoesNotExist:
            log.debug(u"EcoGASMemberFeeForm: cannot retrieve GASMember instance. Identifier (%s)." % cleaned_data['gm_id'])
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
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__gas)):
            raise PermissionDenied(ugettext("You are not a cash_referrer, you cannot update GASMembers cash!"))

        gm = self.cleaned_data['gasmember']
        if not gm in self.__gas.gasmembers:
            raise PermissionDenied(ugettext("You are not a cash_referrer for the GAS, you cannot register fee GASMembers cash!"))

        gm.gas.accounting.pay_membership_fee(gm, year)

EcoGASMemberFeeFormSet = formset_factory(
    form=EcoGASMemberFeeForm,
    formset=BaseFormSetWithRequest,
    extra=0 #must be 0 no add form
)




#-------------------------------------------------------------------------------

EURO_HTML = '&#8364;'  # &amp;euro; &#8364; &euro;  &#128;  &#x80;
EURO_LABEL = 'Eur.'  # € &amp;euro; &#8364; &euro;  &#128;  &#x80;

class InvoiceOrderForm(forms.Form):

    amount = CurrencyField(label=_('Actual total'), required=True, max_digits=8, decimal_places=2,
        error_messages={'required': _('You must insert an postive amount')}
    )
    note = forms.CharField(label=_('Note'), required=False, widget=forms.Textarea)

    def __init__(self, request, *args, **kw):

        super(InvoiceOrderForm, self).__init__(*args, **kw)

        self.__order = request.resource.order
        if self.__order:
            # display statistic
            stat = ugettext(u"%(state)s - %(totals)s") % {
                'state': self.__order.current_state.name
                , 'totals': self.__order.display_totals.replace("euro",EURO_HTML)
            }
            self.fields['amount'].help_text = stat


            #set invoice data
            if self.__order.invoice_amount:
                self.fields['amount'].initial = "%.2f" % round(self.__order.invoice_amount, 2)
            if self.__order.invoice_note:
                self.fields['note'].initial = self.__order.invoice_note
        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'

        if not self.__order.is_unpaid() and not self.__order.is_closed():
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
            log.error("InvoiceOrderForm: cannot retrieve invoice data: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve invoice data: ") + e.message)

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        if not self.__order:
            return

        #Control logged user KO if superuser
        #DT: refs = gas.cash_referrers
        #DT: if refs and request.user in refs:
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__order.gas)) and \
            not self.__loggedusr == self.__order.referrer_person.user:
            raise PermissionDenied(ugettext("You are not a cash_referrer or the order's referrer, you cannot update GASMembers cash!"))

        if not self.__order.is_unpaid() and not self.__order.is_closed():
            log.debug(u"PermissionDenied %s Order not in state closed (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied(ugettext("order is not in good state!"))

        self.__order.invoice_amount = self.cleaned_data['invoice_amount']
        self.__order.invoice_note = self.cleaned_data['invoice_note']

        self.__order.save()
        #Update State if possible
        self.__order.control_economic_state()

#-------------------------------------------------------------------------------

def get_html_insolutes(insolutes, EURO_TRANS=EURO_HTML):

    _choices = []
    tot_ordered = 0
    tot_invoiced = 0
    tot_eco_entries = 0
    tot_insolutes = 0
    stat = ''
    for ins in insolutes:
        tot_insolutes += 1
        tot_ordered += ins.tot_price
        tot_invoiced += ins.invoice_amount or 0
        tot_eco_entries += ins.tot_curtail

        choice = ugettext(u"<span>%(html_order)s<br />%(totals)s</span>") % {
            'state': ins.current_state.name
            , 'totals' : ins.display_totals.replace("euro",EURO_TRANS)
            , 'html_order': u'<a class="resource order inline" href="%s">%s</a>' % (ins.get_absolute_url_page(), ins)
        }
        _choices.append((ins.pk, mark_safe(choice)))

    #set order informations
    stat = ugettext(u"Totals (%(n)s insolutes) --> Expected: %(fam)s %(euro)s --> Actual: %(fatt)s %(euro)s --> Curtailed: %(eco)s %(euro)s") % {
        'fam'    : "%.2f" % round(tot_ordered, 2)
        , 'fatt' : "%.2f" % round(tot_invoiced, 2)
        , 'eco'  : "%.2f" % round(tot_eco_entries, 2)
        , 'euro' : EURO_TRANS
        , 'n'    : tot_insolutes
    }

    return _choices, mark_safe(stat)

class InsoluteOrderForm(forms.Form):

    orders = forms.MultipleChoiceField(label=_("Insolute order(s)"), required=True
        , help_text = _("Select one or multiple orders to pay in this operation.")
        , widget=forms.CheckboxSelectMultiple
    )

    amount = CurrencyField(label=_('Payment'), required=True, max_digits=8, decimal_places=2)

    causal = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
        help_text = _('Some indication about the payment: by bank or cash, bank number transaction...'), 
        error_messages={'required': _('You must declare the causal of this payment')}
    )

    date = forms.DateField(initial=datetime.date.today, required=True
        , label = _("Date")
        , help_text = _("Adjust the operation date if needed")
        , widget=DateFormatAwareWidget
    )


    def __init__(self, request, *args, **kw):

        super(InsoluteOrderForm, self).__init__(*args, **kw)

        #TODO: refactor for SOLIDAL PACT --> do not use order as ressource but insolutes
        self.__order = request.resource.order
        self.__gas = request.resource.gas

        if self.__order:

            #set insolute data and informations
            yet_payed, descr, date_payed =self.__gas.accounting.get_supplier_order_data(self.__order)
            if yet_payed > 0:
                self.fields['amount'].initial = "%.2f" % round(yet_payed, 2)
                self.fields['causal'].initial = descr
                self.fields['causal'].widget.attrs['readonly'] = True
                self.fields['causal'].widget.attrs['disabled'] = 'disabled'
                self.fields['causal'].help_text = ''
                self.fields['causal'].required = False
                self.fields['date'].initial = date_payed
                self.fields['date'].help_text = ''
                del self.fields['orders']
                #set order informations
                stat = ugettext(u"%(state)s - %(totals)s") % {
                    'state': self.__order.current_state.name
                    , 'totals': self.__order.display_totals.replace("euro",EURO_HTML)
                }

            else:
                insolutes = self.__order.insolutes
                _choice, stat = get_html_insolutes(insolutes)
                self.fields['orders'].choices = _choice

            self.fields['amount'].help_text = stat

        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'
        if not self.__order.is_unpaid() and not self.__order.is_closed():
            self.fields['amount'].widget.attrs['readonly'] = True
            self.fields['amount'].widget.attrs['disabled'] = 'disabled'
        self.fields['causal'].widget.attrs['class'] = 'input_long'

        self.__loggedusr = request.user
        self.__gas = self.__order.gas

    def clean(self):

        cleaned_data = super(InsoluteOrderForm, self).clean()
        try:
            cleaned_data['insolute_amount'] = abs(cleaned_data['amount'])
        except KeyError, e:
            log.error("InsoluteOrderForm: cannot retrieve economic data: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve economic data: ") + e.message)

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        if not self.__order:
            return

        #Control logged user
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__gas)):
            raise PermissionDenied(ugettext("You are not a cash_referrer, you cannot manage insolute order cash!"))

        if not self.__order.is_unpaid() and not self.__order.is_closed():
            log.debug(u"PermissionDenied %s Order not in state closed or unpaid (%s)" % (self.__loggedusr, self.__order.current_state.name))
            raise PermissionDenied(ugettext("order is not in good state!"))

        #cc_orders = cleaned_data.get("orders")
        yet_payed, descr, date_payed =self.__gas.accounting.get_supplier_order_data(self.__order)
        if yet_payed > 0: # and not cc_orders:
            pay_insolutes(
                    self.__order.gas,
                    self.__order.pact,
                    self.cleaned_data['insolute_amount'],
                    [self.__order.pk],
                    self.cleaned_data['causal'],
                    self.cleaned_data['date'],
            )
        else:
            pay_insolutes(
                    self.__order.gas,
                    self.__order.pact,
                    self.cleaned_data['insolute_amount'],
                    self.cleaned_data['orders'],
                    self.cleaned_data['causal'],
                    self.cleaned_data['date'],
            )

#-------------------------------------------------------------------------------

def get_eco_class(eco_state):
    eco_class = "negative"
    _sold = float(eco_state)
    if _sold >= 10:
        eco_class = "positive"
    elif -10 < _sold and _sold < 10:
        eco_class = "stalled"
    return "balance " + eco_class

#-------------------------------------------------------------------------------

class BalanceForm(forms.Form):

    balance = CurrencyField(label=_('Balance'), required=False, max_digits=8, decimal_places=2)

    def __init__(self, request, *args, **kw):

        super(BalanceForm, self).__init__(*args, **kw)
        #self.__gas_list = request.resource.gas_list

        eco_state = request.resource.balance
        eco_class = get_eco_class(eco_state)
        self.fields['balance'].initial = ("%.2f" % round(request.resource.balance, 2)).replace('.','€')
        self.fields['balance'].widget.attrs['class'] = eco_class
        self.__loggedusr = request.user

        # LF: Balance is a readonly field
        field_name = 'balance'
        self.fields[field_name].widget.attrs['readonly'] = True
        self.fields[field_name].widget.attrs['disabled'] = 'disabled'

#LF: balance and wallet_*  are always read-only so they SHOULD NOT be included in form...
class BalanceGASForm(BalanceForm):

    wallet_gasmembers = CurrencyField(label=_('Wallet GASMembers'), required=False, max_digits=8, decimal_places=2)
    wallet_suppliers = CurrencyField(label=_('Solidal cash flow'), required=False, max_digits=8, decimal_places=2)

#    orders_grd = forms.MultipleChoiceField(
#        label=_('Insolutes'), choices=GASSupplierOrder.objects.none(), 
#        required=False, 
#        widget=forms.CheckboxSelectMultiple
#    )
#
#    wallet_insolute = CurrencyField(label=_('Wallet Insolute'), required=False, max_digits=8, decimal_places=2)

    def __init__(self, request, *args, **kw):

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

        #show insolutes
        _choice, stat = get_html_insolutes(request.resource.gas.insolutes, EURO_LABEL)
        #WAS LF: self.fields['orders_grd'].choices = _choice
        #WAS LF: self.fields['wallet_insolute'].initial = stat.replace('(euro)s',EURO_HTML)


#-------------------------------------------------------------------------------

#LF: other stuff now may be commented because we have to think
# about more intuitive way to do these operations
#UGLY: fixme when succeed to open popup for cash referrer operations
#class TransationGASForm(forms.Form):
class TransationGASForm(BalanceGASForm):

    amount = CurrencyField(label=_('cash amount').capitalize(), required=True, max_digits=8, decimal_places=2,
        help_text = _('Insert the amount of money (no sign)'),
        error_messages = {'required': _('You must insert an postive or negative amount for the operation')}
    )

    target = forms.ChoiceField(required=True, 
        choices = [
            (INCOME,_('Income: Event, Donate, Sponsor, Fund... +GAS')),
            (EXPENSE,_('Expense: Expenditure, Invoice, Bank, Administration, Event, Rent... -GAS'))
        ],
        widget=forms.RadioSelect,
        #help_text = _("select the kind for this operation"),
        label=_("operation kind").capitalize(),
        error_messages={'required': _('You must select the type of operation')}
    )

    causal = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
        help_text = _('Reason of the movement'),
        error_messages={'required': _('You must declare the causal of this transaction')}
    )

    date = forms.DateField(initial=datetime.date.today, required=True
        , label = _("Date")
        , help_text = _("Adjust the operation date if needed")
        , widget=DateFormatAwareWidget
    )

    def __init__(self, request, *args, **kw):

        super(TransationGASForm, self).__init__(request, *args, **kw)
        self.__loggedusr = request.user
        self.__gas = request.resource.gas
        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'
        self.fields['causal'].widget.attrs['class'] = 'input_long'

    def clean(self):

        cleaned_data = super(TransationGASForm, self).clean()
        #log.debug(u"TransationGASForm cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['economic_amount'] = abs(cleaned_data['amount'])
            cleaned_data['economic_target'] = cleaned_data['target']
            cleaned_data['economic_causal'] = cleaned_data['causal']
            if cleaned_data['economic_causal'] == '':
                log.error("TransationGASForm: transaction require a causal explanation")
                raise forms.ValidationError(ugettext("Transaction require a causal explanation"))
            cleaned_data['economic_date'] = cleaned_data['date']
        except KeyError, e:
            log.error("TransationGASForm: cannot retrieve economic data: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve economic data: ") + e.message)

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #DT: not needeed all derived class are read only
        #super(TransationGASForm, self).save()

        #Do economic work
        if not self.__gas:
            return

        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__gas)):
            raise PermissionDenied(ugettext("TransationGASForm: You are not a cash_referrer, you cannot do economic operation!"))

        self.__gas.accounting.extra_operation(
                self.cleaned_data['economic_amount'],
                self.cleaned_data['economic_target'],
                self.cleaned_data['economic_causal'],
                add_time(self.cleaned_data['economic_date']),
        )

#-------------------------------------------------------------------------------



class TransationPACTForm(BalanceForm):

#DT     Use this if we have to insert this block in the GAS economic Tab too
#LF    pact = forms.ModelChoiceField(label=_('pact'), queryset=GASSupplierSolidalPact.objects.none(), required=False, error_messages={'required': _('You must select one pact (or create it in your GAS details if empty)')})

    amount = CurrencyField(label=_('cash amount').capitalize(), 
        required=True, max_digits=8, decimal_places=2,
        help_text = _('Insert the amount of money (no sign)'),
        error_messages = {'required': _('You must insert an postive or negative amount for the operation')}
    )

    TARGET_CHOICES = [ 
        (INCOME,_('Correction in favor to supplier: +Supplier -GAS')),
        (EXPENSE,_('Correction in favor to GAS: +GAS -Supplier ')),
        (INVOICE_COLLECTION,_('Orders payment'))
    ]
    target = forms.ChoiceField(required=True,
        choices = TARGET_CHOICES,
        widget=forms.RadioSelect,
        #help_text = _("select the kind for this operation"),
        label=_("operation kind").capitalize(),
        error_messages={'required': _('You must select the type of operation')}
    )

    orders = forms.MultipleChoiceField(label=_("Insolute order(s)"), required=False
        , help_text = _("If chosen operation kind is order payment, you must select at least one order to pay")
        , widget=forms.CheckboxSelectMultiple
    )

    causal = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
        help_text = _('Reason of the movement'),
        error_messages={'required': _('You must declare the causal of this transaction')}
    )

    date = forms.DateField(initial=datetime.date.today, required=True
        , label = _("Date")
        , help_text = _("Adjust the operation date if needed")
        , widget=DateFormatAwareWidget
    )

    def __init__(self, request, *args, **kw):

        super(TransationPACTForm, self).__init__(request, *args, **kw)
        self.__loggedusr = request.user
        self.__gas = request.resource.gas
        self.__pact = request.resource.pact
        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'
        self.fields['causal'].widget.attrs['class'] = 'input_long'

        _choice = self.fields['target'].choices
        #Avoid multiple delete during post (in case of raise some exception)

        insolutes = self.__pact.insolutes
        if not insolutes:
            # Hide Insolute choice
            _choice = self.fields['target'].choices
            if len(_choice) > 2: #FIXME (related to ##) BAD CHECK NO NEED if we do choices modification for form instance
                del _choice[-1]
                #FIXME (id:##) AAAA WARNING WE ARE CHANGING a CLASS ATTRIBUTE (field!)
                #CHECK if it is possible to do choices update in form instance
                #rather than in form class. Now we fix with a corresponding bad code
                #in the "else" branch.
                self.fields['target'].choices = _choice
                #Hide order form field
                del self.fields['orders']

        else:
            #FIXME (related to ##) bad code to FIX weird behaviour described before
            self.fields['target'].choices = TransationPACTForm.TARGET_CHOICES

            choices, stat = get_html_insolutes(insolutes)
            self.fields['orders'].choices = choices
            self.fields['amount'].help_text = stat
#            _choice = []
#            tot_orders = 0
#            tot_ordered = 0
#            tot_invoiced = 0
#            tot_eco_entries = 0
#            stat = ''
#            for ins in insolutes:
#                #WAS: #In the SUPPLIER FORM we only pay unpayed orders.
#                #WAS: #to modify one payed order: go to it's sheet.
#                #WAS: yet_payed, descr, date_payed =self.__gas.accounting.get_supplier_order_data(ins)
#                #WAS: yet_payed == 0:
#                #LF: insolutes are unpaid, so I can't see why it is needed this further check
#                    tot_orders += 1
#                    tot_ordered += ins.tot_price
#                    tot_invoiced += ins.invoice_amount or 0
#                    tot_eco_entries += ins.tot_curtail
#                    stat = "Ord.%(order)s %(state)s -Fam: %(fam)s (euro)s --> Fatt: %(fatt)s (euro)s --> Pag: %(eco)s (euro)s" % {
#                        'fam'    : "%.2f" % round(ins.tot_price, 2)
#                        , 'fatt' : "%.2f" % round(ins.invoice_amount or 0, 2)
#                        , 'eco'  : "%.2f" % round(ins.tot_curtail, 2)
#                        , 'state'  : ins.current_state.name
#                        , 'order'  : str(ins.pk) + " - " + short_date(ins.datetime_end)
#                        } 
#                    _choice.append((ins.pk, stat.replace('(euro)s',EURO_LABEL)))
#            self.fields['orders'].choices = _choice
#
#            #set order informations
#            stat = "Orders(%(num)s) - Total --> Fam: %(fam)s (euro)s --> Fatt: %(fatt)s (euro)s --> Pag: %(eco)s (euro)s" % {
#                'fam'    : "%.2f" % round(tot_ordered, 2)
#                , 'fatt' : "%.2f" % round(tot_invoiced, 2)
#                , 'eco'  : "%.2f" % round(tot_eco_entries, 2)
#                , 'num'  : str(tot_orders)
#            }
#            self.fields['amount'].help_text = stat.replace('(euro)s',EURO_HTML)

#LF        # SOLIDAL PACT
#LF        pacts = request.resource.pacts
#LF        if pacts and pacts.count() > 0:
#LF            self.fields['pact'].queryset = pacts
#LF#            self.fields['pact'].initial = pacts[0]

    def clean(self):

        cleaned_data = super(TransationPACTForm, self).clean()
        #log.debug(u"TransationPACTForm cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['economic_amount'] = abs(cleaned_data['amount'])
            cleaned_data['economic_target'] = cleaned_data['target']
            cleaned_data['economic_causal'] = cleaned_data['causal']
            if cleaned_data['economic_causal'] == '':
                log.error("TransationPACTForm: transaction require a causal explanation")
                raise forms.ValidationError(ugettext("Transaction require a causal explanation"))
            if cleaned_data['economic_target'] == INVOICE_COLLECTION:
                cleaned_data['economic_orders'] = cleaned_data['orders']
                if not cleaned_data['economic_orders'] or len(cleaned_data['economic_orders']) <= 0:
                    self._errors["orders"] = self.error_class([ugettext("Insolute transaction require almost one order to be payed")])
            cleaned_data['economic_date'] = cleaned_data['date']
        except KeyError, e:
            log.error("TransationPACTForm: cannot retrieve economic data: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve economic data: ") + e.message)

#        try:
#            GASSupplierSolidalPact.objects.get(gas=self._gas, supplier=cleaned_data['supplier'])
#        except GASSupplierSolidalPact.DoesNotExist:
#            #ok
#            pass
#        else:
#            raise ValidationError(ugettext("Pact between this GAS and this Supplier already exists"))

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #DT: not needeed all derived class are read only
        #super(TransationPACTForm, self).save()

        #Do economic work
        if not self.__pact:
            return

        #if self.__loggedusr not in self.__order.cash_referrers: KO if superuser
        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__gas)):
            raise PermissionDenied(ugettext("You are not a cash_referrer, you cannot do economic operation!"))

        if self.cleaned_data['economic_target'] == INVOICE_COLLECTION:
            #Pay Insolute
            pay_insolutes(
                    self.__gas,
                    self.__pact,
                    self.cleaned_data['economic_amount'],
                    self.cleaned_data['economic_orders'],
                    self.cleaned_data['economic_causal'],
                    add_time(self.cleaned_data['economic_date']),
            )
        else:
            #Do correction
            self.__pact.supplier.accounting.extra_operation(
                    self.__gas,
                    self.__pact,
                    self.cleaned_data['economic_amount'],
                    self.cleaned_data['economic_target'],
                    self.cleaned_data['economic_causal'],
                    add_time(self.cleaned_data['economic_date']),
            )


def pay_insolutes(gas, pact, amount, insolutes, descr, date):
    refs=[]
    if insolutes:
        multiple_ords = ""
        for ins_pk in insolutes:
            try:
                _ins = GASSupplierOrder.objects.get(pk=ins_pk)
            except GASSupplierOrder.DoesNotExist:
                log.debug("pay_insolutes: cannot retrieve order instance. Identifier (%s)." % ins_pk)
            else:
                if _ins and (_ins.is_unpaid() or _ins.is_closed()):
                    refs.append(_ins)
                    if multiple_ords == "":
                        multiple_ords = "[" + str(_ins.pk)
                    else:
                        multiple_ords += ", " + str(_ins.pk)

        if len(refs) > 0:
            if len(refs) == 1:
                multiple_ords = None
            else:
                multiple_ords += "]"

            #log.debug("pay_insolutes: descr (%s)." % descr)
            try:
                #MAKE ONLY ONE TRANSACTION with the amount but the ref must contains all orders reference in order to matche this unique transcation
                log.debug("Entering gas.accounting.pay_supplier_order amount=%s descr=%s" %
(amount, descr))
                gas.accounting.pay_supplier_order(order=refs[0], amount=amount, descr=descr, refs=refs, date=date, multiple=multiple_ords)
                log.debug("Finished gas.accounting.pay_supplier_order")
            except ValueError, e:
                #log.debug("retry later " + e.message)
                raise forms.ValidationError(ugettext("Error while saving insolute economic data: ") + e.message)
            else:
                #log.debug("Insolute(%s) saved " % len(refs))
                for _order in refs:
                    #NOTE: orders can be payed but receipt invoice and curtail families could not be yet done; so update State if possible
                    _order.control_economic_state()
        else:
            raise forms.ValidationError(ugettext("Cannot retrieve economic orders"))

#-------------------------------------------------------------------------------

class TransationGMForm(BalanceForm):

#DT     Use this if we have to insert this block in the GAS economic Tab too
#LF    person = forms.ModelChoiceField(queryset=Person.objects.none(), required=False, label=_("Person"))

    amount = CurrencyField(label=_('cash amount').capitalize(), 
        required=True, max_digits=8, decimal_places=2,
        help_text = _('Insert the amount of money (no sign)'),
        error_messages = {'required': _('You must insert an postive or negative amount for the operation')}
    )

    target = forms.ChoiceField(required=True,
        choices = [ (INCOME,_('Correction in favor to gasmember: +gasmember -GAS')),
                    (EXPENSE,_('Correction in favor to GAS: +GAS -gasmember ')),
                    (ASSET,_('Detraction from Gasmember: -gasmember ')),
                    (LIABILITY,_('Addition to Gasmember: +gasmember ')),
                    (EQUITY,_('Restitution in favor to gasmember: empty container +gasmember -GAS'))
        ],
        widget=forms.RadioSelect,
        #help_text = _("select the kind for this operation"),
        label=_("operation kind").capitalize(),
        error_messages={'required': _('You must select the type of operation')}
    )

    causal = forms.CharField(label=_('Causal'), required=True, widget=forms.TextInput,
        help_text = _('Reason of the movement'),
        error_messages={'required': _('You must declare the causal of this transaction')}
    )

    date = forms.DateField(initial=datetime.date.today, required=True
        , label = _("Date")
        , help_text = _("Adjust the operation date if needed")
        , widget=DateFormatAwareWidget
    )

    def __init__(self, request, *args, **kw):

        super(TransationGMForm, self).__init__(request, *args, **kw)
        self.__loggedusr = request.user
        self.__gas = request.resource.gas
        self.__gm = request.resource.gasmember
        self.fields['amount'].widget.attrs['class'] = 'balance input_payment'
        self.fields['causal'].widget.attrs['class'] = 'input_long'

    def clean(self):

        cleaned_data = super(TransationGMForm, self).clean()
        #log.debug(u"TransationGMForm cleaned_data %s" % cleaned_data)
        try:
            cleaned_data['economic_amount'] = abs(cleaned_data['amount'])
            cleaned_data['economic_target'] = cleaned_data['target']
            cleaned_data['economic_causal'] = cleaned_data['causal']
            if cleaned_data['economic_causal'] == '':
                log.error("TransationGMForm: transaction require a causal explanation")
                raise forms.ValidationError(ugettext("Transaction require a causal explanation"))
            cleaned_data['economic_date'] = cleaned_data['date']
        except KeyError, e:
            log.error("TransationGMForm: cannot retrieve economic data: " + e.message)
            raise forms.ValidationError(ugettext("Cannot retrieve economic data: ") + e.message)

#LF        # MEMBERS
#LF        gms = request.resource.gasmembers
#LF        if gms and gms.count() > 0:
#LF            self.fields['person'].queryset = gms

        return cleaned_data

    @transaction.commit_on_success
    def save(self):

        #Do economic work
        if not self.__gm:
            return

        if not self.__loggedusr.has_perm(CASH, obj=ObjectWithContext(self.__gas)):
            raise PermissionDenied(ugettext("You are not a cash_referrer, you cannot do economic operation!"))

        self.__gm.person.accounting.extra_operation(
                self.__gas,
                self.cleaned_data['economic_amount'],
                self.cleaned_data['economic_target'],
                self.cleaned_data['economic_causal'],
                add_time(self.cleaned_data['economic_date']),
        )

