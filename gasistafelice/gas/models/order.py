"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.models import Resource, Place, DefaultTransition
from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.auth.utils import register_parametric_role
from gasistafelice.auth import GAS_REFERRER_ORDER, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL

from workflows.models import Workflow
from workflows.utils import get_workflow, get_state, do_transition

class GASSupplierStock(Resource, PermissionBase, models.Model):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    gas = models.ForeignKey(GAS)
    supplier_stock = models.ForeignKey(SupplierStock)
    # if a Product is available to GAS Members; policy is GAS-specific
    enabled = models.BooleanField()    
    ## constraints on what a single GAS Member is able to order
    # minimun amount of Product units a GAS Member is able to order 
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum; 
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
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
    class Meta:
        app_label = 'gas'


class GASSupplierOrder(Resource, PermissionBase, models.Model):
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
    # Where and when Delivery occurs
    delivery = models.ForeignKey('Delivery', related_name="supplier_orders")
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier  
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True) # FIXME: should be a `CurrencyField` ?
    # Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', related_name="supplier_orders")
    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    products = models.ManyToManyField(GASSupplierStock, help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    def setup_roles(self):
        # register a new `GAS_REFERRER_ORDER` Role for this GASSupplierOrder
        register_parametric_role(name=GAS_REFERRER_ORDER, param1=self)
        
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    def save(self):
        super(GASSupplierOrder, self).save()
        # If no Products has been associated to this order, then use every Product bound to the Supplier        
        if not self.products.all():
            for product in self.supplier.product_catalog:
                self.products.add(product)
        return
        
    class Meta:
        app_label = 'gas'

class GASSupplierOrderProduct(Resource, PermissionBase, models.Model):

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
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
    class Meta:
        app_label = 'gas'

class GASMemberOrder(Resource, PermissionBase, models.Model):
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

    @workflow.setter
    def workflow(self, value=None):
        raise AttributeError(_("Workflow for specific GASMemberOrder is not allowed. Just provide a default order workflow for your GAS"))

    def forward(self, user):
        """Apply default transition"""
        state = get_state(self)
        transition = DefaultTransition.objects.get(workflow=self.workflow, state=state).transition
        do_transition(self, transition, user)
        
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    def save(self):
        if not self.workflow:
            # Set default workflow
            w = self.gas.workflow_default_gasmember_order.workflow
            set_workflow(self, w)

        return super(GASMemberOrder, self).save()

    class Meta:
        app_label = 'gas'

class Delivery(Resource, PermissionBase, models.Model):
    """
    A delivery appointment, i.e. an event where one or more Suppliers deliver goods 
    associated with SupplierOrders issued by a given GAS (or Retina of GAS).  
    """
    
    place = models.ForeignKey(Place, related_name="deliveries", help_text=_("where the order will be delivered by supplier"))
    date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"))    
    # GAS referrers for this Delivery appointment (if any) 
    referrers = models.ManyToManyField(GASMember, null=True, blank=True)
    
    def setup_roles(self):
        # register a new `GAS_REFERRER_DELIVERY` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_DELIVERY, param1=self)            
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
    class Meta:
        app_label = 'gas'


class Withdrawal(Resource, PermissionBase, models.Model):
    """
    A wihtdrawal appointment, i.e. an event where a GAS (or Retina of GAS) distribute 
    to their GASMembers goods they ordered issuing GASMemberOrders to the GAS/Retina.  
    """
    
    place = models.ForeignKey(Place, related_name="withdrawals", help_text=_("where the order will be withdrawn by GAS members"))
    # a Withdrawal appointment usually span a time interval
    start_time = models.TimeField(help_text=_("when the withdrawal will start"))
    end_time = models.TimeField(help_text=_("when the withdrawal will end"))
    # GAS referrers for this Withdrawal appointment  
    referrers = models.ManyToManyField(GASMember)
    
    def setup_roles(self):
        # register a new `GAS_REFERRER_WITHDRAWAL` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_WITHDRAWAL, param1=self)   
        
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv 
    
    class Meta:
        app_label = 'gas'

