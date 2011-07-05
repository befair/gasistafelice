from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError

from permissions.models import Role
from workflows.models import Workflow
from history.models import HistoricalRecords

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import PermissionResource, Person, Place
from gasistafelice.base.const import DAY_CHOICES

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.gas.managers import GASMembersManager
from gasistafelice.bank.models import Account

from gasistafelice.des.models import DES


from decimal import Decimal


class GAS(models.Model, PermissionResource):

    """A group of people which make some purchases together.

    Every GAS member has a Role where the basic Role is just to be a member of the GAS.
    """

    name = models.CharField(max_length=128)
    id_in_des = models.CharField(_("GAS code"), max_length=8, null=False, blank=False, unique=True, help_text=_("GAS unique identifier in the DES. Example: CAMERINO--> CAM"))    
    logo = models.ImageField(upload_to="/images/", null=True, blank=True)
    headquarter = models.ForeignKey(Place, related_name="gas_headquarter_set", help_text=_("main address"), null=True, blank=True)
    description = models.TextField(blank=True, help_text=_("Who are you? What are yours specialties?"))
    membership_fee = CurrencyField(default=Decimal("0"), help_text=_("Membership fee for partecipating in this GAS"), blank=True)

    suppliers = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True, help_text=_("Suppliers bound to the GAS through a solidal pact"))

    #, editable=False: admin validation refers to field 'account_state' that is missing from the form
    account = models.ForeignKey(Account, null=True, blank=True, related_name="gas_set", help_text=_("GAS manage all bank account for GASMember and PDS."))
    #TODO: change name
    liquidity = models.ForeignKey(Account, null=True, blank=True, related_name="gas_set2", help_text=_("GAS have is own bank account. "))

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

    des = models.ForeignKey(DES)

    #COMMENT fero: photogallery and attachments does not go here
    #they should be managed elsewhere in Wordpress (now, at least)

    #-- Managers --#

    history = HistoricalRecords()

    #-- Meta --#
    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'

    #-- Overriding built-in methods --#
    def __unicode__(self):
        return self.name

    #-- Properties --#
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv  

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
        self.id_in_des = self.id_in_des.upper()

        if not self.pk:

            self.config = GASConfig()
            self.account = Account.objects.create(balance=0)
            self.liquidity = Account.objects.create(balance=0)

        # This should never happen, but is it reasonable
        # that an installation has only one DES
        if not self.des:
            if DES.objects.count() > 1:
                raise AttributeError(_("You have to bind GAS %s to a DES") % self.name)
            else:
                self.des = DES.objects.all()[0]

        super(GAS, self).save(*args, **kw)

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

    
    use_single_delivery = models.BooleanField(default=True, 
        help_text=_("GAS uses only one delivery place")
    )

    # Do not set default to both places because we want to have the ability
    # to follow headquarter value if it changes.
    # Provide delivery place and withdrawal place properties to get the right value
    default_withdrawal_place = models.ForeignKey(Place, blank=True, null=True, related_name='gas_default_withdrawal_set', help_text=_("to specify if different from headquarter"))
    default_delivery_place = models.ForeignKey(Place, blank=True, null=True, related_name='gas_default_delivery_set', help_text=_("to specify if different from delivery place"))

    auto_select_all_products = models.BooleanField(default=True, help_text=_("automatic selection of all products bound to a supplier when a relation with the GAS is activated"))
    is_active = models.BooleanField(default=True)
    use_scheduler = models.BooleanField(default=True)  

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
        pass
        #TODO placeholder domthu code that default_delivery_place must not be None
        # if headquarter is not specified
        pass
        
        return super(GASConfig, self).clean()

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

    objects = GASMembersManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        unique_together = (('gas', 'id_in_gas'), )

    def __unicode__(self):
        return _('%(person)s in GAS "%(gas)s"') % {'person' : self.person, 'gas': self.gas}
    
    # Resource API
    def des(self):
        # A GAS member belongs to the DES its GAS belongs to.
        return self.gas.des
    
    # Resource API
    def pacts(self):
        # A GAS member is interested primarily in those pacts (`SupplierSolidalPact` instances) subscribed by its GAS
        return self.gas.pacts
    
    # Resource API
    def suppliers(self):
        # A GAS member is interested primarily in those suppliers dealing with its GAS
        return self.gas.suppliers
    
    # Resource API
    def orders(self):
        # A GAS member is interested primarily in those suppliers orders to which he/she can submit orders
        return self.gas.orders
    
    # Resource API
    def deliveries(self):
        # A GAS member is interested primarily in delivery appointments scheduled for its GAS
        return self.gas.deliveries
    
    # Resource API
    def withdrawals(self):
        # A GAS member is interested primarily in withdrawal appointments scheduled for its GAS
        return self.gas.withdrawals
    
    # Resource API
    def products(self):
        # A GAS member is interested primarily in those products he/she can order
        return self.gas.products
    

    
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

    #COMMENT domthu: fero added id_in_retina for GASMember. That it not required: ask to community if necesary.
    @property
    def id_in_retina(self):
        #TODO: Should we provide also and id for retina?
        #TODO: is it dependent by person or by membership?
        #TODO: should we provide a "retina" parameter and make this a function
        """Some algorhythm to return unique GAS member "card number" in Retina"""
        raise NotImplementedError

    def setup_roles(self):
        # automatically add a new GASMember to the `GAS_MEMBER` Role
        user = self.person.user
        #COMMENT: issue #2 In my local database i've seen that roles are empty: needed fixtures?
        role = register_parametric_role(name=GAS_MEMBER, gas=self.gas)
        role.add_principal(user)
    
    @property        
    def local_grants(self):
        rv = (
            # GAS tech referrers have full access to members of their own GAS 
            ('ALL', ParamRole.objects.filter(role=GAS_REFERRER_TECH, param1=self.gas)),
            # GAS members can see list and details of their fellow members
            ('LIST', ParamRole.objects.filter(role=GAS_MEMBER, param1=self.gas)),
            ('VIEW', ParamRole.objects.filter(role=GAS_MEMBER, param1=self.gas)),
              )     
        return rv  
    
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

class GASSupplierStock(models.Model, PermissionResource):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    pact = models.ForeignKey("GASSupplierSolidalPact")
    supplier_stock = models.ForeignKey(SupplierStock)
    # if a Product is available to GAS Members; policy is GAS-specific
    enabled = models.BooleanField()    
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
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
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
    Relation between GAS1 and Supplier1

    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_signed = models.DateField(blank=True, null=True, default=None)

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

    account = models.ForeignKey(Account, null=True, blank=True)

    history = HistoricalRecords()
    
    class Meta:
        app_label = 'gas'
     
    def __unicode__(self):
        return _("Relation between %(gas)s and %(supplier)s") % \
                      { 'gas' : self.gas, 'supplier' : self.supplier}

    @property
    def gas_supplier_referrers(self):
        """Retrieve all GASMember who are GAS supplier referrers associated with this solidal pact"""

        # TODO UNITTEST: write unit tests for this method
        parametric_role = ParamRole.get_role(GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)
        referrers = self.gas.gas_member_set.have_role(parametric_role)
        return referrers

    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this GAS/Supplier pair
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return "" 

    def save(self, *args, **kw):

        created = False
        if not self.pk:
            created = True
      
        super(GASSupplierSolidalPact, self).save(*args, **kw)

        if created and self.gas.config.auto_select_all_products:
            for p in self.supplier.supplierstock_set.all():
                p.gassupplierstock_set.add(gas=self.gas)

        
        
