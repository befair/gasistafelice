"""These models include information about Products, Suppliers, Producers.

These are fundamental DES data to rely on. They represent market offering.

Models here rely on base model classes.

Definition: `Vocabolario - Fornitori <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#Fornitori>`__ (ITA only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from history.models import HistoricalRecords

from gasistafelice.base.const import SUPPLIER_FLAVOUR_LIST, ALWAYS_AVAILABLE
from gasistafelice.base.models import Resource, PermissionResource, Person, Place

from gasistafelice.auth import SUPPLIER_REFERRER
from gasistafelice.auth.utils import register_parametric_role

class Supplier(models.Model, PermissionResource):
    """An actor having a stock of Products for sale to the DES."""

    name = models.CharField(max_length=128) 
    seat =  models.ForeignKey(Place, null=True, blank=True)
    vat_number =  models.CharField(max_length=128, unique=True) #TODO: perhaps a custom field needed here ? (for validation purposes)
    website =  models.URLField(verify_exists=True, blank=True)
    referrers = models.ManyToManyField(Person, through="SupplierReferrer") 
    flavour = models.CharField(max_length=128, choices=SUPPLIER_FLAVOUR_LIST, default=SUPPLIER_FLAVOUR_LIST[0][0])
    certifications = models.ManyToManyField('Certification', null=True, blank=True)

    history = HistoricalRecords()

    # the set of products provided by this Supplier to every GAS
    @property
    def product_catalog(self):
        return [s.product for s in SupplierStock.objects.filter(supplier=self)]
    
    def __unicode__(self):
        return self.name
    
    def setup_roles(self):
        # register a new `SUPPLIER_REFERRER` Role for this Supplier
        register_parametric_role(name=SUPPLIER_REFERRER, supplier=self)
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv   
        
    
class SupplierReferrer(models.Model, PermissionResource):
    supplier = models.ForeignKey(Supplier)
    person = models.ForeignKey(Person)
    job_title = models.CharField(max_length=256, blank=True)
    job_description = models.TextField(blank=True)
    
    history = HistoricalRecords()

    
    def setup_roles(self):
        # automatically add a new SupplierReferrer to the `SUPPLIER_REFERRER` Role
        user = self.person.user
        role = register_parametric_role(name=SUPPLIER_REFERRER, supplier=self.supplier)
        role.add_principal(user)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
    
class Certification(models.Model, PermissionResource):
    name = models.CharField(max_length=128, unique=True) 
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.name
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

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
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

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
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
class Product(models.Model, PermissionResource):

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, verbose_name='UUID') # if empty, should be programmatically set at DB save time
    producer = models.ForeignKey(Supplier)
    category = models.ForeignKey(ProductCategory)
    mu = models.ForeignKey(ProductMU, blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    
    history = HistoricalRecords()
    
    def __unicode__(self):
        return self.name

    @property
    def referrers(self):
        return self.producer.referrers.all()
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

class SupplierStock(models.Model, PermissionResource):
    """A Product that a Supplier offers in the DES marketplace.
        
       Includes price, order constraints and availability information.          
    """

    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    price = models.FloatField() # FIXME: should be a `CurrencyField` ?
    amount_available = models.PositiveIntegerField(default=ALWAYS_AVAILABLE)
    ## constraints posed by the Supplier on orders issued by *every* GAS
    # minimum amount of Product units a GAS is able to order 
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum; 
    # useful when a Product ships in packages containing multiple units.
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    # how the Product will be delivered
    delivery_terms = models.TextField(null=True, blank=True) #FIXME: find a better name for this attribute 

    history = HistoricalRecords()
    
    def __unicode__(self):
        return "%s (by %s)" % (self.product, self.supplier)

    @property
    def producer(self):
        return self.product.producer
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
