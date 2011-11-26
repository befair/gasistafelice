"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from workflows.models import Workflow, Transition
from gasistafelice.base.workflows_utils import get_workflow, set_workflow, get_state, do_transition, get_allowed_transitions
from history.models import HistoricalRecords

from gasistafelice.base.models import PermissionResource, Place, DefaultTransition

from gasistafelice.lib.fields.models import CurrencyField, PrettyDecimalField
from gasistafelice.lib.fields import display
from gasistafelice.lib import ClassProperty
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.models.base import GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.managers import AppointmentManager, OrderManager
from gasistafelice.gas import signals
from gasistafelice.base.models import Person
from gasistafelice.consts import *
from flexi_auth.models import ParamRole
from flexi_auth.utils import register_parametric_role
from flexi_auth.exceptions import WrongPermissionCheck

from django.conf import settings

from workflows.utils import do_transition
from datetime import datetime, timedelta
import logging

log = logging.getLogger(__name__)

#from django.utils.encoding import force_unicode

class GASSupplierOrder(models.Model, PermissionResource):
    """An order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * status is a meaningful parameter... TODO
    * gasstock_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """
    
    pact = models.ForeignKey(GASSupplierSolidalPact, related_name="order_set",verbose_name=_('pact'))
    datetime_start = models.DateTimeField(verbose_name=_('Date start'), default=datetime.now, help_text=_("when the order will be opened"))
    datetime_end = models.DateTimeField(verbose_name=_('Date end'), help_text=_("when the order will be closed"), null=True, blank=True)
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier  
    order_minimum_amount = CurrencyField(verbose_name=_('Minimum amount'), null=True, blank=True)
    # Where and when Delivery occurs
    delivery = models.ForeignKey('Delivery', verbose_name=_('Delivery'), related_name="order_set", null=True, blank=True)
    # Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', verbose_name=_('Withdrawal'), related_name="order_set", null=True, blank=True)

    # Delivery cost. To be set after delivery has happened
    delivery_cost = CurrencyField(verbose_name=_('Delivery cost'), null=True, blank=True)

    # STATUS is MANAGED BY WORKFLOWS APP: 
    # status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("order state"))
    gasstock_set = models.ManyToManyField(GASSupplierStock, verbose_name=_('GAS supplier stock'), help_text=_("products available for the order"), blank=True, through='GASSupplierOrderProduct')

    group_id = models.PositiveIntegerField(verbose_name=_('Order group'), null=True, blank=True, 
        help_text=_("If not null this order is aggregate with orders from other GAS")
    )

    objects = OrderManager()

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('order issued to supplier')
        verbose_name = _('orders issued to supplier')
        ordering = ('datetime_end', 'datetime_start')
        app_label = 'gas'
        
    def __init__(self, *args, **kw):
        super(GASSupplierOrder, self).__init__(*args, **kw)
        self._msg = None

    def __unicode__(self):
        if self.datetime_end is not None:
            fmt_date = ('{0:%s}' % settings.DATE_FMT).format(self.datetime_end)
            if self.is_active():
                state = _("close on %(date)s") % { 'date' : fmt_date }
            else:
                state = _("closed on %(date)s") % { 'date' : fmt_date }
        else:
            state = _("open")

        rv = _("Order %(gas)s to %(supplier)s (%(state)s)") % {
                    'gas' : self.gas,
                    'supplier' : self.supplier,
                    'state' : state
        }
        if settings.DEBUG:
            rv += " [%s]" % self.pk
        return rv

    def do_transition(self, transition, user):
        super(GASSupplierOrder, self).do_transition(transition, user)
        signals.order_state_update.send(sender=self, transition=transition)

    def open_if_needed(self):
        """Check datetime_start and open order if needed."""

        if self.datetime_start <= datetime.datetime.now():

            # Act as superuser
            user = User.objects.get(username=settings.INIT_OPTIONS['su_username'])
            t_name = "open"
            t = Transition.objects.get(name__iexact=t_name, workflow=self.workflow)

            if t in get_allowed_transitions(self, user):
                log.debug("Do %s transition. datetime_start is %s" % (t, self.datetime_start))
                self.do_transition(t, user)

    def get_valid_name(self):
        from django.template.defaultfilters import slugify
        from django.utils.encoding import smart_str
        n = str(self.pk) + '_'
        n += smart_str(slugify(self.pact.supplier.name).replace('-', '_'))
        n += '_{0:%Y%m%d}'.format(self.delivery.date)
        return n
        return self.pact.supplier.name.replace('-', '_').replace(' ', '_')

    #-- Contacts --#

    @property
    def contacts(self):
        return Contact.objects.filter(person__in=self.info_people)

    @property
    def info_people(self):
        return self.pact.info_people

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
            return self.delivery.referrers_people
        return Person.objects.none()

    @property
    def withdrawal_referrer_persons(self):
        if self.withdrawal:
            return self.withdrawal.referrers_people
        return Person.objects.none()

    def set_default_gasstock_set(self):
        '''
        A helper function associating a default set of products to a GASSupplierOrder.
        
        Useful if a supplier referrer isn't interested in "cherry pick" products one-by-one; 
        in this c ase, a reasonable choice is to add every Product bound to the Supplier the order will be issued to.
        '''

        if not self.pact.gas.config.auto_populate_products:
            self._msg = []
            self._msg.append(ugettext("GAS is not configured to auto populate all products. You have to select every product you want to put into the order"))
            return

        stocks = GASSupplierStock.objects.filter(pact=self.pact, stock__supplier=self.pact.supplier, enabled =True)
        for s in stocks:
            if s.enabled:
                GASSupplierOrderProduct.objects.create(order=self, gasstock=s, initial_price=s.price, order_price=s.price, delivered_price=s.price)

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
        gsop, created = GASSupplierOrderProduct.objects.get_or_create(order=self, gasstock=s, initial_price=s.price)
        if created:
            self._msg.append('No product found in order(%s) state(%s)' % (self.pk, self.current_state))
            gsop.order_price = s.price
            gsop.save()
        else:
            self._msg.append('Product already present in order(%s) state(%s)' % (self.pk, self.current_state))
            if gsop.delivered_price != s.price:
                gsop.delivered_price = s.price
                gsop.save()

    def remove_product(self, s):
        '''
        A helper function to remove a product from a GASSupplierOrder.
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
                self._msg.append(ugettext('Deleting gas member %(member)s email %(email)s: Unit price(%(price)s) ordered quantity(%(quantity)s) total price(%(price)s) for product %(product)s') % (gmo.purchaser, gmo.purchaser.email, gmo.ordered_price, gmo.ordered_amount, gmo.ordered_price, gmo.product, ))
                signals.gmo_product_erased.send(sender=self)
                gmo.delete()
            self._msg.append('Deleted gas members orders (%s) for total of %s euro' % (count, total))
            gsop.delete()


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
    #ERROR: An unexpected error occurred while tokenizing input
    #The following traceback may be corrupted or invalid
    #The error message is: ('EOF in multi-line statement', (390, 0))

    @property
    def ordered_products(self):
        return GASMemberOrder.objects.filter(ordered_product__in=self.orderable_products)

    @property
    def stocks(self):
        from gasistafelice.supplier.models import SupplierStock
        stocks_pk=map(lambda x: x[0], self.gasstock_set.values('stock'))
        return SupplierStock.objects.filter(pk__in=stocks_pk)

    @property
    def gasstocks(self):
        return self.gasstock_set.all()

    @property
    def gas(self):
        return self.pact.gas

    @property
    def gasmembers(self):
        return self.gas.gasmembers

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(pk=self.pk)

    @property
    def order(self):
        return self

    @property
    def tot_price(self):
        tot = 0
        for gmo in self.ordered_products:
            tot += gmo.tot_price
        return tot

    def save(self, *args, **kw):
        created = False

        if not self.pk:
            created = True
            if self.gas.config.use_withdrawal_place:

                # Create default withdrawal
                if self.datetime_end and not self.withdrawal:

                    #TODO: check gasconfig for weekday
                    w = Withdrawal(
                            date=self.datetime_end + timedelta(7), 
                            place=self.gas.config.withdrawal_place
                    )
                    w.save()
                    self.withdrawal = w

        super(GASSupplierOrder, self).save(*args, **kw)

        if created:
            self.set_default_gasstock_set()
        
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        """Who can create a supplier order?

        In general:
            * GAS administrators
            * Referrers for the pact the order is placed against
        In depth we have to switch among multiple possible contexts

        If we are checking for a "unusual key" (not in ctx_keys_to_check),
        just return False, do not raise an exception.
        """

        allowed_users = User.objects.none()
        ctx_keys_to_check = set(('pact', 'gas', 'site', 'supplier'))
        ctx_keys = context.keys()

        if len(ctx_keys) > 1:
            raise WrongPermissionCheck('CREATE [only one key supported for context]', cls, context)

        k = ctx_keys[0]

        if k not in ctx_keys_to_check:
            # No user is allowed, just return False
            # (user is not in User empty querySet)
            # Do not raise an exception
            pass

        # Switch among possible different contexts

        elif k == 'pact':
            # pact context
            pact = context[k]
            allowed_users = pact.gas.tech_referrers | pact.gas.supplier_referrers

        elif k == 'gas':
            # gas context
            gas = context[k]
            if gas.pacts.count():
                allowed_users = gas.tech_referrers | gas.supplier_referrers

        elif k == 'site':
            # des context
            des = context[k]
            if des.pacts.count():
                allowed_users = des.gas_tech_referrers | des.gas_supplier_referrers

        elif k == 'supplier':
            # supplier context
            # Every GAS REFERRER SUPPLIER or GAS REFERRER TECH of a GAS 
            # who has a GASSupplierSolidalPact with this Supplier
            supplier = context[k]
            for pact in supplier.pacts:
                allowed_users |= pact.gas.supplier_referrers | pact.gas.tech_referrers

        return user in allowed_users
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.referrers | self.gas.tech_referrers | self.gas.supplier_referrers
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can edit details of a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators  
        allowed_users = self.referrers | self.gas.tech_referrers | self.pact.gas_supplier_referrers
        return user in allowed_users 
    
    #-----------------------------------------------#

    display_fields = (
        display.Resource(name="gas", verbose_name=_("GAS")),
        display.Resource(name="supplier", verbose_name=_("Supplier")),
        models.CharField(max_length=32, name="current_state", verbose_name=_("Current state")),
        datetime_start, datetime_end, order_minimum_amount, 
        delivery, display.ResourceList(name="delivery_referrer_persons", verbose_name=_("Delivery referrer")),
        withdrawal, display.ResourceList(name="withdrawal_referrer_persons", verbose_name=_("Withdrawal referrer")),
    )

#-------------------------------------------------------------------------------
class GASSupplierOrderProduct(models.Model, PermissionResource):
    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    order = models.ForeignKey(GASSupplierOrder, related_name="orderable_product_set",verbose_name=_('order'))
    gasstock = models.ForeignKey(GASSupplierStock, related_name="orderable_product_set",verbose_name=_('gas stock'))
    # how many units of Product a GAS Member can request during this GASSupplierOrder
    # useful for Products with a low availability
    maximum_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('maximum amount'),
                        max_digits=8, decimal_places=2
    )
    # the price of the Product at the time the GASSupplierOrder was created
    initial_price = CurrencyField(verbose_name=_('initial price'))
    # the price of the Product at the time the GASSupplierOrder was sent to the Supplier
    order_price = CurrencyField(verbose_name=_('order price'))
    # the actual price of the Product (as resulting from the invoice)
    delivered_price = CurrencyField(null=True, blank=True,verbose_name=_('delivered price'))
    # how many items were actually delivered by the Supplier 
    delivered_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('delivered amount'),
                        max_digits=8, decimal_places=2
    )

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('gas supplier order product')
        verbose_name_plural = _('gas supplier order products')
        app_label = 'gas'

    def __unicode__(self):
        rv = _('%(gasstock)s of order %(order)s') % { 'gasstock' : self.gasstock, 'order' : self.order}
        if settings.DEBUG:
            rv += " [%s]" % self.pk
        return rv

    @property
    def has_changed(self):
        return self.initial_price != self.order_price

    # how many items of this kind were ordered (globally by the GAS)
    @property
    def tot_amount(self):
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
    def unconfirmed_orders(self):
        return self.gasmember_order_set.filter(is_confirmed=False).count()

    @property
    def tot_price(self):
        """Grab all GASMemberOrders related to this orderable product"""

        #INFO: i.e. if you want to optimize this method you could write:
        #INFO: self.gasmember_order_set.values('ordered_price', 'ordered_amount')
        #INFO: and compute tot_price in here.
        
        gmo_list = self.gasmember_order_set.all()
        tot = 0 
        for gmo in gmo_list:
            tot += gmo.tot_price
        return tot 

    @property
    def pact(self):
        return self.order.pact

    @property
    def gas(self):
        return self.order.pact.gas

    @property
    def supplier(self):
        return self.order.supplier

    @property
    def product(self):
        return self.gasstock.product

    @property
    def stock(self):
        return self.gasstock.stock
    
    def save(self, *args, **kw):
        """Sef default initial price"""
        if not self.pk:
            self.initial_price = self.order_price
        if self.delivered_price is None:
            self.delivered_price = self.order_price
        super(GASSupplierOrderProduct, self).save(*args, **kw)

        # CASCADING set until GASMemberOrder
        if self.has_changed_price:
            self._msg = []
            self._msg.append('Price has changed for gsop (%s) [ %s--> %s]' %  (self.pk, self.order_price))
            for gmo in self.gasmember_order_set:
                #gmo.order_price = self.order_price
                gmo.note = _("Price changed on %(date)s") % { 'date' : datetime.now() }
                gmo.save()


    @property
    def has_changed_price(self):
        try:
            gsop = GASSupplierOrderProduct.objects.get(pk=self.pk)
            if not gsop is None:
                return bool(self.order_price != gsop.order_price)
            else:
                return False
        except GASSupplierOrderProduct.DoesNotExist:
            return False

    #-------------- Authorization API ---------------#

    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new product to a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators        
        try:
            order = context['order']
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.gas_supplier_referrers
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of product associated with a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators        
        allowed_users = self.order.referrers | self.gas.tech_referrers | self.pact.gas_supplier_referrers                    
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a product associated with a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators    
        allowed_users = self.order.referrers | self.gas.tech_referrers | self.pact.gas_supplier_referrers        
        return user in allowed_users 


class GASMemberOrder(models.Model, PermissionResource):

    """An order made by a GAS member in the context of a given GASSupplierOrder.

    See `here http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineGasista`__  for details (ITA only).

    """

    purchaser = models.ForeignKey(GASMember, related_name="gasmember_order_set", null=False, blank=False,verbose_name=_('purchaser'))
    ordered_product = models.ForeignKey(GASSupplierOrderProduct, related_name="gasmember_order_set", null=False, blank=False,verbose_name=_('order product'))
    # price of the Product at order time
    ordered_price = CurrencyField(verbose_name=_('ordered price'))
    # how many Product units were ordered by the GAS member
    ordered_amount = PrettyDecimalField(null=False, blank=False, verbose_name = _('order amount'),
                        max_digits=6, decimal_places=2
    )
    # how many Product units were withdrawn by the GAS member 
    withdrawn_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('widthdrawn amount'),
                        max_digits=6, decimal_places=2
    )
    # gasmember order have to be confirmed if GAS configuration allowed it
    is_confirmed = models.BooleanField(default=False,verbose_name=_('confirmed'))

    note = models.CharField(max_length=64, verbose_name=_('product note'), null=True, blank=True, help_text=_("GAS member can write some short message about this product for the producer"))

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('GAS member order')
        verbose_name_plural = _('GAS member orders')
        unique_together = (('ordered_product', 'purchaser'),)

    def __unicode__(self):
        return u"Ordered product %(product)s by GAS member %(gm)s" % { 'product' : self.product, 'gm': self.gasmember }
    
    def confirm(self):
        self.is_confirmed = True

    @property
    def has_changed(self):
        return self.ordered_product.order_price != self.ordered_price

    @property
    def tot_price(self):
        """Ordered price per ordered amount for this ordered product"""
        #FIXME: we have to use self.ordered_price instead of self.ordered_product.order_price?
        return self.ordered_product.order_price * self.ordered_amount

    @property
    def gasmember(self):
        return self.purchaser

    @property
    def product(self):
        return self.ordered_product.product

    @property
    def supplier(self):
        return self.ordered_product.supplier

    @property
    def email(self):
        return self.purchaser.email

    @property
    def order(self):
        """GASSupplierOrder this GASMemberOrder belongs to."""

        return self.ordered_product.order

    @property
    def gas(self):
        """Which GAS this order belongs"""
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
 
    def save(self, *args, **kw):

        # Delete a GAS Member order if amount == 0
        if not self.ordered_amount:
            return self.delete()

        #Duplicate Entry. Retrieve data from database
        if not self.pk:
            YetExist = GASMemberOrder.objects.filter(ordered_product=self.ordered_product, purchaser=self.purchaser)
            if YetExist and YetExist.count() > 0:
                self.pk = YetExist[0].pk

        if not self.workflow:
            # Set default workflow
            w = self.gas.config.default_workflow_gasmember_order
            set_workflow(self, w)

        #If the GAS's member do not have to confirm is order auto set the flag
        if not self.purchaser.gas.config.gasmember_auto_confirm_order:
            self.is_confirmed = True

        return super(GASMemberOrder, self).save(*args, **kw)
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can issue an order *to* a GAS ?
        # *  members of that GAS
        try:
            order = context['order']
            allowed_users = order.gas.members
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can modify an order placed by a GAS member ?
        # * the member itself (of course)
        # * order referrers (if any)
        # * referrers for the pact the order is placed against 
        # * GAS administrators                
        allowed_users = self.purchaser | self.order.referrers | self.gas.tech_referrers | self.pact.gas_supplier_referrers                    
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an order placed by a GAS member ?
        # * the member itself (of course)
        # * order referrers (if any)
        # * referrers for the pact the order is placed against 
        # * GAS administrators                
        allowed_users = self.purchaser | self.order.referrers | self.gas.tech_referrers | self.pact.gas_supplier_referrers                    
        return user in allowed_users
    
    #---------------------------------------------------#
     

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
    
    place = models.ForeignKey(Place, related_name="delivery_set", help_text=_("where the order will be delivered by supplier"),verbose_name=_('place'))
    date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"),verbose_name=_('date'))    

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')
        
    def __unicode__(self):
        return "%(date)s at %(place)s" % {'date':self.date, 'place':self.place}
    
    @property
    def gas_list(self):
        """
        Return a QuerySet containing all GAS sharing this delivery appointment. 
        """
        pacts = GASSupplierSolidalPact.objects.filter(order_set__in=self.order_set.all())
        return GAS.objects.filter(pact_set__in = pacts)
    
    #-------------------------------------------------------------------------------#   
    # Referrers API
        
    @property
    def referrers(self):
        """
        Return all users being referrers for this delivery appointment.
        """
        # retrieve 'delivery referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_DELIVERY, delivery=self)
        # retrieve all Users having this role
        return pr.get_users()       
 
    @property
    def persons(self):
        return self.referrers_people

    #-------------------------------------------------------------------------------#   
    # Authorization API
        
    def setup_roles(self):
        # register a new `GAS_REFERRER_DELIVERY` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_DELIVERY, delivery=self)      
    
#-------------------------------------------------------------------------------#

    #-------------- Authorization API ---------------#
    
    # COMMENT-fero: now we do not use authoriazion API on this model.
    # we have to make some consideration for deliveries shared on more than one order
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # TODO: REVIEW NEEDED see below (Withdrawal.can_create)
        # Who can schedule a new delivery appointment for a GAS ?
        # * pact referrers (all)
        # * order referrers (all, if any)
        # * GAS administrators       

        # TODO: order referres: ticket www.jagom.org/trac/reesgas/ticket/185
        # add.. "evryone is referrer for one active order in GAS

        allowed_users = User.objects.none()
        try:
            # gas context
            gas = context['gas']
            allowed_users = gas.supplier_referrers | gas.tech_referrers
        except KeyError:
            try:
                # TODO: ticket www.jagom.org/trac/reesgas/ticket/185
                # order context
                order = context['order']
                raise NotImplementedError("can_create withdrawal in order")
                allowed_users = order.referrers | order.gas.supplier_referrers | order.gas.tech_referrers
            except KeyError:
                raise WrongPermissionCheck('CREATE', cls, context)   

        return user in allowed_users
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can modify a delivery appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any) 
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators            
        # 3) ELSE:
        #     * DES administrators

        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()  
        if len(associated_orders) == 1:
            order = associated_orders[0] 
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.gas_supplier_referrers                    
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers
            
        return user in allowed_users
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can delete a delivery appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any) 
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators            
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()  
        if len(associated_orders) == 1:
            order = associated_orders[0] 
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.gas_supplier_referrers                    
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers
            
        return user in allowed_users
    
        
    #---------------------------------------------------#
     
    

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
    def gas_list(self):
        """
        Return a QuerySet containing all GAS sharing this withdrawal appointment. 

        """
        pacts = GASSupplierSolidalPact.objects.filter(order_set__in=self.order_set.all())
        return GAS.objects.filter(pact_set__in = pacts)

    #-------------------------------------------------------------------------------#   
    # Referrers API
        
    @property
    def referrers(self):
        """
        Return all users being referrers for this wihtdrawal appointment.
        """
        # retrieve 'wihtdrawal referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self)
        # retrieve all Users having this role
        return pr.get_users()       

    @property
    def persons(self):
        return self.referrers_people

    #-------------------------------------------------------------------------------#   
    # Authorization API

    def setup_roles(self):
        # register a new `GAS_REFERRER_WITHDRAWAL` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_WITHDRAWAL, withdrawal=self)  
         
#-------------------------------------------------------------------------------#


    #-------------- Authorization API ---------------#

    # COMMENT-fero: now we do not use authoriazion API on this model.
    # we have to make some consideration for withdrawals shared on more than one order
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can schedule a new withdrawal appointment for a GAS ?
        # * pact referrers (all)
        # * GAS administrators       

        # TODO: order referres: ticket www.jagom.org/trac/reesgas/ticket/185
        # add.. "evryone is referrer for one active order in GAS

        allowed_users = User.objects.none()
        try:
            # gas context
            gas = context['gas']
            allowed_users = gas.supplier_referrers | gas.tech_referrers
        except KeyError:
            try:
                # TODO: ticket www.jagom.org/trac/reesgas/ticket/185
                # order context
                order = context['order']
                raise NotImplementedError("can_create withdrawal in order")
                allowed_users = order.referrers | order.gas.supplier_referrers | order.gas.tech_referrers
            except KeyError:
                raise WrongPermissionCheck('CREATE', cls, context)   

        return user in allowed_users
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can modify a withdrawal appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any) 
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators            
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()  
        if len(associated_orders) == 1:
            order = associated_orders[0] 
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.gas_supplier_referrers                    
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers
            
        return user in allowed_users
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can delete a withdrawal appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any) 
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators            
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()  
        if len(associated_orders) == 1:
            order = associated_orders[0] 
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.gas_supplier_referrers                    
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers
            
        return user in allowed_users
            
    #---------------------------------------------------#
