"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base.models import Place 
from gasistafelice.gas.models import GAS, GASMember, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.gas.const import STATES_LIST

from workflows.models import Workflow
from workflows.utils import get_workflow

if not Workflow.objects.get(name="DefaultOrder"):
    from gasistafelice.gas.utils import init_workflow
    init_workflow()

class GASSupplierStock(models.Model):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    gas = models.ForeignKey(GAS)
    supplier_stock = models.ForeignKey(SupplierStock)
    # if a Product is available to GAS Members; policy is GAS-specific
    enabled = models.BooleanField()    
    ## constraints on what a single GAS Member is able to order
    # minimun amount of Product units a GAS Member is able to order 
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) after `order_minimum_amount`; 
    # useful when a Product ships in packages containing multiple units. 
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    

    @property
    def supplier(self):
        return self.supplier_stock.supplier

    @property
    def price(self):
        # Product base price as updated by agreements contained in GASSupplierSolidalPact
        price_percent_update = GASSupplierSolidalPact.objects.get(gas=self.gas, supplier=self.supplier).order_price_percent_update
        return self.supplier_stock.price*(1 + price_percent_update)

class GASSupplierOrder(models.Model):
    """An order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * status is a meaningful parameter... TODO
    * product_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_start = models.DateTimeField(help_text=_("when the order will be opened"))
    date_end = models.DateTimeField(help_text=_("when the order will be closed"))
    # Where and when delivery occurs
    # TODO: factor out delivery information in a `DeliveryAppointment` model class
    delivery_date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"))
    delivery_place = models.ForeignKey('Place', related_name="deliveries", help_text=_("where the order will be delivered by supplier"))
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier  
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True) # FIXME: should be a `CurrencyField` ?
    # Where and when withdrawal occurs
    # TODO: factor out withdrawal information in a `WithdrawalAppointment` model class
    withdrawal_date = models.DateTimeField(help_text=_("when the order will be withdrawn by GAS members"))
    withdrawal_place = models.ForeignKey('Place', related_name="withdrawals", help_text=_("where the order will be withdrawn by GAS members"))

    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    products = models.ManyToManyField(GASSupplierStock, help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    def save(self):
        # If no Products has been associated to this order, then use every Product bound to the Supplier
        super(GASSupplierOrder, self).save()
        if not self.products.all():
            for product in self.supplier.product_catalog:
                self.products.add(product)
        return

class GASSupplierOrderProduct(models.Model):

    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    order = models.ForeignKey(GASSupplierOrder)
    stock = models.ForeignKey(GASSupplierStock)
    # how many units of Product a GAS Member can request during this GASSupplierOrder
    # useful for Products with a low availability
    maximum_amount = models.PositiveIntegerField(blank=True, default=0)
    # the price of the Product at the time the GASSupplierOrder was sent to the Supplier
    ordered_price = models.FloatField(blank=True) # FIXME: should be a `CurrencyField` ?
    # the actual price of the Product (as resulting from the invoice)
    delivered_price = models.FloatField(blank=True) # FIXME: should be a `CurrencyField` ?
    # how many items were actually delivered by the Supplier 
    delivered_amount = models.PositiveIntegerField(blank=True)
    
    # how many items of this kind were ordered (globally by the GAS)
    @property
    def ordered_amount(self):
        # grab all GASMemberOrders related to this product
        orders = GASMemberOrder.objects.filter(product=self)
        amount = 0 
        for order in orders:
            amount=+ order.ordered_amount
        return amount 
    
class GASMemberOrder(models.Model):
    """An order made by a GAS member in the context of a given GASSupplierOrder.

    See `here http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineGasista`__  for details (ITA only).

    """

    purchaser = models.ForeignKey(GASMember)
    product = models.ForeignKey(GASSupplierOrderProduct)
    # price of the Product at order time
    ordered_price = models.FloatField(blank=True) # FIXME: should be a `CurrencyField` ?
    # how many Product units were ordered by the GAS member
    ordered_amount = models.PositiveIntegerField(blank=True)
    # how many Product units were withdrawn by the GAS member 
    withdrawn_amount = models.PositiveIntegerField(blank=True)
    
    # how much the GAS member actually payed for this Product (as resulting from the invoice)   
    @property
    def actual_price(self):
        return self.product.delivered_price
    
    # GASSupplierOrder this GASMemberOrder belongs to
    @property
    def order(self):
        return self.product.order 
    # which GAS this order was issued to ? 
    @property
    def gas(self):
        return self.purchaser.gas

    # Workflow management

    @property
    def workflow(self):
        return get_workflow(self)

    @workflow.set
    def workflow(self, value=None):
        raise AttributeError(_("Workflow for specific order is not allowed. Just provide a default order workflow for your GAS"))

    def forward(self):
        """Apply default transition"""
        #TODO!
        default_workflow = self.gas.workflow_default_gasmember_order
        transition = default_workflow. #TODO! Serie di stati o serie di transizioni? TODO
        

    def save(self):
        if not self.workflow:
            # Set default workflow
            w = self.gas.workflow_default_gasmember_order.workflow
            set_workflow(self, w)

        return super(GASMemberOrder, self).save()

