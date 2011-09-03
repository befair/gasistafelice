"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from workflows.models import Workflow, Transition
from gasistafelice.base.workflows_utils import get_workflow, set_workflow, get_state, do_transition
from history.models import HistoricalRecords

from gasistafelice.base.models import PermissionResource, Place, DefaultTransition
from gasistafelice.base.fields import CurrencyField
from gasistafelice.lib import fields, ClassProperty
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.models.base import GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.managers import AppointmentManager, OrderManager
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.utils import register_parametric_role
from gasistafelice.auth import GAS_REFERRER_ORDER, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL

from datetime import datetime

class GASSupplierOrder(models.Model, PermissionResource):
    """An order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * status is a meaningful parameter... TODO
    * stock_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """
    
    pact = models.ForeignKey(GASSupplierSolidalPact)
    date_start = models.DateTimeField(default=datetime.now, help_text=_("when the order will be opened"))
    date_end = models.DateTimeField(help_text=_("when the order will be closed"), null=True, blank=True)
    # Where and when Delivery occurs
    delivery = models.ForeignKey('Delivery', related_name="order_set", null=True, blank=True)
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier  
    order_minimum_amount = CurrencyField(null=True, blank=True)
    # Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', related_name="order_set", null=True, blank=True)
    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    stock_set = models.ManyToManyField(GASSupplierStock, help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    objects = OrderManager()
    history = HistoricalRecords()

    display_fields = (
        models.CharField(max_length=32, name="current_state", verbose_name=_("Current state")),
        date_start, date_end, order_minimum_amount, delivery, withdrawal,
        
    )

    def __unicode__(self):
        if not self.date_end is None:
            return "Order gas %s to %s (close on %s)" % (self.gas, self.supplier, '{0:%Y%m%d}'.format(self.date_end))
        else:
            return "Order gas %s to %s (opened)" % (self.gas, self.supplier)

    class Meta:
        app_label = 'gas'
        
#-------------------------------------------------------------------------------#
# Model Archive API

    def is_active(self):
        """
        Return `True` if the GAS supplier order is to be considered as 'active'; `False` otherwise.
        """
        return self in GASSupplierOrder.objects.open()
    
    def is_archived(self):
        """
        Return `True` if the GAS supplier order is to be considered as 'archived'; `False` otherwise.
        """
        return not self.is_active()
    
#-------------------------------------------------------------------------------#    
# Authorization API

    @property
    def referrers(self):
        """
        Return all users being referrers for this order.
        """
        # retrieve 'order referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_ORDER, order=self)
        # retrieve all Users having this role
        return pr.get_users()       
    

#-------------------------------------------------------------------------------#

    def set_default_stock_set(self):
        '''
        A helper function associating a default set of products to a GASSupplierOrder.
        
        Useful if a supplier referrer isn't interested in "cherry pick" products one-by-one; 
        in this case, a reasonable choice is to add every Product bound to the Supplier the order will be issued to.
        '''
        stocks = GASSupplierStock.objects.filter(pact=self.pact, supplier_stock__supplier=self.pact.supplier)
        for s in stocks:
            GASSupplierOrderProduct.objects.create(order=self, stock=s)

    def setup_roles(self):
        # register a new `GAS_REFERRER_ORDER` Role for this GASSupplierOrder
        register_parametric_role(name=GAS_REFERRER_ORDER, order=self)
        
    # Workflow management

    @property
    def current_state(self):
        return get_state(self)

    @property
    def workflow(self):
        return get_workflow(self)

    @workflow.setter
    def workflow(self, value=None):
        raise AttributeError(_("Workflow for specific GASSupplierOrder is not allowed. Just provide a default order workflow for your GAS"))

    def forward(self, user):
        """Apply default transition"""
        state = get_state(self)
        transition = DefaultTransition.objects.get(workflow=self.workflow, state=state).transition
        do_transition(self, transition, user)
 
    # -- Resource API --#

    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "order"
    
    @property
    def parent(self):
        return self.pact

    @property
    def des(self):
        return self.gas.des

    @property
    def gas(self):
        """Return the GAS issuing this order."""
        return self.pact.gas
    
    @property
    def supplier(self):
        """Return the supplier this order is placed against."""
        return self.pact.supplier        
    
    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.supplier.pk)
    
    def save(self, *args, **kw):

        super(GASSupplierOrder, self).save(*args, **kw)

        if not self.workflow:
            # Set default workflow
            w = self.gas.config.default_workflow_gassupplier_order
            set_workflow(self, w)


    @property
    def report_name(self):
        # Clean file order name
        #TODO: clean supplier name 
        return u"GAS_%s_%s" % (self.supplier.supplier, '{0:%Y%m%d}'.format(self.delivery_date))
    

class GASSupplierOrderProduct(models.Model, PermissionResource):


    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    order = models.ForeignKey(GASSupplierOrder)
    gasstock = models.ForeignKey(GASSupplierStock)
    # how many units of Product a GAS Member can request during this GASSupplierOrder
    # useful for Products with a low availability
    maximum_amount = models.PositiveIntegerField(null=True, blank=True, default=0)
    # the price of the Product at the time the GASSupplierOrder was sent to the Supplier
    order_price = CurrencyField(null=True, blank=True)
    # the actual price of the Product (as resulting from the invoice)
    delivered_price = CurrencyField(null=True, blank=True)
    # how many items were actually delivered by the Supplier 
    delivered_amount = models.PositiveIntegerField(null=True, blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        app_label = 'gas'

    def __unicode__(self):
        return  unicode(self.stock)

    # how many items of this kind were ordered (globally by the GAS)
    @property
    def ordered_amount(self):
        # grab all GASMemberOrders related to this product and issued by members of the right GAS
        gmo_list = self.gasmember_order_set.values('ordered_amount')
        amount = 0 
        for gmo in gmo_list:         
            amount += gmo['ordered_amount']
        return amount 
    
    @property
    def tot_gasmembers(self):
        return self.gasmember_order_set.count()

    @property
    def tot_price(self):
        # grab all GASMemberOrders related to this product and issued by members of the right GAS
        gmo_list = self.gasmember_order_set.values('ordered_price')
        amount = 0 
        for gmo in gmo_list:         
            amount += gmo['ordered_price']
        return amount 
    
    @property
    def gas(self):
        return self.order.pact.gas    

    
class GASMemberOrder(models.Model, PermissionResource):

    """An order made by a GAS member in the context of a given GASSupplierOrder.

    See `here http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineGasista`__  for details (ITA only).

    """

    purchaser = models.ForeignKey(GASMember)
    ordered_product = models.ForeignKey(GASSupplierOrderProduct, related_name="gasmember_order_set")
    # price of the Product at order time
    ordered_price = CurrencyField(null=True, blank=True)
    # how many Product units were ordered by the GAS member
    ordered_amount = models.PositiveIntegerField(null=True, blank=True)
    # how many Product units were withdrawn by the GAS member 
    withdrawn_amount = models.PositiveIntegerField(null=True, blank=True)
    # gasmember order have to be confirmed if GAS configuration allowed it
    is_confirmed = models.BooleanField(default=False)

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('GAS member order')
        verbose_name_plural = _('GAS member orders')

    def __unicode__(self):
        return unicode(self.product)
    
    def confirm(self):
        self.is_confirmed = True

    @property
    def product(self):
        return self.ordered_product.stock.product

    # how much the GAS member actually payed for this Product (as resulting from the invoice)   
    @property
    def actual_price(self):
        return self.ordered_product.delivered_price
    
    # GASSupplierOrder this GASMemberOrder belongs to
    @property
    def order(self):
        return self.ordered_product.order 

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
 
    def save(self, *args, **ke):

        if not self.workflow:
            # Set default workflow
            w = self.gas.config.default_workflow_gasmember_order
            set_workflow(self, w)

        if self.purchaser.gas.config.gasmember_auto_confirm_order:
            self.is_confirmed = True

        return super(GASMemberOrder, self).save(*args, **kw)


class Appointment(models.Model):
    """
    A base, abstract model class meant to factor out fields common to appointment-like models
    (i.e.  meetings, events, ..)
    """
    
    objects = AppointmentManager()
    
    class Meta:
        abstract = True

#-------------------------------------------------------------------------------#
# Model Archive API
        
    def is_active(self):
        """
        Return `True` if the Appointment is to be considered as 'active'; `False` otherwise.
        """
        return self in Appointment.objects.future()
    
    def is_archived(self):
        """
        Return `True` if the Appointment is to be considered as 'archived'; `False` otherwise.
        """
        return not self.is_active()
    
#-------------------------------------------------------------------------------#    


class Delivery(Appointment, PermissionResource):

    """
    A delivery appointment, i.e. an event where one or more Suppliers deliver goods 
    associated with SupplierOrders issued by a given GAS (or Retina of GAS).  
    """
    
    place = models.ForeignKey(Place, related_name="delivery_set", help_text=_("where the order will be delivered by supplier"))
    date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"))    
    # GAS referrers for this Delivery appointment (if any) 
    referrers = models.ManyToManyField(GASMember, null=True, blank=True)
    
    # COSTO DI QUESTA CONSEGNA SPECIFICA?
    
    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')
        
    def __unicode__(self):
        return "%(date)s at %(place)s" % {'date':self.date, 'place':self.place}
    
    @property
    def gas_set(self):
        """
        Return a QuerySet containing all GAS sharing this delivery appointment. 
        """
        pass
    
#-------------------------------------------------------------------------------#   
# Authorization API

    @property
    def referrers_users(self):
        """
        Return all users being referrers for this delivery appointment.
        """
        # retrieve 'delivery referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_DELIVERY, delivery=self)
        # retrieve all Users having this role
        return pr.get_users()       
 
        
    def setup_roles(self):
        # register a new `GAS_REFERRER_DELIVERY` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_DELIVERY, delivery=self)      
    
#-------------------------------------------------------------------------------#
    

class Withdrawal(Appointment, PermissionResource):
    """
    A wihtdrawal appointment, i.e. an event where a GAS (or Retina of GAS) distribute 
    to their GASMembers goods they ordered issuing GASMemberOrders to the GAS/Retina.  
    """
    
    place = models.ForeignKey(Place, related_name="withdrawal_set", help_text=_("where the order will be withdrawn by GAS members"))
    date = models.DateTimeField(help_text=_("when the order will be withdrawn by GAS members"))
    # a Withdrawal appointment usually span a time interval
    start_time = models.TimeField(help_text=_("when the withdrawal will start"))
    end_time = models.TimeField(help_text=_("when the withdrawal will end"))
    # GAS referrers for this Withdrawal appointment  
    referrers = models.ManyToManyField(GASMember)
    
    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('wihtdrawal')
        verbose_name_plural = _('wihtdrawals')
    
    def __unicode__(self):
        return "%From (start_time)s to (end_time)s of (date)s at %(place)s" % {'start_time':self.start_time, 'end_time':self.end_time, 'date':self.date, 'place':self.place}
    
    @property
    def gas_set(self):
        """
        Return a QuerySet containing all GAS sharing this withdrawal appointment. 
        """
        pass

#-------------------------------------------------------------------------------#   
# Authorization API

    @property
    def referrers_users(self):
        """
        Return all users being referrers for this wihtdrawal appointment.
        """
        # retrieve 'wihtdrawal referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_WITHDRAWAL, wihtdrawal=self)
        # retrieve all Users having this role
        return pr.get_users()       


    def setup_roles(self):
        # register a new `GAS_REFERRER_WITHDRAWAL` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_WITHDRAWAL, withdrawal=self)  
         
#-------------------------------------------------------------------------------#
