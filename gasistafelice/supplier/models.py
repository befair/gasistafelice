"""These models include information about Products, Suppliers, Producers.

These are fundamental DES data to rely on. They represent market offering.

Models here rely on base model classes.

Definition: `Vocabolario - Fornitori <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#Fornitori>`__ (ITA only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from history.models import HistoricalRecords

from gasistafelice.exceptions import NoSenseException
from gasistafelice.lib.fields.models import CurrencyField
from gasistafelice.lib.fields import display

from gasistafelice.base.const import SUPPLIER_FLAVOUR_LIST, ALWAYS_AVAILABLE
from gasistafelice.base.models import PermissionResource, Person, Place
from gasistafelice.des.models import DES, Siteattr

from gasistafelice.auth import SUPPLIER_REFERRER
from gasistafelice.auth.utils import register_parametric_role
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.exceptions import WrongPermissionCheck

class Supplier(models.Model, PermissionResource):
    """An actor having a stock of Products for sale to the DES."""

    name = models.CharField(max_length=128) 
    seat = models.ForeignKey(Place, null=True, blank=True)
    vat_number = models.CharField(max_length=128, unique=True, null=True) #TODO: perhaps a custom field needed here ? (for validation purposes)
    website = models.URLField(verify_exists=True, blank=True)
    referrer_set = models.ManyToManyField(Person, through="SupplierReferrer") 
    flavour = models.CharField(max_length=128, choices=SUPPLIER_FLAVOUR_LIST, default=SUPPLIER_FLAVOUR_LIST[0][0])
    certifications = models.ManyToManyField('Certification', null=True, blank=True)

    #FUTURE TODO des = models.ManyToManyField(DES, null=True, blank=True)

    history = HistoricalRecords()
    
    def __unicode__(self):
        return unicode(self.name)

    def setup_roles(self):
    #    # register a new `SUPPLIER_REFERRER` Role for this Supplier
        register_parametric_role(name=SUPPLIER_REFERRER, supplier=self) 

    #-- Resource API --#

    @property
    def des(self):
        return Siteattr.get_site()

    @property
    def ancestors(self):
        return [self.des]

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.pk)

    @property
    def supplier(self):
        return self

    @property
    def referrers(self):
        return self.referrer_set.all()

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def pacts(self):
        return self.pact_set.all()

    @property
    def pact(self):
        raise NoSenseException("calling supplier.pact is a no-sense. Supplier is related to more than one pact")
        
    @property
    def orders(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def order(self):
        raise NoSenseException("calling supplier.order is a no-sense. Supplier is related to more than one order")

    @property
    def gas_list(self):
        from gasistafelice.gas.models.base import GAS
        return GAS.objects.filter(pact_set__in=self.pacts)

    @property
    def gas(self):
        raise NoSenseException("calling supplier.gas is a no-sense. Supplier is related to more than one gas")

    @property
    def products(self):
        """All products _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all products __produced__ by this supplier
        return Product.objects.filter(stock_set__in=self.stocks)

    @property
    def categories(self):
        """All categories _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all categories __produced__ by this supplier
        return ProductCategory.objects.filter(product_set__in=self.products)

    @property
    def persons(self):
        return self.referrer_set.all()
    
    @property
    def referrers_as_users(self):
        """
        Return all users being referrers for this supplier.
        """
        # retrieve 'Supplier Referrer' parametric role for this supplier
        pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=self)
        # retrieve all Users having this role
        return pr.get_users()
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new supplier in a DES ?
        # * DES administrators
        # * referrers and administrators of every GAS in the DES
        try:
            des = context['des']
            all_gas_referrers = set()
            all_gas_referrers_tech = set()
            for gas in des.gas_list:
                all_gas_referrers = all_gas_referrers | gas.referrers
                all_gas_referrers_tech = all_gas_referrers_tech | gas.tech_referrers
            allowed_users = des.admins | all_gas_referrers | all_gas_referrers_tech 
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a Supplier in a DES ?
        # * DES administrators
        # * referrers for that supplier        
        allowed_users = self.des.admins | self.referrers_as_users
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can remove a supplier from a DES ?
        # * DES administrators
        allowed_users = self.des.admins
        return user in allowed_users 
    
    #-----------------------------------------------#       


    display_fields = (
        seat, vat_number, website, flavour, 
        display.ResourceList(name="referrers", verbose_name=_("People")),
        display.ResourceList(name="pacts", verbose_name=_("Pacts")),
    )

  
class SupplierReferrer(models.Model, PermissionResource):

    supplier = models.ForeignKey(Supplier)
    person = models.ForeignKey(Person)
    job_title = models.CharField(max_length=256, blank=True)
    job_description = models.TextField(blank=True)
    
    history = HistoricalRecords()

    @property
    def ancestors(self):
        return [self.des, self.supplier]
    
    def setup_roles(self):
        # automatically add a new SupplierReferrer to the `SUPPLIER_REFERRER` Role
        user = self.person.user
        role = register_parametric_role(name=SUPPLIER_REFERRER, supplier=self.supplier)
        role.add_principal(user)   
        
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new referrer for an existing supplier in a DES ?
        # * DES administrators
        # * referrers and administrators of every GAS in the DES
        try:
            des = context['des']
            all_gas_referrers = set()
            all_gas_referrers_tech = set()
            for gas in des.gas_list:
                all_gas_referrers = all_gas_referrers | gas.referrers
                all_gas_referrers_tech = all_gas_referrers_tech | gas.tech_referrers
            allowed_users = des.admins | all_gas_referrers | all_gas_referrers_tech 
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)
        
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a supplier referrer ?
        # * DES administrators
        # * the referrer itself
        allowed_users = set(self.supplier.des.admins) | set(self.person.user) 
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a supplier referrer ?
        # * DES administrators
        # * other referrers for that supplier  
        allowed_users = self.supplier.des.admins | self.supplier.referrers_as_users
        return user in allowed_users 
    
    #-----------------------------------------------#  
    
class Certification(models.Model, PermissionResource):
    name = models.CharField(max_length=128, unique=True) 
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.name

#-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new certification ?
        # * DES administrators
        try:            
            des_admins_all = set()
            for des in DES.objects.all():
                des_admins_all = des_admins_all | des.admins
            allowed_users = des_admins_all
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing certification ?
        # * DES administrators         
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing certification ?
        # * DES administrators
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users     
        
    #-----------------------------------------------#


class ProductCategory(models.Model, PermissionResource):
    # Proposal: the name is in the form MAINCATEGORY::SUBCATEGORY
    # like sourceforge categories
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = _("Product categories")

    def __unicode__(self):
        return self.name
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new category for products ?
        # * DES administrators
        try:            
            des_admins_all = set()
            for des in DES.objects.all():
                des_admins_all = des_admins_all | des.admins
            allowed_users = des_admins_all
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing category ?
        # * DES administrators         
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing category ?
        # * DES administrators
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users

    #-----------------------------------------------#

class ProductMU(models.Model, PermissionResource):
    """Measurement unit for a Product."""
    # Implemented as a separated entity like GasDotto software.
    # Each SupplierReferrer has to be able to create its own measurement units.
    
    name = models.CharField(max_length=32, unique=True, blank=False)
    symbol = models.CharField(max_length=5, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.symbol
    
    class Meta():
        verbose_name="measurement unit"
        verbose_name_plural="measurement units"
    
        #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new unit of measure for products ?
        # * DES administrators
        try:            
            des_admins_all = set()
            for des in DES.objects.all():
                des_admins_all = des_admins_all | des.admins
            allowed_users = des_admins_all
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing unit of measure for products ?
        # * DES administrators         
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing unit of measure for products ?
        # * DES administrators
        des_admins_all = set()
        for des in DES.objects.all():
            des_admins_all = des_admins_all | des.admins        
        allowed_users = des_admins_all
        return user in allowed_users

    #-----------------------------------------------#

    

class Product(models.Model, PermissionResource):

    # COMMENT: some producer don't have product codification. 
    # That's why uuid could be blank AND null. See save() method
    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, verbose_name='UUID', help_text=_("Product code"))
    producer = models.ForeignKey(Supplier, related_name="produced_product_set")
    # Resource API
    category = models.ForeignKey(ProductCategory, null=True, blank=True, related_name="product_set")
    mu = models.ForeignKey(ProductMU, blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    
    history = HistoricalRecords()
    
    def __unicode__(self):
        return unicode(self.name)
        #return self.name.decode('utf8')

    @property
    def referrers(self):
        return self.producer.referrers
  
    def save(self, *args, **kw):
        # If uuid is blank, make it NULL
        if not self.uuid:
            self.uuid = None
        return super(Product, self).save(*args, **kw)

    # Resource API
    #def categories(self):
    #    # A product belongs to one category
    #    return self.category

    # Resource API
    #@property
    #def suppliers(self):
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new product to a supplier catalog ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers_as_users
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a product in a supplier catalog ?
        # * referrers for that supplier
        allowed_users = self.producer.referrers_as_users
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a product from a supplier catalog ?
        # * referrers for that supplier
        allowed_users = self.producer.referrers_as_users
        return user in allowed_users 
    
    #-----------------------------------------------#

class SupplierStock(models.Model, PermissionResource):
    """A Product that a Supplier offers in the DES marketplace.
        
       Includes price, order constraints and availability information.

    >>> from supplier.models import *
    >>> ss = SupplierStock.objects.get(pk=1)
    >>> isinstance(ss, SupplierStock)
    True
    >>> ss.has_changed_availability
    Fasle
    >>> ss.amount_available = ss.amount_available + 1
    >>> ss.has_changed_availability
    True

    """

    # Resource API
    supplier = models.ForeignKey(Supplier, related_name="stock_set")
    # Resource API
    product = models.ForeignKey(Product, related_name="stock_set")
    price = CurrencyField(verbose_name=_("price"))
    code = models.CharField(verbose_name=_("code"), max_length=128, null=True, blank=True, help_text=_("Product supplier identifier"))
    amount_available = models.PositiveIntegerField(verbose_name=_("availability"), default=ALWAYS_AVAILABLE)
    ## constraints posed by the Supplier on orders issued by *every* GAS
    # minimum amount of Product units a GAS is able to order 
    #COMMENT: minimum amount of Product units a GASMember is able to order 
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum; 
    # useful when a Product ships in packages containing multiple units.
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    #TODO: Field for Product units per box
    # how the Product will be delivered
    delivery_terms = models.TextField(null=True, blank=True) #FIXME: find a better name for this attribute 
    #TODO: Notify system

    history = HistoricalRecords()

    class Meta:
        unique_together = (('code', 'supplier'),)

    def __init__(self, *args, **kw):
        super(SupplierStock, self).__init__(*args, **kw)
        self._msg = None

    def __unicode__(self):
        return '%s (by %s)' % (unicode(self.product), unicode(self.supplier))

    @property
    def producer(self):
        return self.product.producer

    @property
    def availability(self):
        return bool(self.amount_available)

    @property
    def has_changed_availability(self):
        try:
            ss = SupplierStock.objects.get(pk=self.pk)
            if not ss is None:
                return bool(self.amount_available != ss.amount_available)
            else:
                return False
        except SupplierStock.DoesNotExist:
            return False

    @property
    def message(self):
        """getter property for internal message from model."""
        return self._msg

    def save(self, *args, **kwargs):

        # if `code` is set to an empty string, set it to `None`, instead, before saving,
        # so it's stored as NULL in the DB, avoiding integrity issues.
        if not self.code:
            self.code = None

        # CASCADING
        if self.has_changed_availability:
            self._msg = []
            self._msg.append('Availability have changed for product %s' %  self.product)
            #For each GASSupplierStock (present for each GASSupplierSolidalPact) set new availability and save
            for gss in self.gasstocks:
                if (self.availability != gss.enabled):
                    gss.enabled = self.availability
                    gss.save()
                    if not gss.message is None:
                        self._msg.extend(gss.message)
            self._msg.append('Ended(%d)' % self.gasstocks.count())
            print self._msg
        super(SupplierStock, self).save(*args, **kwargs)

    #-- Resource API --#

    @property
    def gasstocks(self):
        return self.gasstock_set.all()
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new stock to a supplier catalog ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers_as_users
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a stock in  a supplier catalog ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers_as_users
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a stock from  a supplier catalog ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers_as_users
        return user in allowed_users 
    
    #-----------------------------------------------#


class SupplierProductCategory(models.Model):
    """Map supplier categories to product categories with an optional alias.

    This is useful to know WHICH categories a suppplier CAN sell,
    and so limiting the choice in product selections."""

    category = models.ForeignKey(ProductCategory)
    supplier = models.ForeignKey(Supplier)
    alias = models.CharField(verbose_name=_('Alternative name'), max_length=128, blank=True)

    @property
    def name(self):
        return self.alias or self.category.name
 
    def __unicode__(self):
        return self.name
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new supplier-specific category ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers_as_users
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a supplier-specific category ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers_as_users
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a supplier-specific category ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers_as_users
        return user in allowed_users 
    
    #-----------------------------------------------#