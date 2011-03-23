"""This model includes information about products, suppliers, producers.

These are fundamental DES data to relies on. They represents market offering.

It relies on base model.

Definition: `Vocabolario - Fornitori <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#Fornitori>`__ (ita only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base import const
from gasistafelice.base.models import Person

class Supplier(models.Model):
    """The actor who has a stock of products to sell in the DES"""

    name = models.CharField(max_length=128) 
    address =  models.CharField(max_length=128, blank=True)
    vat_number =  models.CharField(max_length=128)
    home_page =  models.CharField(max_length=128, blank=True)
    referrers = models.ManyToManyField(Person, through="SupplierReferrer") 
    flavour = models.CharField(max_length=128, choices=const.SUPPLIER_FLAVOUR_LIST, default=const.SUPPLIER_FLAVOUR_LIST[0][0])
    cert_set = models.ManyToManyField('Certification')

    # the set of products provided by this Supplier to every GAS
    @property
    def product_catalog(self):
        return [s.product for s in SupplierStock.objects.filter(supplier=self)]

    def __unicode__(self):
        return self.name

class SupplierReferrer(models.Model):

    supplier = models.ForeignKey(Supplier)
    person = models.ForeignKey(Person)
    job_role = models.CharField(max_length=256, blank=True)
    job_description = models.TextField(blank=True)

    
class Certification(models.Model):
    name = models.CharField(max_length=128) 
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class ProductCategory(models.Model):
    # Proposal: the name is in the form MAINCATEGORY::SUBCATEGORY
    # like sourceforge categories
    # Proposta usare solo il nome CATEGORIA::SOTTOCATEGORIA
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class ProductMU(models.Model):
    """Measurement unit for the product.

    Implemented as a separated entity like GasDotto software.
    Each supplier referrer has to be able to create its own measurement units.
    """
    name = models.CharField(max_length=32, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Product(models.Model):

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    producer = models.ForeignKey(Supplier)
    category = models.ForeignKey(ProductCategory)
    mu = models.ForeignKey(ProductMU)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    
    def permission_check(self, user, perm):

        if perm == const.SUPPLIER_REFERRER:
            rv = user in self.referrers.values_list('user')
        elif perm == const.GAS_REFERRER_TECH:
            rv = True
#        elif perm == const.STACIPPA:
#            rv = False
#            for i in self.referrers:
#                if i.name == "stacippa":
#                    rv = True
#                    break
        else:
            # We checked all available permissions...
            raise PermissionDoesNotExist
        return rv

    @property
    def referrers(self):
        return self.producer.referrers.all()

class SupplierStock(models.Model):
    """Product that a Supplier offers in the DES marketplace"""

    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    price = models.FloatField()
    amount_available = models.PositiveIntegerField(default=const.ALWAYS_AVAILABLE)
    # Amount and step are referred to the supplier
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def producer(self):
        return self.product.producer

