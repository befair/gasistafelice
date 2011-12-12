from django.utils.translation import ugettext as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry
from simple_accounting.utils import register_transaction, register_simple_transaction, transaction_details, update_transaction

from gasistafelice.base.models import Person

class GasAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``GAS``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``GAS``' model.    
    """
    
    def pay_supplier(self, order, amount, refs=None, descr=None):
        """
        Transfer a given (positive) amount ``amount`` of money from the GAS's cash
        to a supplier for which a solidal pact is currently active.
        
        If ``amount`` is negative, a ``MalformedTransaction`` exception is raised
        (supplier-to-GAS money transfers should be treated as "refunds").
        
        References for this transaction may be passed as the ``refs`` argument
        (e.g. a list of supplier orders this payment is related to).   
        """
        if amount < 0:
            raise MalformedTransaction("Payment amounts must be non-negative")
        #gas = order.gas
        gas = self.subject.instance
        supplier = order.supplier
        source_account = self.system['/cash']
        exit_point = self.system['/expenses/suppliers/' + supplier.uid]
        entry_point =  supplier.accounting.system['/incomes/gas/' + gas.uid]
        target_account = supplier.accounting.system['/wallet']
        description = _("Ord.%(pk)s %(gas)s --> %(supplier)s") % {'pk': order.pk, 'gas': gas.id_in_des, 'supplier': supplier,}
        if descr:
            description += ". %s" % descr
        #issuer = gas Not the instance
        issuer =  self.subject
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='PAYMENT')
        if refs:
            transaction.add_references(refs)

    def withdraw_from_member_account_update(self, member, updated_amount, refs):

        tx = Transaction.objects.get_by_reference(refs).get(kind='GAS_WITHDRAWAL')
        if tx:
            update_transaction(tx, amount=updated_amount)
            return True
        return False

    def withdraw_from_member_account(self, member, new_amount, refs=None):
        """
        Withdraw a given amount ``new_amount`` of money from the account of a member
        of this GAS and bestow it to the GAS's cash.
        
        If this operation would make that member's account negative, raise a warning.

        If ``member`` is not a member of this GAS, a ``MalformedTransaction`` exception is raised.
        
        References for this transaction may be passed as the ``refs`` argument
        (e.g. a list of GAS member orders this withdrawal is related to).
        """
        # TODO: if this operation would make member's account negative, raise a warning
        gas = self.subject.instance
        if not member.person.is_member(gas):
            raise MalformedTransaction("A GAS can withdraw only from its members' accounts")
        source_account = self.system['/members/' + member.person.uid]
        target_account = self.system['/cash']
        description = _("GAS %(gas)s <-> %(person)s") % {'gas': gas.id_in_des, 'person': member.person,}
        issuer = self.subject
        transaction = register_simple_transaction(source_account, target_account, new_amount, description, issuer, date=None, kind='GAS_WITHDRAWAL')
        if refs:
            transaction.add_references(refs)

    def pay_supplier_order(self, order, amount, refs=None, descr=None):
        """
        Register the payment of a supplier order.

        1 Control if not yet exist a payment for this order

        2 Control if Total amounted for Members are equal or not. If not compense the difference automaticaly? Ask to the comunity. For the moment do nothing.
        """

#        Specifically, such registration is a two-step process:
#        1. First, the GAS withdraws from each member's account an amount of money corresponding
#           to the total cost of products (s)he bought during this order 
#           (price & quantity are as recorded by the invoice!)
#        2. Then, the GAS collects this money amounts and transfers them to the supplier's account 
#        If the given supplier order hasn't been fully withdrawn by GAS members yet, raise ``MalformedTransaction``.
#        from gasistafelice.gas.models import GASSupplierOrder
#        # FIXME: adapt to "Gasista Felice"'s workflow model
#        if order.status == GASSupplierOrder.WITHDRAWN:
#            ## bill members for their orders to the GAS
#            # only members participating to this order need to be billed
#            for member in order.purchasers:
#                # calculate amount to bill to this GAS member for orders (s)he issued 
#                # w.r.t. the given supplier order 
#                member_order_bill = 0 
#                issued_member_orders = member.issued_orders.filter(ordered_product__order=order)
#                for member_order in issued_member_orders:
#                    price = member_order.ordered_product.delivered_price
#                    quantity = member_order.withdrawn_amount 
#                    member_order_bill += price * quantity
#                self.withdraw_from_member_account(member, member_order_bill)
            ## pay supplier
#            self.pay_supplier(pact=order.pact, amount=order.total_amount)
#        else:
#            raise MalformedTransaction("Only fully withdrawn supplier orders are eligible to be payed")

        #retrieve existing payment
        if not refs:
            refs = [order]
        yet_payed, description = self.get_supplier_order_data(order, refs)
        if yet_payed <= 0:
            # pay supplier
            self.pay_supplier(order=order, amount=amount, refs=refs, descr=descr)
        elif yet_payed != amount:
            #TODO: ECO update payment
            tx = self.get_supplier_order_transaction(self, order, refs)
            if tx:
                update_transaction(tx, amount=amount)

    def get_supplier_order_data(self, order, refs=None):
        """
        Get amounted payment and description for one order transaction
        """
        if not refs:
            refs = [order]
        tx = self.get_supplier_order_transaction(order, refs)
        if tx:
            return tx.source.amount, tx.description
        else:
            return 0, ''

    def get_supplier_order_transaction(self, order, refs=None):
        """
        Get transaction payment for one order
        """
        if not refs:
            refs = [order]
        try:
            tx = Transaction.objects.get_by_reference(refs).get(kind='PAYMENT')
        except Transaction.DoesNotExist:
            return None
        else:
            return tx

    def accounted_amount_by_gas_member(self, order):
        """
        Given a supplier order ``order``, return an annotated set of GAS members
        partecipating to that order.
        
        Each GAS member instance will have an ``.accounted_amount`` attribute,
        representing the total amount of money already accounted for with respect 
        to the entire set of orders placed by that GAS member within ``order``.
        
        A (member) order is considered to be "accounted" iff a transaction recording it
        exists within that GAS's accounting system.
        
        If ``order`` has not been placed by the GAS owning this accounting system,
        raise ``TypeError``.
        """
        gas = self.subject.instance
        if order.pact.gas == gas:
            members = set()
            for member in order.purchasers:
                # retrieve transactions related to this GAS member and order,
                # including only withdrawals made by the GAS from members' accounts
                #NOTE: DOMTHU useful for list 
                #txs = Transaction.objects.get_by_reference([member, order]).filter(kind='GAS_WITHDRAWAL')
                #member.accounted_amount = sum([tx.source.amount for tx in txs])
                #NOTE: in this method we MUST have only one transaction 
                # for each (member, order) couple
                try:
                    tx = Transaction.objects.get_by_reference([member, order]).get(kind='GAS_WITHDRAWAL')
                except Transaction.DoesNotExist:
                    member.accounted_amount = None
                else:
                    member.accounted_amount = tx.source.amount

                members.add(member)
            return members
        else:
            raise TypeError("GAS %(gas)s has not placed order %(order)s" % {'gas': gas.id_in_des, 'order': order})

    def account_entries(self, base_path='/'):
        pass

    def entries(self):
        """
        List all LedgerEntries (account, transaction, amount)

        Show transactions for suppliers link to GAS  kind='PAYMENT' + another kind?
        Show transactions for gasmembers link to GAS kind='GAS_WITHDRAWAL' + another kind?
        Show transactions for GAS  from CASH system what kind?
        """

        gm_people = Person.objects.filter(gasmember__in=self.subject.instance.gasmembers)
        members_account = map(lambda p : p.uid, gm_people)
        suppliers = self.subject.instance.suppliers
        s_account = map(lambda s : s.uid, suppliers)
        accounts = self.system.accounts.filter(name="cash") | \
            self.system.accounts.filter(parent__name="members", name__in=members_account) | \
            self.system.accounts.filter(parent__name="suppliers", name__in=s_account)

        return LedgerEntry.objects.filter(account__in=accounts)


