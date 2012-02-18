from django.utils.translation import ugettext as ug, ugettext_lazy as _

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import AccountingProxy, Transaction, LedgerEntry, account_type
from simple_accounting.utils import register_transaction, register_simple_transaction, transaction_details, update_transaction

from gasistafelice.base.models import Person
from gasistafelice.consts import INCOME, EXPENSE
from datetime import datetime

import logging
log = logging.getLogger(__name__)

class GasAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``GAS``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``GAS``' model.    
    """
    
    def pay_supplier(self, order, amount, refs=None, descr=None, date=None, multiple=None):
        """
        Transfer a given (positive) amount ``amount`` of money from the GAS's cash
        to a supplier for which a solidal pact is currently active.
        
        If ``amount`` is negative, a ``MalformedTransaction`` exception is raised
        (supplier-to-GAS money transfers should be treated as "refunds").
        
        References for this transaction may be passed as the ``refs`` argument
        (e.g. a list of supplier orders this payment is related to).   
        """
        if amount < 0:
            raise MalformedTransaction(ug(u"Payment amounts must be non-negative"))
        gas = self.subject.instance
        supplier = order.supplier
        source_account = self.system['/cash']
        exit_point = self.system['/expenses/suppliers/' + supplier.uid]
        entry_point =  supplier.accounting.system['/incomes/gas/' + gas.uid]
        target_account = supplier.accounting.system['/wallet']
        if multiple:
            description = "Ord.%s" % multiple
        else:
            description = "Ord.%s" % order.pk
        description += " %(gas)s --> %(supplier)s" % {'gas': gas.id_in_des, 'supplier': supplier,}
        if descr:
            description += ". %s" % descr.replace(description + ". ", "")
        issuer =  self.subject
        if not date:
            date = datetime.now()  #_date.today
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, date, 'PAYMENT')
        if refs:
            transaction.add_references(refs)

    def withdraw_from_member_account_update(self, member, updated_amount, refs, date):

        tx = Transaction.objects.get_by_reference(refs).get(kind='GAS_WITHDRAWAL')
        if tx:
            #FIXME: Update make me loose old transaction 
            update_transaction(tx, amount=updated_amount, date=date)
            return True
        return False

    def withdraw_from_member_account(self, member, new_amount, refs, order, date):
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
            raise MalformedTransaction(_("A GAS can withdraw only from its members' accounts"))
        source_account = self.system['/members/' + member.person.uid]
        target_account = self.system['/cash']
        #'gas': gas.id_in_des,
        description = "%(person)s %(order)s" % {'person': member.person.report_name, 'order': order.report_name}
        issuer = self.subject
        if not date:
            date = datetime.now()  #_date.today
        transaction = register_simple_transaction(source_account, target_account, new_amount, description, issuer, date=date, kind='GAS_WITHDRAWAL')
        if refs:
            transaction.add_references(refs)

    def pay_supplier_order(self, order, amount, refs=None, descr=None, date=None, multiple=None):
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
        yet_payed, description, date_payed = self.get_supplier_order_data(order, refs)
        #Insolute aggregated payment contain many orders that are payed in simultaneous. Refs must be a list of each order that are relative to this unique transaction
        if yet_payed <= 0:
            # pay supplier
            self.pay_supplier(order=order, amount=amount, refs=refs, descr=descr, date=date, multiple=multiple)
        elif yet_payed != amount:
            tx = self.get_supplier_order_transaction(order, refs)
            if tx:
                #FIXME: something wrong. The old transaction is deleted and the new one loose refs
                #simple accounting: transaction.ledger_entries.delete() but do not recreate the link to the original refs that permit to retrieve the transaction itsel finding by order. see: get_supplier_order_data
                update_transaction(tx, amount=amount)

    def get_supplier_order_data(self, order, refs=None):
        """
        Get amounted payment and description for one order transaction
        """
        if not refs:
            refs = [order]
        tx = self.get_supplier_order_transaction(order, refs)
        if tx:
            return tx.source.amount, tx.description, tx.date
        else:
            return 0, '', None

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
            raise TypeError(_("GAS %(gas)s has not placed order %(order)s" % {'gas': gas.id_in_des, 'order': order}))

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

        return LedgerEntry.objects.filter(account__in=accounts).order_by('-id', '-transaction__date')

    def extra_operation(self, amount, target, causal, date):
        """
        Another account operation for this subject

        For a GAS the target operation can be income or expense operation
        """

        if amount < 0:
            raise MalformedTransaction(_("Payment amounts must be non-negative"))
        gas = self.subject.instance
        non_des = self.get_non_des_accounting()
        if not non_des:
            raise Person.DoesNotExist
        non_des_system = non_des.system
        if target == INCOME:
            source_account = non_des_system['/wallet']
            exit_point = self.get_account(non_des_system, '/expenses', 'OutOfDES', account_type.expense)
            entry_point = self.get_account(self.system, '/incomes', 'OutOfDES', account_type.income)
            target_account = self.system['/cash']   #WAS gas.accounting.system['/cash']
        elif  target == EXPENSE:
            source_account = self.system['/cash']
            exit_point = self.get_account(self.system, '/expenses', 'OutOfDES', account_type.expense)
            entry_point = self.get_account(non_des_system, '/incomes', 'OutOfDES', account_type.income)
            target_account = non_des_system['/wallet']
        else:
            #WAS raise MalformedTransaction(_("Payment target %s not identified" % target))
            #coercing to Unicode: need string or buffer, __proxy__ found
            raise MalformedTransaction(ug("Payment target %s not identified") % target)

        description = "%(gas)s %(target)s %(causal)s" % {
            'gas': gas.id_in_des,
            'target': target,
            'causal': causal
        }
        #WAS raise description = _("%(gas)s %(target)s %(causal)s") % { ...
        #WAS exceptions must be old-style classes or derived from BaseException, not unicode

        issuer = self.subject
        kind = 'GAS_EXTRA'
        if not date:
            date = datetime.now()  #_date.today
#        transaction = register_simple_transaction(source_account, target_account, amount, description, issuer, date=date, kind=kind)
        transaction = register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, date, kind)

#        +----------- expenses [P,E]+
#        |                +--- TODO: OutOfDES
#        +----------- incomes [P,I]+
#        |                +--- TODO: OutOfDES

    def get_account(self, system, parent_path, name, kind):
        path = parent_path + '/' + name
        try:
            account = system[path]
        except:
#WAS        if not account: but raise exception "Account matching query does not exist."
            #if not exist create it
            system.add_account(parent_path=parent_path, name=name, kind=kind)
            account = system[path]
        if not account:
            raise MalformedTransaction(ug("Unknow account: %(system)s %(path)s %(kind)s") % {
            'system': system,
            'path': path,
            'kind': kind
        })
        return account

    def get_non_des_accounting(self):
        des = self.subject.instance.des
        try:
            return des.accounting
        except AttributeError as e:
            msg = _("calling non-existent out of DES account: %s") % e.message
            log.warning(msg)
            raise MalformedTransaction(msg)
