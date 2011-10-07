from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.conf import settings

from permissions.models import Role
from workflows.models import Workflow
from workflows.utils import get_workflow
from history.models import HistoricalRecords

from gasistafelice.lib import ClassProperty
from gasistafelice.lib.fields.models import CurrencyField

from gasistafelice.base.models import PermissionResource, Person, Place
from gasistafelice.base.const import DAY_CHOICES

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, GAS_REFERRER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, SupplierStock, Product, ProductCategory
from gasistafelice.gas.managers import GASMemberManager
from gasistafelice.bank.models import Account
from gasistafelice.des.models import DES

from gasistafelice.lib.fields import display
from gasistafelice.lib import ClassProperty

from gasistafelice.exceptions import NoSenseException

from decimal import Decimal


class GAS(models.Model, PermissionResource):

    """A group of people who makes some purchases together.

    Every GAS member has a Role where the basic Role is just to be a member of the GAS.
    """
    name = models.CharField(max_length=128, unique=True)
    id_in_des = models.CharField(_("GAS code"), max_length=8, null=False, blank=False, unique=True, help_text=_("GAS unique identifier in the DES. Example: CAMERINO--> CAM"))
    logo = models.ImageField(upload_to="/images/", null=True, blank=True)
    headquarter = models.ForeignKey(Place, related_name="gas_headquarter_set", help_text=_("main address"), null=False, blank=False)
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

    #Persons include relative associated resources to GAS class
    #FIXME: Cannot run SyncDB
    #gas.gas: 'activist_set' specifies an m2m relation through model GASActivist, which has not been installed
    #activist_set = models.ManyToManyField(Person, verbose_name=_('GAS activits'), null=True, blank=True, through="GASActivist")

    association_act = models.FileField(upload_to='gas/docs', null=True, blank=True)
    intent_act = models.FileField(upload_to='gas/docs', null=True, blank=True)

    note = models.TextField(blank=True)

    # Resource API
    des = models.ForeignKey(DES)

    #TODO: Notify system

    #COMMENT fero: photogallery and attachments does not go here
    #they should be managed elsewhere in Wordpress (now, at least)

    #-- Managers --#

    history = HistoricalRecords()

    display_fields = (
        website, 
        models.CharField(max_length=32, name="city", verbose_name=_("City")),
        headquarter, birthday, description, 
        membership_fee, vat, fcc,
        display.ResourceList(verbose_name=_("referrers"), name="referrers"),
        association_act,
    )

    #-- Meta --#
    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'

    #-- Overriding built-in methods --#
    def __unicode__(self):
        return self.name

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
    
    # Row-level EDIT permission
    def can_edit(self, user, **kwargs):
        # only GAS tech referrers and DES administrators can edit GAS details
        return (user in self.tech_referrers) or (user in self.des.admins) 
    
    # Row-level DELETE permission
    def can_delete(self, user, **kwargs):
        # only DES administrators can delete a GAS in a DES
        return user in self.des.admins
    
    #-- Properties --#

    #-- Referrers API --#

    @property
    def referrers(self):
        """Returns GAS referrers which are TECH referrers."""
        return self.tech_referrers

        #TODO: we can add person with GAS_REFERRER role, but doesn't mind now
        #pr = ParamRole.get_role(GAS_REFERRER, gas=self)
        #return pr.get_users() | self.tech_referrers

    @property
    def info_people(self):
        return Person.objects.filter(gasactivist_set__in=self.activist_set.all())

    @property
    def persons(self):
        return Person.objects.filter(gasmember__in=self.gasmembers) | self.info_people | self.referrers_people

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
    def supplier_referrers(self):
        """
        Return all users being supplier referrers for this GAS
        """
        # retrieve 'GAS supplier referrer' parametric role for this pact
        pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, gas=self)
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
        # register a new `GAS_REFERRER` Role for this GAS. This is the President of the GAS or other VIP.
        register_parametric_role(name=GAS_REFERRER, gas=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_TECH, gas=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_CASH, gas=self)

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
    def parent(self):
        return self.des

    @property
    def gas(self):
        return self

    @property
    def gasmembers(self):
        """All GASMember for this GAS"""
        return self.gasmember_set.all()

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
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open())

    @property
    def ordered_products(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(order__in=self.orders)

    @property
    def basket(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(order__in=self.orders.open())

    def clean(self):

        if self.headquarter is None:
            raise ValidationError(_("Default headquarter place must be set"))

        return super(GAS, self).clean()

#-----------------------------------------------------------------------------------------------------

def get_supplier_order_default():
    return Workflow.objects.get(name="SupplierOrderDefault")

def get_gasmember_order_default():
    return Workflow.objects.get(name="GASMemberOrderDefault")

class GASConfig(models.Model, PermissionResource):
    """
    Encapsulate here gas settings and configuration facilities
    """

    # Link to parent class
    gas = models.OneToOneField(GAS, related_name="config")

    default_workflow_gasmember_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gmow_gasconfig_set", blank=True, default=get_gasmember_order_default
    )
    default_workflow_gassupplier_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gsopw_gasconfig_set", blank=True, default=get_supplier_order_default
    )

    can_change_price = models.BooleanField(default=False,
        help_text=_("GAS can change supplier products price (i.e. to hold some funds for the GAS itself)")
    )

#    show_order_by_supplier = models.BooleanField(default=True, 
#        help_text=_("GAS views open orders by supplier. If disabled, views open order by delivery appointment")
#    )

    order_show_only_next_delivery = models.BooleanField(verbose_name=_('Show only next delivery'), default=False, 
        help_text=_("GASMember can choose to filter order block among one or more orders that share the next withdrawal appointment"))
    order_show_only_one_at_a_time = models.BooleanField(verbose_name=_('Show only one order at a time'), default=False, 
        help_text=_("GASMember can select only one open order at a time in order block"))

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
    default_close_time = models.TimeField(verbose_name=_('Default close time'), blank=True, null=True,
        help_text=_("default order closing hour and minutes")
    )
  
    default_delivery_time = models.TimeField(verbose_name=_('Default delivery day time'), blank=True, null=True,
        help_text=_("default delivery closing hour and minutes")
    )

    can_change_withdrawal_place_on_each_order = models.BooleanField(verbose_name=_('Can change withdrawal place on each order'), default=False, 
        help_text=_("If False, GAS uses only one withdrawal place that is the default or if not set it is the GAS headquarter")
    )

    can_change_delivery_place_on_each_order = models.BooleanField(verbose_name=_('Can change delivery place on each order'), default=False, 
        help_text=_("If False, GAS uses only one delivery place that is the default or if not set it is the GAS headquarter")
    )

    # Do not set default to both places because we want to have the ability
    # to follow headquarter value if it changes.
    # Provide delivery place and withdrawal place properties to get the right value
    default_withdrawal_place = models.ForeignKey(Place, verbose_name=_('Default withdrawal place'), blank=True, null=True, related_name="gas_default_withdrawal_set", help_text=_("to specify if different from headquarter"))
    default_delivery_place = models.ForeignKey(Place, verbose_name=_('Default delivery place'), blank=True, null=True, related_name="gas_default_delivery_set", help_text=_("to specify if different from delivery place"))

    auto_populate_products = models.BooleanField(verbose_name=_('Auto populate products'), default=True, help_text=_("automatic selection of all products bound to a supplier when a relation with the GAS is activated"))
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True, help_text=_("This GAS doesn't exist anymore or is banned? (from who?)"))
    use_scheduler = models.BooleanField(default=False)
    gasmember_auto_confirm_order = models.BooleanField(verbose_name=_('GAS members orders are auto confirmed'), default=True, help_text=_("if checked, gasmember's orders are automatically confirmed. If not, each gasmember must confirm by himself his own orders"))

    #TODO:is_suspended = models.BooleanField(default=False, help_text=_("The GAS is not available (hollidays, closed). The motor use this flag to operate or not some automatisms"))
    #TODO:notify_days = models.PositiveIntegerField(null=True, default=0, help_text=_("The number of days that the system will notify an event (product changed). If set to 0 the notify system is off."))

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

#----------------------------------------------------------------------------------------------------

class GASActivist(models.Model, PermissionResource):
    """Relation between a `GAS` and a `Person`.

    If you need information on the GAS, ask to this person.
    This is not necessarily a user in the system. You can consider it just as a contact.
    """

    gas = models.ForeignKey(GAS)
    person = models.ForeignKey(Person)
    info_title = models.CharField(max_length=256, blank=True)
    info_description = models.TextField(blank=True)

    #history = HistoricalRecords()

    @property
    def parent(self):
        return self.gas

#----------------------------------------------------------------------------------------------------

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
    membership_fee_payed = models.DateField(auto_now=False, verbose_name=_("membership_fee_payed"), auto_now_add=False, null=True, blank=True, help_text=_("When was the last the annual quote payment"))
    #TODO: Notify system

    objects = GASMemberManager()

    history = HistoricalRecords()

    display_fields = (
        membership_fee_payed,
        id_in_gas,
        models.CharField(max_length=32, name="city", verbose_name=_("City")),
        models.CharField(max_length=32, name="economic_state", verbose_name=_("Account")),
    )

    class Meta:
        app_label = 'gas'
        unique_together = (('gas', 'id_in_gas'), )

    def __unicode__(self):
        rv = _('%(person)s in GAS "%(gas)s"') % {'person' : self.person, 'gas': self.gas}
        if settings.DEBUG:
            rv += " [%s]" % self.pk
        return rv
   

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
    def parent(self):
        return self.gas

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

    @property
    def city(self):
        return self.person.city

    @property
    def email(self):
        return self.person.email

    @property
    def economic_state(self):
        st1 = self.total_basket
        st2 = self.total_basket_to_be_delivered
        if isinstance(self.account, Account):
            return u"%s - (%s + %s) = %s"  % (self.account, st1, st2, (self.account.balance - (st1 + st2)))
        else:
            return u"(%s + %s)"  % (st1, st2)

    @property
    def total_basket(self):
        tot = 0
        for gmord in self.basket:
            tot += gmord.tot_price
        return tot

    @property
    def total_basket_to_be_delivered(self):
        tot = 0
        for gmord in self.basket_to_be_delivered:
            tot += gmord.tot_price
        return tot

    def setup_roles(self):
        # Automatically add the new GASMember to the `GAS_MEMBER` Role for its GAS
        role = ParamRole.get_role(GAS_MEMBER, gas=self.gas)
        user = self.person.user
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
        # A GAS member is interested primarily in those pacts (`GASSupplierSolidalPact` instances) subscribed by its GAS
        return self.gas.pacts

    @property
    def suppliers(self):
        # A GAS member is interested primarily in those suppliers dealing with its GAS
        return self.gas.suppliers

    @property
    def orders(self):
        # A GAS member is interested primarily in those suppliers orders to which he/she can submit orders
        return self.gas.orders

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
    def gasmember(self):
        return self

    @property
    def basket(self):
        from gasistafelice.gas.models import GASMemberOrder
        #TODO FIXME AFTER 6: there should be no enry with ordered_amount = 0 in GASMemberOrder table
        return self.gasmember_order_set.filter(ordered_product__order__in=self.orders.open(), ordered_amount__gt=0)
        return self.gasmember_order_set.filter(ordered_product__order__in=self.orders.open(), ordered_amount__gt=0)

    @property
    def basket_to_be_delivered(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(ordered_product__in=self.orders.closed())

    @property
    def orderable_products(self):
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open())

#-----------------------------------------------------------------------------------------------------

class GASSupplierStock(models.Model, PermissionResource):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    pact = models.ForeignKey("GASSupplierSolidalPact", related_name="gasstock_set")
    stock = models.ForeignKey(SupplierStock, related_name="gasstock_set")
    # if a Product is available to GAS Members; policy is GAS-specific
    enabled = models.BooleanField(default=True)
    ## constraints on what a single GAS Member is able to order
    # minimun amount of Product units a GAS Member is able to order
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum;
    # useful when a Product ships in packages containing multiple units.
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    #TODO: Notify system

    history = HistoricalRecords()

    def __unicode__(self):
        return '%s' % (self.stock)

    def __init__(self, *args, **kw):
        super(GASSupplierStock, self).__init__(*args, **kw)
        self._msg = None

    @property
    def supplier(self):
        return self.stock.supplier

    @property
    def product(self):
        return self.stock.product

    @property
    def price(self):
        # Product base price as updated by agreements contained in GASSupplierSolidalPact
        price_percent_update = self.pact.order_price_percent_update or 0
        return self.stock.price*(1 + price_percent_update)

    class Meta:
        app_label = 'gas'
        verbose_name = _("GAS supplier stock")
        verbose_name_plural = _("GAS supplier stocks")

    @property
    def has_changed_availability(self):
        #TODO: add to GASSupplierSolidalPact model the inactive state of a solidal pact
        #if (not pact.is_active):
        #    self._msg.append('Solidal pact unactive')
        #    return False;
        try:
            #FIXME: Generate error raise self.model.DoesNotExist: GASSupplierStock matching query does not exist
            gss = GASSupplierStock.objects.get(pk=self.pk)
            if not gss is None:
                return bool(self.enabled != gss.enabled)
            else:
                return False
        except GASSupplierStock.DoesNotExist:
            return False

    @property
    def message(self):
        """getter property for internal message from model."""
        return self._msg

    def save(self, *args, **kwargs):

        # CASCADING
        if self.has_changed_availability:

            self._msg = []
            self._msg.append('   Changing for PDS %s(%s) and stock %s(%s)' %  (self.pact, self.pact.pk, self.stock, self.stock.pk) )
            #For each GASSupplierOrder in Open or Closed state Add or delete GASSupplierOrderProduct
            for order in self.orders.open():
                if self.enabled:
                    #FIXME: see issue #9
                    #Add GASSupplierOrderProduct only for GASSupplierOrder in Open State
                    order.add_product(self)
                else:
                    #Delete GASSupplierOrderProduct for GASSupplierOrder in Open State or Closed state. Delete GASMemberOrder associated
                    order.remove_product(self)
                if order.message is not None:
                    self._msg.extend(order.message)

        super(GASSupplierStock, self).save(*args, **kwargs)

    #-- Resource API --#

    @property
    def orders(self):
        #TODO FIXME AFTER 6
        print "AAAA: sto recuperando tutti gli ordini, ma vorrei solo quelli aperti. Correggere __alla chiamata__ aggiungendo .open()"
        from gasistafelice.gas.models.order import GASSupplierOrder
        return GASSupplierOrder.objects.filter(pact=self.pact)


#-----------------------------------------------------------------------------------------------------


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
    date_signed = models.DateField(verbose_name=_('Date signed'), auto_now=False, auto_now_add=False, blank=True, null=True, default=None, help_text=_("date of first meeting GAS-Producer"))

    # which Products GAS members can order from Supplier
    stock_set = models.ManyToManyField(SupplierStock, through=GASSupplierStock, null=True, blank=True)
    order_minimum_amount = CurrencyField(verbose_name=_('Order minimum amount'), null=True, blank=True)
    order_delivery_cost = CurrencyField(verbose_name=_('Order delivery cost'), null=True, blank=True)
    #time needed for the delivery since the GAS issued the order disposition
    order_deliver_interval = models.TimeField(verbose_name=_('Order delivery interval'), null=True, blank=True)
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

    default_withdrawal_place = models.ForeignKey(Place, verbose_name=_('Default withdrawal place'), related_name="pact_default_withdrawal_place_set", null=True, blank=True)

    # Field to reflect
    # http://www.jagom.org/trac/REESGas/wiki/BozzaAnalisiFunzionale/Gestione dei fornitori e dei listini
    # This MUST NOT be shown in form if GASConfig.auto_populate_products is True
    auto_populate_products = models.BooleanField(default=True, help_text=_("automatic population of all products bound to a supplier in gas supplier stock"))
    #TODO: Field to reflect "il GAS puo stracciare il Patto di Solidarieta."
    #TODO:is_active = models.BooleanField(default=True, help_text=_("This pact can be broken o removed by one of the partner. If not active no orders can be done and the pact will not appear anymore in the interface"))
    #TODO:is_suspended = models.BooleanField(default=False, help_text=_("This pact can be suspended when partners are on unavailable (hollidays, closed). The motor use this flag to operate or not some automatisms"))

    #document = models.FileField(upload_to="/pacts/", null=True, blank=True)

    history = HistoricalRecords()

    display_fields = (
        display.ResourceList(name="gas_supplier_referrers_persons", verbose_name=_("Referrers")),
        order_minimum_amount, order_delivery_cost, order_deliver_interval,
        default_withdrawal_place,
    )

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

    def setup_data(self):

        for st in self.supplier.stocks:
            #enabled = [False, self.auto_populate_products][bool(st.amount_available)]
            enabled = bool(st.amount_available)
            GASSupplierStock.objects.create(pact=self, stock=st, enabled=enabled)

    def save(self, *args, **kw):
        if self.gas.config.auto_populate_products:
            self.auto_populate_products = True

        super(GASSupplierSolidalPact, self).save(*args, **kw)

    #-- Resource API --#

    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return ""

    @property
    def parent(self):
        return self.gas

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.pk)

    @property
    def des(self):
        return self.gas.des

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def orders(self):
        return self.order_set.all()

    @property
    def gasstocks(self):
        return self.gasstock_set.all()

    @property
    def stock(self):
        raise NoSenseException("A GASSupplierSolidalPact is ALWAYS connected to more than one stock")
        
    @property
    def gasstock(self):
        raise NoSenseException("A GASSupplierSolidalPact is ALWAYS connected to more than one gas stock")

    @property
    def pact(self):
        return self
    
    @property
    def persons(self):
        return self.gas.persons | self.supplier.persons

    @property
    def gas_supplier_referrers_persons(self):
        return self.persons.filter(user__in=self.gas_supplier_referrers)

    #-- Permission management --#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, **kwargs):
        ## GAS administrators, GAS referres and GAS supplier referrers (of other pacts)
        ## can create a new pact for their GAS
        try:
            gas = kwargs['gas']
        except KeyError:
            raise SyntaxError("You need to specify a 'gas' argument to perform this permission check.")
        return (user in gas.tech_referrers) or (user in gas.referrers) or (user in gas.supplier_referrers)
 
    # Row-level EDIT permission
    def can_edit(self, user, **kwargs):
        # only GAS technical referrers and referrers for this pact can edit pact details
        return (user in self.gas.tech_referrers) or (user in self.gas_supplier_referrers) 
    
    # Row-level DELETE permission
    def can_delete(self, user, **kwargs):
        # only GAS technical referrers can delete a pact in a GAS
        return user in self.gas.tech_referrers       


#-------------------------------------------------------------------------------

def setup_data(sender, instance, created, **kwargs):
    """
    Setup proper data after a model instance is saved to the DB for the first time.
    This function just calls the `setup_roles()` instance method of the sender model class (if defined);
    actual role-creation/setup logic is encapsulated there.
    """
    if created: # Automatic data-setup should happen only at instance-creation time 
        try:
            # `instance` is the model instance that has just been created
            instance.setup_data()
                                                
        except AttributeError:
            # sender model doesn't specify any data-related setup operations, so just ignore the signal
            pass

# add `setup_data` function as a listener to the `post_save` signal
post_save.connect(setup_data)
