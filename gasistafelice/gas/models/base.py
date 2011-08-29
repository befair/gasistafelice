from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError

from permissions.models import Role
from workflows.models import Workflow
from workflows.utils import get_workflow
from history.models import HistoricalRecords

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import PermissionResource, Person, Place
from gasistafelice.base.const import DAY_CHOICES

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, GAS_REFERRER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.gas.managers import GASMemberManager
from gasistafelice.bank.models import Account

from gasistafelice.des.models import DES

from gasistafelice.lib import fields, ClassProperty

from decimal import Decimal


class GAS(models.Model, PermissionResource):

    """A group of people which make some purchases together.

    Every GAS member has a Role where the basic Role is just to be a member of the GAS.
    """
    name = models.CharField(max_length=128, unique=True)
    id_in_des = models.CharField(_("GAS code"), max_length=8, null=False, blank=False, unique=True, help_text=_("GAS unique identifier in the DES. Example: CAMERINO--> CAM"))
    logo = models.ImageField(upload_to="/images/", null=True, blank=True)
    headquarter = models.ForeignKey(Place, related_name="gas_headquarter_set", help_text=_("main address"), null=True, blank=True)
    description = models.TextField(blank=True, help_text=_("Who are you? What are yours specialties?"))
    membership_fee = CurrencyField(default=Decimal("0"), help_text=_("Membership fee for partecipating in this GAS"), blank=True)

    supplier_set = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True, help_text=_("Suppliers bound to the GAS through a solidal pact"))

    #, editable=False: admin validation refers to field 'account_state' that is missing from the form
    account = models.ForeignKey(Account, null=True, blank=True, related_name="bank_acc_set", help_text=_("GAS manage all bank account for GASMember and PDS."))
    #TODO: change name
    liquidity = models.ForeignKey(Account, null=True, blank=True, related_name="bank_liq_set", help_text=_("GAS have is own bank account. "))

    #active = models.BooleanField()
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text=_("Born"))
    vat = models.CharField(max_length=11, blank=True, help_text=_("VAT number"))
    fcc = models.CharField(max_length=16, blank=True, help_text=_("Fiscal code card"))

    email_gas = models.EmailField(null=True, blank=True)

    #COMMENT fero: imho email_referrer should be a property
    #that retrieve email contact from GAS_REFERRER (role just added). GAS REFERRER usually is GAS President
    #COMMENT domthu: The president 
    email_referrer = models.EmailField(null=True, blank=True, help_text=_("Email president"))
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(verify_exists=True, null=True, blank=True) 

    association_act = models.FileField(upload_to='gas/docs', null=True, blank=True)
    intent_act = models.FileField(upload_to='gas/docs', null=True, blank=True)

    note = models.TextField(blank=True)

    # Resource API
    des = models.ForeignKey(DES)

    #COMMENT fero: photogallery and attachments does not go here
    #they should be managed elsewhere in Wordpress (now, at least)

    #-- Managers --#

    history = HistoricalRecords()

    display_fields = (
        website, 
        models.CharField(max_length=32, name="city", verbose_name=_("City")),
        headquarter, birthday, description, 
        membership_fee, vat, fcc,
		#fields.ResourceList(verbose_name=_("referrers"), name="referrers"),
        association_act,
    )

    #-- Meta --#
    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'

    #-- Overriding built-in methods --#
    def __unicode__(self):
        return self.name
     
    @property
    def allnotes(self):
        return []

    @property
    def ancestors(self):
        return [self.des]

    #-- Properties --#
    @property
    def local_grants(self):
        rv = (
              # permission specs go here
              )
        return rv

    #-- Permission management --#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, **kwargs):
        ## only DES administrators can create a new GAS in a DES
        try:
            des = kwargs['des']
        except KeyError:
            raise SyntaxError("You need to specify a 'des' argument to perform this permission check.")
        return user in des.admins
    
    # Row-level VIEW permission
    def can_view(self, user, **kwargs):
        # only GAS members and DES administrators can view GAS details 
        return (user in self.members) or (user in self.des.admins) 
    
    # Row-level EDIT permission
    def can_edit(self, user, **kwargs):
        # only GAS tech referrers and DES administrators can edit GAS details
        return (user in self.tech_referrers) or (user in self.des.admins) 
    
    # Row-level DELETE permission
    def can_delete(self, user, **kwargs):
        # only DES administrators can delete a GAS in a DES
        return user in self.des.admins
    
    #-- Properties --#

    @property
    def referrers(self):
        """
        Return all users being referrers for this GAS.
        """
        # retrieve 'GAS referrer' parametric role for this GAS
        pr = ParamRole.get_role(GAS_REFERRER, gas=self)
        # retrieve all Users having this role
        return pr.get_users()       
        

    @property
    def members(self):
        """
        Return all users being members of this GAS.
        """
        # retrieve 'GAS member' parametric role for this GAS
        pr = ParamRole.get_role(GAS_MEMBER, gas=self)
        # retrieve all Users having this role
        return pr.get_users()       
    
    @property
    def tech_referrers(self):
        """
        Return all users being technical referrers for this GAS.
        """
        # retrieve 'tech referrer' parametric role for this GAS
        pr = ParamRole.get_role(GAS_REFERRER_TECH, gas=self)
        # retrieve all Users having this role
        return pr.get_users()       

    @property
    def cash_referrers(self):
        """
        Return all users being accounting referrers for this GAS.
        """
        # retrieve 'cash referrer' parametric role for this GAS
        pr = ParamRole.get_role(GAS_REFERRER_CASH, gas=self)
        # retrieve all Users having this role
        return pr.get_users()  
    
    
    @property
    def city(self):
        return self.headquarter.city 

    @property
    def economic_state(self):
        return u"%s - %s" % (self.account, self.liquidity)

    #-- Methods --#

    def setup_roles(self):
        # register a new `GAS_MEMBER` Role for this GAS
        register_parametric_role(name=GAS_MEMBER, gas=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_TECH, gas=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_CASH, gas=self)
        rv = (
              # initial roles setup goes here
              )
        return rv

    def save(self, *args, **kw):

        if not self.id_in_des:
            self.id_in_des = self.name[:3]
            while True:
                try:
                    GAS.objects.get(id_in_des=self.id_in_des)
                    self.id_in_des = self.id_in_des[:2] + chr(ord(self.id_in_des[2]) + 1)
                except: #DoesNotExist or MultipleObjectsReturned
                    break
                    
        self.id_in_des = self.id_in_des.upper()

        created = False
        if not self.pk:
            created = True

        # This should never happen, but is it reasonable
        # that an installation has only one DES
        try:
            self.des
        except DES.DoesNotExist:
            if DES.objects.count() > 1:
                raise AttributeError(_("You have to bind GAS %s to a DES") % self.name)
            else:
                self.des = DES.objects.all()[0]

        super(GAS, self).save(*args, **kw)

        if created:

            self.config = GASConfig.objects.create(gas=self)
            #TODO self.account = Account.objects.create()
            #TODO self.liquidity = Account.objects.create()

    #-- Resource API --#

    @property
    def gas(self):
        return self

    @property
    def orders(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        """Return orders bound to resource"""
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def order(self):
        raise NoSenseException("calling gas.order is a no-sense. GAS is related to more than one order")

    @property
    def deliveries(self):
        from gasistafelice.gas.models.order import Delivery
        # The GAS deliveries appointments take from orders. Do distinct operation. 
        rv = Delivery.objects.none()
        for obj in self.orders:
            if obj.delivery: 
                rv |= obj.delivery
        return rv

    @property
    def delivery(self):
        raise NoSenseException("calling gas.delivery is a no-sense. GAS is related to more than one delivery")

    @property
    def withdrawals(self):
        from gasistafelice.gas.models.order import Withdrawal
        # The GAS withdrawal appointments. Do distinct operation.
        rv = Withdrawal.objects.none()
        for obj in self.orders:
            if obj.withdrawal: 
                rv |= obj.withdrawal
        return rv

    @property
    def withdrawal(self):
        raise NoSenseException("calling gas.withdrawal is a no-sense. GAS is related to more than one withdrawal")

    @property
    def pacts(self):
        # Return pacts bound to a GAS
        return self.pact_set.all()

    @property
    def suppliers(self):
        """Return suppliers bound to a GAS"""
        return self.supplier_set.all()

    @property
    def accounts(self):
        #return (Account.objects.filter(pk=self.account.pk) | Account.objects.filter(pk=self.liquidity.pk)).order_by('balance')
        raise NotImplementedError

    @property
    def gasmembers(self):
        return self.gasmember_set.all()

    @property
    def persons(self):
        return Person.objects.filter(gasmember__in=self.gasmembers)

    @property
    def stocks(self):
        return SupplierStock.objects.filter(supplier__in=self.suppliers)

    @property
    def products(self):
        #TODO OPTIMIZE
        return Product.objects.filter(pk__in=[obj.product.pk for obj in self.stocks])

    @property
    def categories(self):
        #TODO All disctinct categories for all suppliers with solidal pact with the gas
        #distinct(pk__in=[obj.category.pk for obj in self.Products])
        return ProductCategory.objects.all()

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.filter(gas=self)

    @property
    def orderable_products(self):
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open())

    @property
    def ordered_products(self):
        return GASMemberOrder.objects.filter(order__in=self.orders)

    @property
    def basket(self):
        return GASMemberOrder.objects.filter(order__in=self.orders.open())


class GASConfig(models.Model, PermissionResource):
    """
    Encapsulate here gas settings and configuration facilities
    """

    # Link to parent class
    gas = models.OneToOneField(GAS, related_name="config")

    default_workflow_gasmember_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gasmember_order_set", null=True, blank=True
    )
    default_workflow_gassupplier_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gassupplier_order_set", null=True, blank=True
    )

    can_change_price = models.BooleanField(default=False,
        help_text=_("GAS can change supplier products price (i.e. to hold some funds for the GAS itself)")
    )

    show_order_by_supplier = models.BooleanField(default=True, 
        help_text=_("GAS views open orders by supplier. If disabled, views open order by delivery appointment")
    )

    #TODO: see ticket #65
    default_close_day = models.CharField(max_length=16, blank=True, choices=DAY_CHOICES, 
        help_text=_("default closing order day of the week")
    )
    #TODO: see ticket #65
    default_delivery_day = models.CharField(max_length=16, blank=True, choices=DAY_CHOICES, 
        help_text=_("default delivery day of the week")
    )

    #Do not provide default for time fields because it has no sense set it to the moment of GAS configuration
    #TODO placeholder domthu: Default time to be set to 00:00
    default_close_time = models.TimeField(blank=True, null=True,
        help_text=_("default order closing hour and minutes")
    )
  
    default_delivery_time = models.TimeField(blank=True, null=True,
        help_text=_("default delivery closing hour and minutes")
    )

    can_change_withdrawal_place_on_each_order = models.BooleanField(default=False, 
        help_text=_("If False, GAS uses only one withdrawal place that is the default or if not set it is the GAS headquarter")
    )

    can_change_delivery_place_on_each_order = models.BooleanField(default=False, 
        help_text=_("If False, GAS uses only one delivery place that is the default or if not set it is the GAS headquarter")
    )

    # Do not set default to both places because we want to have the ability
    # to follow headquarter value if it changes.
    # Provide delivery place and withdrawal place properties to get the right value
    default_withdrawal_place = models.ForeignKey(Place, blank=True, null=True, related_name="gas_default_withdrawal_set", help_text=_("to specify if different from headquarter"))
    default_delivery_place = models.ForeignKey(Place, blank=True, null=True, related_name="gas_default_delivery_set", help_text=_("to specify if different from delivery place"))

    auto_select_all_products = models.BooleanField(default=True, help_text=_("automatic selection of all products bound to a supplier when a relation with the GAS is activated"))
    is_active = models.BooleanField(default=True)
    use_scheduler = models.BooleanField(default=False)
    gasmember_auto_confirm_order = models.BooleanField(default=True, help_text=_("if True gasmember's orders are automatically confirmed. If False each  gasmember must confirm by himself his own orders"))

    history = HistoricalRecords()

    #-- Meta --#
    class Meta:
        verbose_name = _('GAS options')
        verbose_name_plural = _('GAS options')
        app_label = 'gas'

    def __unicode__(self):
        return _('Configuration for GAS "%s"') % self.gas 

    @property
    def delivery_place(self):
        return self.default_delivery_place or self.gas.headquarter

    @property
    def withdrawal_place(self):
        return self.default_withdrawal_place or self.gas.headquarter

    def clean(self):
        #TODO placeholder domthu code that default_withdrawal_place must not be None
        # if headquarter is not specified
        if self.default_delivery_place is None:
            self.default_delivery_place =  self.gas.headquarter;
        #pass
        #TODO placeholder domthu code that default_delivery_place must not be None
        # if headquarter is not specified
        if self.default_withdrawal_place is None:
            self.default_withdrawal_place = self.gas.headquarter;
        #pass
        
        return super(GASConfig, self).clean()

    def save(self):
        self.default_workflow_gassupplier_order = Workflow.objects.get(name="SupplierOrderDefault")
        self.default_workflow_gasmember_order = Workflow.objects.get(name="GASMemberOrderDefault")
        return super(GASConfig, self).save()

class GASMember(models.Model, PermissionResource):
    """A bind of a Person into a GAS.
    Each GAS member specifies which Roles he is available for.
    This way, every time there is a need to assign one or more GAS Members to a given Role,
    there is already a group of people to choose from. 
    
    """
    # Resource API
    person = models.ForeignKey(Person)
    # Resource API
    gas = models.ForeignKey(GAS)
    id_in_gas = models.CharField(_("Card number"), max_length=10, blank=True, null=True, help_text=_("GAS card number"))
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_member_available_set")
    account = models.ForeignKey(Account, null=True, blank=True)
    membership_fee_payed = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text=_("When was the last the annual quote payment"))

    objects = GASMemberManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        unique_together = (('gas', 'id_in_gas'), )

    def __unicode__(self):
        return _('%(person)s in GAS "%(gas)s"') % {'person' : self.person, 'gas': self.gas}
   

    def _get_roles(self):
        """
        Return a QuerySet containing all the parametric roles which have been assigned
        to the User associated with this GAS member.
        
        Only roles which make sense for the GAS the GAS member belongs to are returned 
        (excluding roles the User may have been assigned with respect to other GAS).
        """
        # Roles MUST BE a property because roles are bound to a User 
        # with `add_principal()` and not directly to a GAS member
        # costruct the result set by joining partial QuerySets
        roles = []
        # get all parametric roles assigned to the User associated with this GAS member;
        # note that "spurious" roles can be included, since a User can be a member of more
        # than one GAS, while here we're interested only in roles bound to the GAS this 
        # GAS member belongs to
        qs = ParamRole.objects.filter(principal_param_role_set__user = self.person.user)
        # add  `GAS_REFERRER`, `GAS_REFERRER_CASH`, `GAS_REFERRER_TECH`, `GAS_REFERRER_SUPPLIER` and `GAS_MEMBER` roles
        roles += [pr for pr in qs if pr.gas == self.gas]
        # add  `GAS_REFERRER_ORDER` roles
        roles += [pr for pr in qs if pr.order.pact.gas == self.gas]
        # add  `GAS_REFERRER_DELIVERY` roles
        roles += [pr for pr in qs if self.gas in pr.delivery.gas_set]
        # add  `GAS_REFERRER_WITHDRAWAL` roles
        roles += [pr for pr in qs if self.gas in pr.withdrawal.gas_set]
        # HACK: convert a list of model instances to a QuerySet by filtering on instance's primary keys
        qs = ParamRole.objects.filter(pk__in=[obj.pk for obj in roles]) 
        return qs 

    def _set_roles(self, list):
        raise NotImplementedError
        
    roles = property(_get_roles, _set_roles)
        
    @property
    def verbose_name(self):
        """Return GASMember representation along with his own card number in GAS"""
        #See ticket #54
        return _("%(id_in_gas)s - %(gas_member)s") % {'gas_member' : self, 'id_in_gas': self.id_in_gas}

    @property
    def ancestors(self):
        return [self.des, self.gas]

    #COMMENT domthu: fero added id_in_des (or id_in_gas ) for GASMember. That it not required: ask to community if necesary.
    @property
    def id_in_des(self):
        """TODO: Return unique GAS member "card number" in the DES.
        This must be referred to a Person, not to a GAS membership.
        Think about its use cases.."""
        # TODO:
        # return self.person.id_in_des
        # or
        # return something
        raise NotImplementedError

    def setup_roles(self):
        # automatically add a new GASMember to the `GAS_MEMBER` Role
        user = self.person.user
        #COMMENT: issue #3 TypeError: The principal must be either a User instance or a Group instance.
        if user is None:
            return ""
        #TODO: fixtures create user foreach person
        role = register_parametric_role(name=GAS_MEMBER, gas=self.gas)
        role.add_principal(user)

    def clean(self):
        # Clean method is for validation. Validation errors are meant to be
        # catched in forms
        if not self.person.user: # GAS members must have an account on the system
            raise ValidationError(_("GAS Members must be registered users"))
        return super(GASMember, self).clean()

    def save(self, *args, **kw):
        # Save method is meant to do some trickery at saving time
        # and to do some low-level checks raising low-level exceptions.
        # These exceptions do not need to be translated.
        if not self.person.user: # GAS members must have an account on the system
            raise AttributeError('GAS Members must be registered users')
        if not self.id_in_gas:
            self.id_in_gas = None
        super(GASMember, self).save(*args, **kw)

    #-- Resource API --#

    @property
    def des(self):
        # A GAS member belongs to the DES its GAS belongs to.
        return self.gas.des

    @property
    def pacts(self):
        # A GAS member is interested primarily in those pacts (`SupplierSolidalPact` instances) subscribed by its GAS
        return self.gas.pacts

    @property
    def suppliers(self):
        # A GAS member is interested primarily in those suppliers dealing with its GAS
        return self.gas.suppliers

    @property
    def orders(self):
        # A GAS member is interested primarily in those suppliers orders to which he/she can submit orders
        # WARNING: get GAS proxy instance!
        g = GAS.objects.get(pk=self.gas.pk)
        return g.orders

    @property
    def deliveries(self):
        # A GAS member is interested primarily in delivery appointments scheduled for its GAS
        return self.gas.deliveries

    @property
    def withdrawals(self):
        # A GAS member is interested primarily in withdrawal appointments scheduled for its GAS
        return self.gas.withdrawals

    @property
    def products(self):
        # A GAS member is interested primarily to show products
        return self.gas.products

    @property
    def stocks(self):
        # A GAS member is interested primarily to show products and price
        return self.gas.stocks

    @property
    def gasstocks(self):
        # A GAS member is interested primarily in those products and price per GAS
        return self.gas.gasstocks

    @property
    def basket(self):
        return GASMemberOrder.objects.filter(product__order__in=self.orders.open())

class GASSupplierStock(models.Model, PermissionResource):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    pact = models.ForeignKey("GASSupplierSolidalPact")
    supplier_stock = models.ForeignKey(SupplierStock)
    # if a Product is available to GAS Members; policy is GAS-specific
    enabled = models.BooleanField(default=True)
    ## constraints on what a single GAS Member is able to order
    # minimun amount of Product units a GAS Member is able to order
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum;
    # useful when a Product ships in packages containing multiple units.
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    
    history = HistoricalRecords()

    def __unicode__(self):
        return unicode(self.supplier_stock)
        
    @property
    def supplier(self):
        return self.supplier_stock.supplier

    @property
    def price(self):
        # Product base price as updated by agreements contained in GASSupplierSolidalPact
        price_percent_update = self.pact.order_price_percent_update or 0
        return self.supplier_stock.price*(1 + price_percent_update)

    class Meta:
        app_label = 'gas'
        verbose_name = _("GAS supplier stock")
        verbose_name_plural = _("GAS supplier stocks")


class GASSupplierSolidalPact(models.Model, PermissionResource):
    """Define a GAS <-> Supplier relationship agreement.

    Each Supplier comes into relationship with a GAS by signing a pact,
    where are factorized behaviour agreements between these two entities.
    This pact acts as a configurator for order and delivery management with respect to the given Supplier.

    >>> from gasistafelice.gas.models.base import GAS, GASSupplierSolidalPact
    >>> from gasistafelice.supplier.models import Supplier
    >>> g1 = GAS(name='GAS1')
    >>> g1.save()
    >>> s1 = Supplier(name='Supplier1')
    >>> s1.save()

    >>> pds = GASSupplierSolidalPact()
    >>> pds.gas = g1
    >>> pds.supplier = s1
    >>> pds.save()
    >>> print pds
    Pact between GAS1 and Supplier1

    >>> from gasistafelice.gas.models.base import *
    >>> from gasistafelice.gas.models.order import *
    >>> from gasistafelice.supplier.models import *
    >>> p = GASSupplierSolidalPact(gas=GAS.objects.get(id=1), supplier=Supplier.objects.get(id=1))
    >>> p.save()
    >>> st = SupplierStock.objects.filter(supplier__id=3).count()
    >>> gst = GASSupplierStock.objects.filter(pact__id=p.pk).count()
    >>> st==gst
    True
    >>> p.account_id>0
    True

    """

    gas = models.ForeignKey(GAS, related_name="pact_set")
    supplier = models.ForeignKey(Supplier, related_name="pact_set")
    date_signed = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None, help_text=_("date of first meeting GAS-Producer"))

    # which Products GAS members can order from Supplier
    # COMMENT fero: I think the solution proposed by domthu in ticket #80 respect
    # the semantic of the through parameter for a ManyToManyField relation:
    # GASSupplierStock is just a way to augment relation between a pact and a supplier stock
    supplier_stock = models.ManyToManyField(SupplierStock, through=GASSupplierStock, null=True, blank=True)
    order_minimum_amount = CurrencyField(null=True, blank=True)
    order_delivery_cost = CurrencyField(null=True, blank=True)
    #time needed for the delivery since the GAS issued the order disposition
    order_deliver_interval = models.TimeField(null=True, blank=True)
    # how much (in percentage) base prices from the Supplier are modified for the GAS
    order_price_percent_update = models.FloatField(null=True, blank=True)
    
    #domthu: if GAS's configuration use only one 
    #TODO: see ticket #65
    default_withdrawal_day = models.CharField(max_length=16, choices=DAY_CHOICES, blank=True,
        help_text=_("Withdrawal week day agreement")
    )
    default_withdrawal_time = models.TimeField(null= True, blank=True, \
        help_text=_("withdrawal time agreement")
    )

    default_withdrawal_place = models.ForeignKey(Place, related_name="pact_default_withdrawal_place_set", null=True, blank=True)

    #document = models.FileField(upload_to="/pacts/", null=True, blank=True)

    history = HistoricalRecords()

    display_fields = ()

    class Meta:
        app_label = 'gas'
        unique_together = (('gas', 'supplier'),)

    def __unicode__(self):
        return _("Pact between %(gas)s and %(supplier)s") % \
                      { 'gas' : self.gas, 'supplier' : self.supplier}
    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "pact"

    @property
    def gas_supplier_referrers(self):
        """
        Return all users being referrers for this solidal pact (GAS-to-Supplier interface).
        """
        # retrieve 'GAS supplier referrer' parametric role for this pact
        pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=self)
        # retrieve all Users having this role
        return pr.get_users()    

    
    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this solidal pact
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, pact=self)     
    
    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return "" 

    def save(self, *args, **kw):

        created = False
        if not self.pk:
            created = True

        super(GASSupplierSolidalPact, self).save(*args, **kw)

        #if created and self.account is None:
        #    self.account = Account.objects.create()

        if created and self.gas.config.auto_select_all_products:
            for st in self.supplier.stocks:
                GASSupplierStock.objects.create(pact=self, supplier_stock=st, enabled=True)

    @property
    def ancestors(self):
        return [self.des, self.gas]

    @property
    def des(self):
        return self.gas.des

#-------------------------------------------------------------------------------
