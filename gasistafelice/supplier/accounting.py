from django.utils.translation import ugettext as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry
from simple_accounting.utils import register_transaction, register_simple_transaction, transaction_details


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
    
    def refund_gas(self, gas, amount, refs=None):
        """
        Refund a given ``amount`` of money to a GAS for which a solidal pact 
        is currently active.
        
        If GAS ``gas`` doesn't have an active solidal pact with this supplier, 
        or if ``amount`` is negative, raise a ``MalformedTransaction`` exception.
        
        References for this transaction may be passed as the ``refs`` argument
        (e.g. a list of supplier orders this refund is related to).
        """
        if amount < 0:
            raise MalformedTransaction("Refund amounts must be non-negative")
        supplier = self.subject.instance
        
        if supplier not in gas.suppliers:
            msg = "An active solidal pact must be in place between a supplier and the GAS (s)he is refunding"
            raise MalformedTransaction(msg)
        
        source_account = self.system['/wallet']
        exit_point = self.system['/incomes/gas/' + gas.uid]
        entry_point = gas.system['/expenses/suppliers/' + supplier.uid] 
        target_account = gas.system['/cash']
        description = _("Refund from supplier %(supplier)s to GAS %(gas)s") % {'gas': gas, 'supplier': supplier,}
        issuer = supplier 
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='REFUND')
        if refs:
            transaction.add_references(refs)

    def entries(self, base_path='/'):
        """
        List all transactions. Return LedgerEntry (account, transaction, amount)
        """
        return self.system[base_path].ledger_entries


