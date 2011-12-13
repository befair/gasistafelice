from django.utils.translation import ugettext as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry
from simple_accounting.utils import register_transaction, register_simple_transaction, transaction_details

#from gasistafelice.base.models import GAS, GASMember

class PersonAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``Person``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``Person``' model.    
    """
    
    def pay_membership_fee(self, gas, year):
        """
        Pay the annual membership fee for a GAS this person is member of.
        
        Fee amount is determined by the ``gas.membership_fee`` attribute.
        
        If this person is not a member of GAS ``gas``, 
        a ``MalformedTransaction`` exception is raised.
        """
        person = self.subject.instance
        if not person.is_member(gas):
            raise MalformedTransaction("A person can't pay membership fees to a GAS that (s)he is not member of")
        source_account = self.system['/wallet']
        exit_point = self.system['/expenses/gas/' + gas.uid + '/fees']
        #FIXME: 'GAS' object has no attribute 'system
        #SOLVED: Do not pass gas but gas.accounting(.system)
        entry_point =  gas.accounting.system['/incomes/fees']
        target_account = gas.accounting.system['/cash']
        amount = gas.membership_fee
        description = _("Year %(year)s --> %(person)s") % {'person': person.report_name, 'year': year,}
        issuer = self.subject 
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='MEMBERSHIP_FEE')
        transaction.add_references([person, gas])

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

    def do_recharge(self, gas, amount, note=""):
        """
        Do a recharge of amount ``amount`` to the corresponding member account
        in the GAS ``gas``.
        
        If this person is not a member of GAS ``gas``, or if ``amount`` is a negative number
        a ``MalformedTransaction`` exception is raised.
        """
        person = self.subject.instance
        if amount < 0:
            raise MalformedTransaction("Amount of a recharge must be non-negative")
        elif not person.is_member(gas):
            raise MalformedTransaction("A person can't make an account recharge for a GAS that (s)he is not member of")
        else:
            source_account = self.system['/wallet']
            exit_point = self.system['/expenses/gas/' + gas.uid + '/recharges']
            entry_point =  gas.accounting.system['/incomes/recharges']
            target_account = gas.accounting.system['/members/' + person.uid]
            description = unicode(person.report_name)
            issuer = self.subject
            transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='RECHARGE')
            transaction.add_references([person, gas])

#Transaction
#    date = models.DateTimeField(default=datetime.now)
#    description = models.CharField(max_length=512, help_text=_("Reason of the transaction"))
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


    def entries(self, base_path='/'):
        """
        List all LedgerEntries (account, transaction, amount)

        Show transactions for gasmembers link to GAS kind='GAS_WITHDRAWAL' + another kind?
        """
        member_account = gasmember.person.uid
        gas_account = gasmember.gas.uid
        accounts = self.system.accounts.filter(name="wallet") | \
            self.system.accounts.filter(parent__name="members", name__in=member_account) | \
            self.system.accounts.filter(parent__name="expenses/gas/" + gas_account + "/fees", name__in=member_account) | \
            self.system.accounts.filter(parent__name="expenses/gas/" + gas_account + "/recharges", name__in=member_account)

        return LedgerEntry.objects.filter(account__in=accounts).order_by('-id', '-transaction__date')

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


