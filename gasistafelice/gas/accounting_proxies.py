from accounting.exceptions import MalformedTransaction
from accounting.models import AccountingProxy
from accounting.utils import register_transaction, register_simple_transaction


class GasAccountingProxy(AccountingProxy):
    """
    This class is meant to be the place where implementing the accounting API 
    for ``GAS``-like economic subjects.
    
    Since it's a subclass of  ``AccountingProxy``, it inherits from its parent 
    all the methods and attributes comprising the *generic* accounting API;
    here, you can add whatever logic is needed to augment that generic API,
    tailoring it to the specific needs of the ``GAS``' model.    
    """
    
    def pay_supplier(self, pact, amount):
        """
        Transfer a given (positive) amount ``amount`` of money from the GAS's cash
        to a supplier for which a solidal pact is currently active.
        
        If ``amount`` is negative, a ``MalformedTransaction`` exception is raised
        (supplier-to-GAS money transfers should be treated as "refunds")   
        """
        if amount < 0:
            raise MalformedTransaction("Payment amounts must be non-negative")
        gas = self.subject.instance
        supplier = pact.supplier
        source_account = self.system['/cash']
        exit_point = self.system['/expenses/suppliers/' + str(supplier.name)]
        entry_point =  supplier.system['/incomes/gas' + str(gas.name)]
        target_account = supplier.system['/wallet']
        description = "Payment from GAS %(gas)s to supplier %(supplier)s" % {'gas': gas, 'supplier': supplier,}
        issuer = gas 
        register_transaction(source_account, exit_point, entry_point, target_account, amount, description, issuer, kind='PAYMENT')
        
    def withdraw_from_member_account(self, member, amount):
        """
        Withdraw a given amount ``amount`` of money from the account of a member
        of this GAS and bestow it to the GAS's cash.
        
        If this operation would make that member's account negative, raise a warning.
        """
        # TODO: if this operation would make member's account negative, raise a warning
        gas = self.subject.instance
        source_account = self.system['/members/' + str(member.person.full_name)]
        target_account = self.system['/cash']
        description = "Withdrawal from member %(member)s account by GAS %(gas)s" % {'gas': gas, 'member': member,}
        issuer = gas 
        register_simple_transaction(source_account, target_account, amount, description, issuer, date=None, kind='GAS_WITHDRAWAL')
    
    def pay_supplier_order(self, order):
        """
        Register the payment of a supplier order.
        
        Specifically, such registration is a two-step process:
        1. First, the GAS withdraws from each member's account an amount of money corresponding
           to the price of products (s)he bought during this order 
           (price & quantity are as recorded by the invoice!)
        2. Then, the GAS collects this money amounts and transfers them to the supplier's account 
        
        If the given supplier order hasn't been fully withdrawn by GAS members yet, raise ``MalformedTransaction``.
        """
        from gasistafelice.gas.models import GASSupplierOrder
        # FIXME: adapt to "Gasista Felice"'s workflow model
        if order.status == GASSupplierOrder.WITHDRAWN:
            ## bill members for their orders to the GAS
            # only members participating to this order need to be billed
            for member in order.purchasers:
                # calculate amount to bill to this GAS member for orders (s)he issued 
                # w.r.t. the given supplier order 
                member_order_bill = 0 
                issued_member_orders = member.issued_orders.filter(ordered_product__order=order)
                for member_order in issued_member_orders:
                    price = member_order.ordered_product.delivered_price
                    quantity = member_order.withdrawn_amount 
                    member_order_bill += price * quantity               
                self.withdraw_from_member_account(member, member_order_bill)
            ## pay supplier
            self.pay_supplier(pact=order.pact, amount=order.total_amount)
        else:
            raise MalformedTransaction("Only fully withdrawn supplier orders are eligible to be payed")
    

