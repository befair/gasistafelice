"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base.models import Place, GASMember, GAS
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
        price_percent_update = self.gas.supplier_set.get(supplier=self.supplier).price_percent_update
        return self.supplier_stock.price*price_percent_update

class GASSupplierOrder(models.Model):
    """An Order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * status is a meaningful parameter... TODO
    * product_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_start = models.DateTimeField(help_text=_("when the order will be available"))
    date_end = models.DateTimeField(help_text=_("when the order will be closed"))
    # Where and when delivery occurs
    delivery_date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"))
    delivery_place = models.ForeignKey('Place', related_name="delivery_for_order_set", help_text=_("where the order will be delivered by supplier"))
    # How much has been delivered 
    delivery_amount = models.PositiveIntegerField()
    # Where and when withdraw occurs
    withdraw_date = models.DateTimeField(help_text=_("when the order will be withdrawn by GAS members"))
    withdraw_place = models.ForeignKey('Place', related_name="withdraw_for_order_set", help_text=_("where the order will be withdrawn by GAS members"))

    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    product_set = models.ManyToManyField(GASSupplierStock, help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    def save(self):
        # If no product_set has been specified --> use all products bound to the supplier
        super(GASSupplierOrder, self).save()
        if not self.product_set.all():
            for product in self.gas.supplier_set.get(self.supplier).all():
                self.product_set.add(product)
        return

class GASSupplierOrderProduct(models.Model):

    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    gassupplierorder = models.ForeignKey(GASSupplierOrder)
    gassupplierstock = models.ForeignKey(GASSupplierStock)

    maximum_amount = models.PositiveIntegerField(blank=True, default=0)

    ordered_price = models.FloatField(blank=True)
    ordered_amount = models.PositiveIntegerField(blank=True)
    delivered_price = models.FloatField(blank=True)
    delivered_amount = models.PositiveIntegerField(blank=True)
    
class GASMemberOrder(models.Model):
    """An Order made by a GAS Member in the context of a given GASSupplierOrder.

    See `here http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineGasista`__  for details (ITA only).

    """

    gasmember = models.ForeignKey(GASMember)
    gassupplierorder = models.ForeignKey(GASSupplierOrder)
    product = models.ForeignKey(GASSupplierOrderProduct)

    ordered_price = models.FloatField(blank=True)
    ordered_amount = models.PositiveIntegerField(blank=True)
    #TODO? delivered_price = models.FloatField(blank=True)
    delivered_amount = models.PositiveIntegerField(blank=True)
    
    @property
    def gas(self):
        return self.gasmember.gas

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

