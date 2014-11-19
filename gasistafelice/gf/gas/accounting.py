from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from simple_accounting.exceptions import MalformedTransaction
from simple_accounting.models import (AccountingProxy, Transaction, 
    LedgerEntry, account_type, TransactionReference
)
from simple_accounting.utils import (register_transaction, 
    register_simple_transaction, transaction_details, 
    update_transaction
)

from gf.base.models import Person
from consts import INCOME, EXPENSE, GAS_EXTRA
import datetime

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
    
    GAS_WITHDRAWAL = 'GAS_WITHDRAWAL'
    MEMBERSHIP_FEE = 'MEMBERSHIP_FEE'

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
            raise MalformedTransaction(ugettext(u"Payment amounts must be non-negative"))
        gas = self.subject.instance
        supplier = order.supplier
        source_account = self.system['/cash']
        exit_point = self.system['/expenses/suppliers/' + supplier.uid]
        entry_point =  supplier.accounting.system['/incomes/gas/' + gas.uid]
        target_account = supplier.accounting.system['/wallet']
        if multiple:
            description = "Ord. %s" % multiple
            description += " %(pact)s" % {'pact': order.pact,}
        else:
            description = order.common_name

        if descr:
            description += ". %s" % descr.replace(description + ". ", "")
        issuer =  self.subject
        transaction = register_transaction(source_account, exit_point, entry_point, 
            target_account, amount, description, issuer, date, 'PAYMENT'
        )
        if refs:
            transaction.add_references(refs)

    def withdraw_from_member_account_update(self, member, updated_amount, refs, date=None):
        """
        WARNING: if you use this method you lose history of updates
        """

        tx = Transaction.objects.get_by_reference(refs).get(kind=GasAccountingProxy.GAS_WITHDRAWAL)
        if tx:
            # WARNING: if you update a transaction, you will lose old transaction info. Use with care!
            update_transaction(tx, amount=updated_amount, date=date)
            return True
        return False

    def get_amount_by_gas_member(self, gasmember, order):
        """
        Given a supplier order ``order``, return an annotated set for a specific GAS members
        partecipating to that order.

        If ``order`` has not been placed by the GAS owning this accounting system,
        raise ``TypeError``.

        20120227 This function is deprecated because we do not use mulitple GAS_WITHDRAWAL for one reference [gasmember, order]
        but we use only one GAS_WITHDRAWAL transaction with update. 
        """
        from django.db.models import Count, Sum
     
        gas = self.subject.instance
        existing_amount = 0
        if order.pact.gas == gas:

            #refs = [gm, self.__order] in cash.py
            order_txs = Transaction.objects.get_by_reference([gasmember, order])
            order_txs = order_txs.filter(kind=GasAccountingProxy.GAS_WITHDRAWAL)
            #Fixme: 
            existing_amount = order_txs.aggregate(Sum('source__amount'))
            number_of_txs = order_txs.count()
            return existing_amount, number_of_txs
            
        else:
            raise TypeError(_("GAS %(gas)s has not placed order %(order)s" % {
                'gas': gas.id_in_des, 'order': order
            }))

    def withdraw_from_member_account(self, member, new_amount, refs, order, date=None, comment=""):
        """
        Withdraw a given amount ``new_amount`` of money from the account of a member
        of this GAS and bestow it to the GAS's cash.
        
        If this operation would make that member's account negative, raise a warning.

        If ``member`` is not a member of this GAS, a ``MalformedTransaction`` exception is raised.
        
        References for this transaction may be passed as the ``refs`` argument
        (e.g. a list of GAS member orders this withdrawal is related to).
        """
        # Only for test Control if yet exist some transaction for this refs.
        #computed_amount, existing_txs = self.get_amount_by_gas_member(member, order)
        #log.debug("ACCOUNTING %(computed_amount)s %(existing_txs)s" % {'computed_amount': computed_amount, 'existing_txs': existing_txs})

        gas = self.subject.instance
        if member.gas != gas:
            raise MalformedTransaction(ugettext("A GAS can withdraw only from its members' accounts"))
        source_account = self.system['/members/' + member.person.uid]
        target_account = self.system['/cash']
        #'gas': gas.id_in_des,
        #WAS: description = "%(person)s %(order)s" % {'person': member.person.report_name, 'order': order.report_name}
        #NOTE LF: person is a repetition of gasmember person bound
        description = order.common_name
        if comment:
            description = u"%s (%s)" % (description, comment)
        issuer = self.subject
        log.debug("registering transaction: issuer=%s descr=%s source=%s target=%s" % (
            issuer, description, source_account, target_account
        ))
        transaction = register_simple_transaction(source_account, target_account, new_amount, 
            description, issuer, date=date, kind=GasAccountingProxy.GAS_WITHDRAWAL
        )
        if refs:
            transaction.add_references(refs)

        # TODO: if this operation would make member's account negative, raise a warning

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
#        from gf.gas.models import GASSupplierOrder
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
                #simple accounting: transaction.ledger_entries.delete() but do not recreate the link to the original refs that permit to retrieve the transaction itself finding by order. see: get_supplier_order_data
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
        
        A (member) order is considered to be "accounted" if a transaction recording it
        exists within that GAS's accounting system.
        
        If ``order`` has not been placed by the GAS owning this accounting system,
        raise ``TypeError``.
        """
        from gf.gas.models import GASMember

        gas = self.subject.instance
        if order.pact.gas == gas:

            order_txs = Transaction.objects.get_by_reference([order])
            order_txs = order_txs.filter(kind=GasAccountingProxy.GAS_WITHDRAWAL)

            ctype_gm = ContentType.objects.get_for_model(GASMember)

            members_d = {}

            # For each WITHDRAW related to the order
            for tx in order_txs:

                try:
                    # Retrieve GASMember reference
                    gm_ref = tx.reference_set.get(content_type=ctype_gm)
                except TransactionReference.DoesNotExist as e:
                    # We have hit a WITHDRAW related to order, 
                    # but not to a GASMember
                    pass
                else:
                    #KO: we cannot use .instance attribute
                    #KO: because it excludes suspended gasmembers and inactive users
                    #KO: gm = gm_ref.instance
                    gm = GASMember.all_objects.get(pk=gm_ref.object_id)
                    members_d[gm] = members_d.get(gm,0) + tx.source.amount

            members = set()
            for gm, amount in members_d.items():
                gm.accounted_amount = amount
                members.add(gm)

            return members
            
        else:
            raise TypeError(ugettext("GAS %(gas)s has not placed order %(order)s" % {
                'gas': gas.id_in_des, 'order': order
            }))

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
            raise MalformedTransaction(ugettext("Payment amounts must be non-negative"))
        gas = self.subject.instance
        non_des = self.get_non_des_accounting()
        if not non_des:
            raise Person.DoesNotExist
        non_des_system = non_des.system
        if target == INCOME:
            source_account = non_des_system['/wallet']
            exit_point, created = non_des_system.get_or_create_account('/expenses', 'OutOfDES', account_type.expense)
            entry_point = self.system['/incomes/OutOfDES']
            target_account = self.system['/cash']   #WAS gas.accounting.system['/cash']
        elif  target == EXPENSE:
            source_account = self.system['/cash']
            exit_point = self.system['/expenses/OutOfDES']
            entry_point, created = non_des_system.get_or_create_account('/incomes', 'OutOfDES', account_type.income)
            target_account = non_des_system['/wallet']
        else:
            #WAS raise MalformedTransaction(ugettext("Payment target %s not identified" % target))
            #coercing to Unicode: need string or buffer, __proxy__ found
            raise MalformedTransaction(ugettext("Payment target %s not identified") % target)

        description = "%(gas)s %(target)s %(causal)s" % {
            'gas': gas.id_in_des,
            'target': target,
            'causal': causal
        }
        #WAS raise description = ugettext("%(gas)s %(target)s %(causal)s") % { ...
        #WAS exceptions must be old-style classes or derived from BaseException, not unicode

        issuer = self.subject
        kind = GAS_EXTRA
        if not date:
            date = datetime.datetime.now()  #_date.today
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
        except Exception as e: #should be KeyError, but maybe is an AttributeError due to previous implementation
#WAS        if not account: but raise exception "Account matching query does not exist."
            #if not exist create it
            system.add_account(parent_path=parent_path, name=name, kind=kind)
            account = system[path]
        if not account:
            raise MalformedTransaction(ugettext("Unknow account: %(system)s %(path)s %(kind)s") % {
                'system': system,
                'path': path,
                'kind': kind
            })
        return account

    def get_non_des_accounting(self):
        des = self.subject.instance.des
        return des.accounting

    def pay_membership_fee(self, member, year, date=None):
        """
        Pay the annual membership fee for this GAS member.
        
        Fee amount is determined by the ``gas.membership_fee`` attribute.
        
        If the gas member belongs to another ``gas``, 
        a ``MalformedTransaction`` exception is raised.
        """
        gas = self.subject.instance
        if member.gas != gas:
            raise MalformedTransaction(ugettext("A person can't pay membership fees to a GAS that (s)he is not member of"))

        person = member.person
        source_account = self.system['/members/' + person.uid]
        target_account = self.system['/cash']

        amount = gas.membership_fee
        description = ugettext("year %(year)s --> %(person)s") % {'person': person.report_name, 'year': year,}
        issuer = self.subject
        if not date:
            date = datetime.datetime.now()  #_date.today

        transaction = register_simple_transaction(source_account, target_account, 
            amount, description, issuer, date, kind=GasAccountingProxy.MEMBERSHIP_FEE
        )
        transaction.add_references([person, gas])


    def last_person_fee(self, person):
        """Get latest membership fee paid by a person.

        Return None if this person is not ever been member of the GAS.

        Person parameter is preferred instead of member parameter because membership is temporary
        """

        transactions = self.subject.issued_transactions_set.get_by_reference([person])
        transactions = transactions.filter(
            kind=GasAccountingProxy.MEMBERSHIP_FEE
        )
        fees = self.system['/cash'].ledger_entries.filter(transaction__in=transactions)

        try:
            last_fee = fees.latest('transaction__date')
        except LedgerEntry.DoesNotExist:
            last_fee = None
        return last_fee

