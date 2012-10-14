from django.utils.translation import ugettext as ug, ugettext_lazy as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry, account_type
from simple_accounting.utils import register_transaction

from gasistafelice.consts import INCOME, EXPENSE, PACT_EXTRA
from datetime import datetime

class SupplierAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``Supplier``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``Supplier``' model.
    """
        
    def confirm_invoice_payment(self, invoice):
        """
        Confirm that an invoice issued by this supplier has been actually payed.
        
        If ``invoice`` isn't an ``Invoice`` model instance, or if it was issued by another subject,
        raise ``ValueError``.
        """
        self.set_invoice_payed(invoice)

#    def refund_gas(self, gas, amount, refs=None):
#        """
#        Refund a given ``amount`` of money to a GAS for which a solidal pact 
#        is currently active.
#        
#        If GAS ``gas`` doesn't have an active solidal pact with this supplier, 
#        or if ``amount`` is negative, raise a ``MalformedTransaction`` exception.
#        
#        References for this transaction may be passed as the ``refs`` argument
#        (e.g. a list of supplier orders this refund is related to).
#        """
#        if amount < 0:
#            raise MalformedTransaction(_("Refund amounts must be non-negative"))
#        supplier = self.subject.instance
#        
#        if supplier not in gas.suppliers:
#            msg = _("An active solidal pact must be in place between a supplier and the GAS (s)he is refunding")
#            raise MalformedTransaction(msg)
#        
#        source_account = self.system['/wallet']
#        exit_point = self.system['/incomes/gas/' + gas.uid]
#        entry_point = gas.system['/expenses/suppliers/' + supplier.uid]
#        target_account = gas.system['/cash']
#        description = _("Refund for %(gas)s <-- %(supplier)s ") % {'gas': gas.id_in_des, 'supplier': supplier,}
#        issuer = supplier 
#        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, date, 'REFUND')
#        if refs:
#            transaction.add_references(refs)

    def entries(self, base_path='/'):
        """
        List all transactions. Return LedgerEntry (account, transaction, amount)
        """
        return self.system[base_path].ledger_entries

    def entries_pact(self, gas):
        """
        List all transactions for one pact. Return LedgerEntry (account, transaction, amount)
        """
        #UGLY: remove me when done and executed one command that regenerate all missing accounts
        self.missing_accounts(gas)

        supplier = self.subject.instance
        gas_system = gas.accounting.system

        #This is the DES transactions
        #accounts = self.system.accounts.filter(name="wallet")
        #PACT economics operations
        accounts = self.system.accounts.filter(parent__name='gas', name=gas.uid) | \
            gas_system.accounts.filter(parent__name='suppliers', name=supplier.uid)


        #COMMENT domthu: ?? they are entry or exit point -> transaction not account??
        #accounts = self.system.accounts.filter(name='/expenses/gas/' + gas.uid) 
        #accounts = self.system.accounts.filter(parent__name='incomes/gas', name=gas.uid) 
        #accounts = self.system.accounts.filter(parent__name='gas', name=gas.uid) 
        # supplier.system --> 'expenses/gas/' + gas.uid
        # supplier.system --> 'incomes/gas/' + gas.uid
        # gas.system --> 'expenses/suppliers/' + supplier.uid
        # gas.system --> 'incomes/suppliers/' + supplier.uid
        #accounts = gas_system.accounts.filter(parent__name='suppliers', name=supplier.uid)

        #TODO: retrieve transition for and return LedgerEntry 
        #transactions = self.subject.issued_transactions_set.get_by_reference([person])
        #transactions = transactions.filter(
        #    kind=GasAccountingProxy.MEMBERSHIP_FEE
        #)
        #return self.system['/wallet'].ledger_entries.filter(transaction__in=transactions)

        return LedgerEntry.objects.filter(account__in=accounts).order_by('-id', '-transaction__date')
        
        

    def extra_operation(self, gas, pact, amount, target, causal, date):
        """
        Another account operation for this subject

        For a Supplier the target operation can be income or expense operation with GAS
        """

        if amount < 0:
            raise MalformedTransaction(_("Payment amounts must be non-negative"))
        if amount < 0:
            raise MalformedTransaction(_("Refund amounts must be non-negative"))
        supplier = self.subject.instance

        if supplier not in gas.suppliers:
            msg = _("An active solidal pact must be in place between a supplier and the GAS (s)he is refunding")
            raise MalformedTransaction(msg)

        gas_acc = gas.accounting
        gas_system = gas.accounting.system

        #Correzione a favore del GAS: +GAS -fornitore
        if target == EXPENSE: #+GAS -Supplier

            #UGLY: remove me when done and executed one command that regenerate all missing accounts
            self.missing_accounts(gas)

            source_account = self.system['/wallet']
            exit_point = self.system['/expenses/gas/' + gas.uid]
            entry_point = gas_system['/incomes/suppliers/' + supplier.uid]
            target_account = gas_system['/cash']

        #Correzione a favore del fornitore: +fornitore -GAS
        elif  target == INCOME: #+Supplier -GAS
            source_account = gas_system['/cash']
            exit_point = gas_system['/expenses/suppliers/' + supplier.uid]
            entry_point = self.system['/incomes/gas/' + gas.uid]
            target_account = self.system['/wallet']

        else:
            raise MalformedTransaction(_("Payment target %s not identified") % target)

        description = "%(pact)s %(target)s %(causal)s" % {
            'pact': pact,
            'target': target,
            'causal': causal
        }
        issuer = self.subject
        kind = PACT_EXTRA
        if not date:
            date = datetime.now()  #_date.today
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, date, kind)

    def create_account(self, parent_path, name, kind, is_placeholder=None):
        if parent_path == '/':
          path = parent_path + name
        else:
          path = parent_path + '/' + name
        try:
            account = self.system[path]
        except:
            #if not exist create it
            if is_placeholder:
                self.system.add_account(parent_path=parent_path, name=name, kind=kind, is_placeholder=is_placeholder)
            else:
                self.system.add_account(parent_path=parent_path, name=name, kind=kind)
            account = self.system[path]
        if not account:
            raise MalformedTransaction(ugettext("Unknow create account: %(system)s %(path)s %(name)s %(kind)s %(is_placeholder)s") % {
                'system': self.system,
                'path': path,
                'name': name,
                'kind': kind,
                'is_placeholder': is_placeholder
            })

    #UGLY: remove me when done and executed one command that regenerate all missing accounts
    def missing_accounts(self, gas):
        supplier = self.subject.instance
        gas_acc = gas.accounting
        gas_system = gas.accounting.system
        #COMMENT: ensure all path exist --> add_account do not construct all tree
        xsys = gas_acc.get_account(self.system, '/expenses', 'gas', account_type.expense)
        xsys = gas_acc.get_account(self.system, '/expenses/gas', gas.uid, account_type.expense)
        xsys = gas_acc.get_account(gas_system, '/incomes', 'suppliers', account_type.income)
        xsys = gas_acc.get_account(gas_system, '/incomes/suppliers', supplier.uid, account_type.income)

