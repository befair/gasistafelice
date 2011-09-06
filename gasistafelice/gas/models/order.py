"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from workflows.models import Workflow, Transition
from workflows.utils import get_workflow, set_workflow, get_state, do_transition
from history.models import HistoricalRecords

from gasistafelice.base.models import PermissionResource, Place, DefaultTransition
from gasistafelice.base.fields import CurrencyField
from gasistafelice.lib import ClassProperty
from gasistafelice.lib.fields import display
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.models.base import GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.managers import AppointmentManager, OrderManager
from gasistafelice.base.models import Person
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.utils import register_parametric_role
from gasistafelice.auth import GAS_REFERRER_ORDER, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL

from django.conf import settings

from datetime import datetime, timedelta

#from django.utils.encoding import force_unicode

class GASSupplierOrder(models.Model, PermissionResource):
    """An order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * status is a meaningful parameter... TODO
    * gasstock_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """
    
    pact = models.ForeignKey(GASSupplierSolidalPact, related_name="order_set")
    date_start = models.DateTimeField(verbose_name=_('Date start'), default=datetime.now, help_text=_("when the order will be opened"))
    date_end = models.DateTimeField(verbose_name=_('Date end'), help_text=_("when the order will be closed"), null=True, blank=True)
    # Where and when Delivery occurs
    delivery = models.ForeignKey('Delivery', verbose_name=_('Delivery'), related_name="order_set", null=True, blank=True)
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier  
    order_minimum_amount = CurrencyField(verbose_name=_('Minimum amount'), null=True, blank=True)
    # Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', verbose_name=_('Withdrawal'), related_name="order_set", null=True, blank=True)
    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    gasstock_set = models.ManyToManyField(GASSupplierStock, verbose_name=_('GAS supplier stock'), help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    #TODO: Notify system

    objects = OrderManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        
    def __unicode__(self):
        if self.date_end is not None:
            fmt_date = ('{0:%s}' % settings.DATE_FMT).format(self.date_end)
            if self.is_active():
                state = _("close on %(date)s") % { 'date' : fmt_date }
            else:
                state = _("closed on %(date)s") % { 'date' : fmt_date }
        else:
            state = _("open")

        return _("Order %(gas)s to %(supplier)s (%(state)s)") % {
                    'gas' : self.gas,
                    'supplier' : self.supplier,
                    'state' : state
        }

    def __init__(self, *args, **kw):
        super(GASSupplierOrder, self).__init__(*args, **kw)
        self._msg = None

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

    @property
    def delivery_referrer_persons(self):
        if self.delivery:
            return Person.objects.filter(user__in=self.delivery.referrers_users)
        return Person.objects.none()

    @property
    def withdrawal_referrer_persons(self):
        if self.withdrawal:
            return Person.objects.filter(user__in=self.withdrawal.referrers_users)
        return Person.objects.none()

    def set_default_stock_set(self):
        '''
        A helper function associating a default set of products to a GASSupplierOrder.
        
        Useful if a supplier referrer isn't interested in "cherry pick" products one-by-one; 
        in this c ase, a reasonable choice is to add every Product bound to the Supplier the order will be issued to.
        '''

        if not self.pact.gas.config.auto_populate_products:
            self._msg.append('Configuration of auto generation of the product\'s order is not abilitated. To automatism the procedure set auto_populate_products to True')
            return

        stocks = GASSupplierStock.objects.filter(pact=self.pact, stock__supplier=self.pact.supplier)
        for s in stocks:
            if s.enabled:
                GASSupplierOrderProduct.objects.create(order=self, gasstock=s)

    @property
    def message(self):
        """getter property for internal message from model."""
        return self._msg

    def add_product(self, s):
        '''
        A helper function to add product to a GASSupplierOrder.
        '''
        self._msg = []

        # We can retrieve GASSupplierOrderProduct bound to this order with
        # self.orderable_products but it is useful to use get_or_create
        gsop, create = GASSupplierOrderProduct.objects.get_or_create(order=self, gasstock=s)
        if created:
            self._msg.append('No product found in order(%s) state(%s)' % (self.pk, self.current_state))
        else:
            self._msg.append('Product already present in order(%s) state(%s)' % (self.pk, self.current_state))

    def remove_product(self, s):
        '''
        A helper function to add product to a GASSupplierOrder.
        '''
        #TODO: Does workflows.utils have method state_in(tupple of state)
        #if (order.current_state == OPEN) | (order.current_state == CLOSED) 
        self._msg = []

        try:
            gsop = self.orderable_products.get(gasstock=s)
        except GASSupplierOrderProduct.DoesNotExist:
            self._msg.append('No product found in order(%s) state(%s)' % (self.pk, self.current_state))

        else:
            self._msg.append('product found in order(%s) state(%s)' % (self.pk, self.current_state))
            #Delete all GASMemberOrders done
            lst = gsop.gasmember_order_set.all()
            total = 0
            count = lst.count()
            for gmo in lst:
                total += gmo.ordered_price
                self._msg.append('Deleting gas member %s(%s) email %s ordered quantity(%s) total price(%s) for product %s' % (gmo.purchaser, gmo.purchaser.pk, gmo.purchaser.email, gmo.ordered_amount, gmo.ordered_price, gmo.product, ))
                gmo.delete()
            self._msg.append('Deleted gas members orders(%s) for total of %s' % (count, total))
            GASSupplierOrderProduct.objects.delete(gsop)


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
    
    @property
    def orderable_products(self):
        return self.orderable_product_set.all()

    @property
    def ordered_products(self):
        return GASMemberOrder.objects.filter(ordered_product__in=self.orderable_products)

    @property
    def stocks(self):
        from supplier.models import SupplierStock
        stocks_pk=map(lambda x: x[0], self.gasstock_set.values('stock'))
        return SupplierStock.objects.filter(pk__in=stocks_pk)

    @property
    def gasstocks(self):
        return self.gasstock_set.all()

    @property
    def total_ordered(self):
        tot = 0
        for gmo in self.ordered_products:
            tot += gmo.ordered_price
        return tot

    def save(self, *args, **kw):
        created = False
        if not self.pk:
            created = True
            # Create default withdrawal
            if self.date_end and not self.withdrawal:
                #TODO: check gasconfig for weekday
                w = Withdrawal(
                        date=self.date_end + timedelta(7), 
                        place=self.gas.config.withdrawal_place
                )
                w.save()
                self.withdrawal = w

        super(GASSupplierOrder, self).save(*args, **kw)

        if not self.workflow:
            # Set default workflow
            w = self.gas.config.default_workflow_gassupplier_order
            set_workflow(self, w)

        if created:
            self.set_default_stock_set()

    display_fields = (
        models.CharField(max_length=32, name="current_state", verbose_name=_("Current state")),
        date_start, date_end, order_minimum_amount, 
        delivery, display.ResourceList(name="delivery_referrer_persons", verbose_name=_("Delivery referrer")),
        withdrawal, display.ResourceList(name="withdrawal_referrer_persons", verbose_name=_("Withdrawal referrer")),
    )

#-------------------------------------------------------------------------------

class GASSupplierOrderProduct(models.Model, PermissionResource):


    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    order = models.ForeignKey(GASSupplierOrder, related_name="orderable_product_set")
    gasstock = models.ForeignKey(GASSupplierStock, related_name="orderable_product_set")
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
        return unicode(self.gasstock)
        #return force_unicode(self.stock)

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

    @property
    def supplier(self):
        return self.order.supplier

    @property
    def product(self):
        return self.gasstock.product

    
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

    @property
    def email(self):
        return self.purchaser.email

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
    #TODO FIXME AFTER 6th of september: 
    # * date should be Date field
    # * start_time and end_time (with no defaults) must be managed in forms
    date = models.DateTimeField(help_text=_("when the order will be withdrawn by GAS members"))
    # a Withdrawal appointment usually span a time interval
    start_time = models.TimeField(default="18:00", help_text=_("when the withdrawal will start"))
    end_time = models.TimeField(default="22:00", help_text=_("when the withdrawal will end"))
    # GAS referrers for this Withdrawal appointment  
    referrers = models.ManyToManyField(GASMember)
    
    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('wihtdrawal')
        verbose_name_plural = _('wihtdrawals')
    
    def __unicode__(self):
        return "At %(place)s on %(date)s from %(start_time)s to %(end_time)s" % {
                    'start_time':self.start_time.strftime("%H:%M"), 
                    'end_time':self.end_time.strftime("%H:%M"), 
                    'date':self.date.strftime("%d-%m-%Y"), 
                    'place':self.place
        }
    
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
        pr = ParamRole.get_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self)
        # retrieve all Users having this role
        return pr.get_users()       


    def setup_roles(self):
        # register a new `GAS_REFERRER_WITHDRAWAL` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_WITHDRAWAL, withdrawal=self)  
         
#-------------------------------------------------------------------------------#
