from django.utils.translation import ugettext, ugettext_lazy as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry, account_type
from simple_accounting.utils import register_transaction

from gasistafelice.consts import (
    INCOME, EXPENSE, ASSET, LIABILITY, EQUITY,
    GASMEMBER_GAS, RECYCLE, ADJUST
)
from datetime import datetime

class PersonAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``Person``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``Person``' model.    
    """
    
    def last_entry(self, base_path):
        """last entry for one subject"""

        try:
            latest = self.system[base_path].ledger_entries.latest('transaction__date')
        except LedgerEntry.DoesNotExist:
            latest = None
        return latest

        #FIXME: create last_entry or one method for each base_path? Encapsulation and refactoring
        #FIXME: self <gasistafelice.base.accounting.PersonAccountingProxy object at 0xabaf86c>
        #       base_path '/expenses/gas/gas-1/recharges'

    def do_recharge(self, gas, amount, note="", date=None):
        """
        Do a recharge of amount ``amount`` to the corresponding member account
        in the GAS ``gas``.
        
        If this person is not a member of GAS ``gas``, or if ``amount`` is a negative number
        a ``MalformedTransaction`` exception is raised.
        """
        person = self.subject.instance
        if amount < 0:
            raise MalformedTransaction(ugettext("Amount of a recharge must be non-negative"))
        elif not person.is_member(gas):
            raise MalformedTransaction(ugettext("A person can't make an account recharge for a GAS that (s)he is not member of"))
        else:
            source_account = self.system['/wallet']
            exit_point = self.system['/expenses/gas/' + gas.uid + '/recharges']
            entry_point =  gas.accounting.system['/incomes/recharges']
            target_account = gas.accounting.system['/members/' + person.uid]
            description = unicode(person.report_name)
            issuer = self.subject
            if not date:
                date = datetime.now()  #_date.today
            transaction = register_transaction(source_account, exit_point, 
                entry_point, target_account, amount, description, issuer, 
                date, 'RECHARGE'
            )
            transaction.add_references([person, gas])

#Transaction
#    date = models.DateTimeField(default=datetime.now)
#    description = models.CharField(max_length=512, help_text=ugettext("Reason of the transaction"))
#    issuer = models.ForeignKey(Subject, related_name='issued_transactions_set')
#    source = models.ForeignKey(CashFlow)
#    split_set = models.ManyToManyField(Split)
#    kind = models.CharField(max_length=128, choices=settings.TRANSACTION_TYPES)
#    is_confirmed = models.BooleanField(default=False)
#    def splits(self):
#    def is_split(self):
#    def is_internal(self):
#    def is_simple(self):

#LedgerEntry
#    account = models.ForeignKey(Account, related_name='entry_set')
#    transaction = models.ForeignKey(Transaction, related_name='entry_set')
#    entry_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
#    amount = CurrencyField()
#    def date(self):
#    def description(self):
#    def issuer(self):


    def entries_gasmember(self, gasmember):
        """
        List all LedgerEntries (account, transaction, amount)

        Show transactions for gasmembers link to GAS kind='GAS_WITHDRAWAL' + another kind?
        """

        member_account = gasmember.person.uid
        gas_account = gasmember.gas.uid
        #accounts = self.system.accounts.filter(name="wallet") | \
        accounts = \
            self.system.accounts.filter(parent__name="members", name__in=member_account) | \
            self.system.accounts.filter(parent__name="expenses/gas/" + gas_account + "/fees", name__in=member_account) | \
            self.system.accounts.filter(parent__name="expenses/gas/" + gas_account + "/recharges", name__in=member_account) | \
            gasmember.gas.accounting.system.accounts.filter(parent__name="members", name=member_account)

#gasmember.gas.accounting.system.accounts.filter(name="members/%s" % member_account) ko?

        return LedgerEntry.objects.filter(account__in=accounts).order_by('-id', '-transaction__date')

    def extra_operation(self, gas, amount, target, causal, date):
        """
        Another account operation for this subject

        For a GASMEMBER the target operation can be income or expense operation
        The operation can implicate a GAS economic change
        """

        if amount < 0:
            raise MalformedTransaction(ugettext("Payment amounts must be non-negative"))

        person = self.subject.instance
        if not person.is_member(gas):
            raise MalformedTransaction(ugettext("A person can't pay membership fees to a GAS that (s)he is not member of"))

        gas_acc = gas.accounting
        gas_system = gas.accounting.system
        kind = GASMEMBER_GAS

        #UGLY: remove me when done and executed one command that regenerate all missing accounts
        self.missing_accounts(gas)

        if target == INCOME: #Correction for gasmember: +gasmember -GAS
            source_account = gas_system['/cash']
            exit_point = gas_system['/expenses/member']
            entry_point = gas_system['/incomes/recharges']
            target_account = gas_system['/members/' + person.uid]
        elif  target == EXPENSE: #Correction for GAS: +GAS -gasmember
            source_account = gas_system['/members/' + person.uid]
            exit_point = gas_system['/expenses/gas']
            entry_point = gas_system['/incomes/member']
            target_account = gas_system['/cash']
        elif  target == ASSET: #Detraction for Gasmember: -gasmember
            source_account = gas_system['/members/' + person.uid]
            exit_point = gas_system['/expenses/member']
            entry_point = self.system['/incomes/other']
            target_account = self.system['/wallet']
            kind = ADJUST
        elif  target == LIABILITY: #Addition for Gasmember: +gasmember
            source_account = self.system['/wallet']
            exit_point = self.system['/expenses/other']
            entry_point = gas_system['/incomes/recharges']
            target_account = gas_system['/members/' + person.uid]
            kind = ADJUST
        elif  target == EQUITY: #Restitution for gasmember: empty container +gasmember -GAS
            source_account = gas_system['/cash']
            exit_point = gas_system['/expenses/member']
            entry_point = gas_system['/incomes/recharges']
            target_account = gas_system['/members/' + person.uid]
            kind = RECYCLE
        else:
            raise MalformedTransaction(ugettext("Payment target %s not identified") % target)

        description = "%(gas)s %(target)s %(causal)s" % {
            'gas': gas.id_in_des,
            'target': target,
            'causal': causal
        }
        issuer = self.subject
        if not date:
            date = datetime.now()  #_date.today
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, date, kind)

#		. gasmember ROOT (/)
#		|----------- wallet [A]
#		+----------- incomes [P,I]	+
#		|				+--- TODO: Other (Private order, correction, Deposit)
#		+----------- expenses [P,E]	+  UNUSED because we use the gas_system[/incomes/recharges]
#						+--- TODO: Other (Correction, Donation, )

#        . GAS ROOT (/)
#        |----------- cash [A]
#        +----------- members [P,A]+
#        |                +--- <UID member #1>  [A]
#        |                | ..
#        |                +--- <UID member #n>  [A]
#        +----------- expenses [P,E]+
#        |                +--- TODO: member (correction or other)
#        |                +--- TODO: gas (correction or other)
#        +----------- incomes [P,I]+
#        |                +--- recharges [I]
#        |                +--- TODO: member (correction or other)

    #UGLY: remove me when done and executed one command that regenerate all missing accounts
    def missing_accounts(self, gas):
        gas_acc = gas.accounting
        gas_system = gas.accounting.system
        xsys = gas_acc.get_account(gas_system, '/expenses', 'member', account_type.expense)
        xsys = gas_acc.get_account(gas_system, '/expenses', 'gas', account_type.expense)
        xsys = gas_acc.get_account(gas_system, '/incomes', 'member', account_type.income)
        xsys = gas_acc.get_account(self.system, '/expenses', 'other', account_type.expense)
        xsys = gas_acc.get_account(self.system, '/incomes', 'other', account_type.income)

