from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry
from simple_accounting.utils import register_transaction, register_simple_transaction, transaction_details


class PersonAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``Person``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``Person``' model.    
    """
    
    def pay_membership_fee(self, gas, year, refs=None):
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
        entry_point =  gas.system['/incomes/fees']
        target_account = gas.system['/cash']
        amount = gas.membership_fee
        description = "Membership fee for year %(year)s" % {'year': year,}
        issuer = person 
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='MEMBERSHIP_FEE')
        transaction.add_references([person, gas])

    def last_entry(self, base_path):
        """last entry for one subject"""
        rv = LedgerEntry.objects.none()
        latest = self.system[base_path].ledger_entries.latest('transaction__date')
        if latest:
            return latest
        return rv
        #FIXME: create last_entry or one method for each base_path? Encapsulation and refactoring
        #FIXME: self <gasistafelice.base.accounting.PersonAccountingProxy object at 0xabaf86c>
        #       base_path '/expenses/gas/gas-1/recharges'



    def do_recharge(self, gas, amount, refs=None):
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
            entry_point =  gas.system['/incomes/recharges']
            target_account = gas.system['/members/' + person.uid]
            description = "GAS member account recharge"
            issuer = person
            transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='RECHARGE')
            transaction.add_references([person, gas])

    def entries(self, base_path='/'):
        """
        List all transactions. Return LedgerEntry (account, transaction, amount)
        """
        return self.system[base_path].ledger_entries

