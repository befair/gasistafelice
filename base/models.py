from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from gasistafelice.base import managers
from gasistafelice.base.const import STATES_LIST, ROLES_LIST, MU_CHOICES, ALWAYS_AVAILABLE, SUPPLIER_FLAVOUR_LIST, CONTACT_CHOICES

class GAS(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"))
    roles = models.ManyToManyField("Person", through="GASMember")

    objects = managers.GASRolesManager()

    #TODO: Prevedere qui tutta la parte di configurazione del GAS

    class Meta:
        verbose_name_plural = _('GAS')

    def __unicode__(self):
        return self.name
    

#class GASRoleMap(models.Model):
#    """Dobbiamo semplificare l'assegnazione dei ruoli?
#    Memorizzare "nome ruolo" -> "gas" -> "ruolo in ROLES_LIST"?
#    Questo serve molto a gestire il GAS come lo si e' sempre fatto
#    e con la consapevolezza dei ruoli che ci potrebbero essere.
#    Alla fine potremmo farne tranquillamente a meno se e' sempre il tecnico
#    che abilita il nuovo utente"""
#    name = models.CharField(max_length=128, choices=ROLES_LIST, default=ROLES_LIST[0][0])

class Contact(models.Model):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

class Person(models.Model):
    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    displayName = models.CharField(max_length=128)
    contacts = models.ManyToManyField(Contact)
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)
   
class Role(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    
class GASMember(models.Model):
    """A GAS member is a bind of a Person into a GAS.

    """
    person = models.ForeignKey(Person)
    gas = models.ForeignKey(GAS)
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gasmember_available_for_roles_set")
    roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gasmember_set")

    def __unicode__(self):
        return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}

#    def save(self):
#        self.first_name = self.name
#        self.last_name = self.last_name
#        super(GASUser, self).save()
    
class Certification(models.Model):
    name = models.CharField(max_length=128) 
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=128) 
    referrers = models.ManyToManyField(Person) 
    flavour = models.CharField(max_length=128, choices=SUPPLIER_FLAVOUR_LIST, default=SUPPLIER_FLAVOUR_LIST[0][0])
    gas_set = models.ManyToManyField(GAS, through='GASSupplierSolidalPact')
    cert_set = models.ManyToManyField(Certification)

    def __unicode__(self):
        return self.name

class GASSupplierSolidalPact(models.Model):
    """Define GAS <-> Supplier relationship agreement"""

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_signed = models.DateField()
    minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    delivery_cost = models.PositiveIntegerField(null=True, blank=True)
    order_deliver_interval = models.TimeField()
    price_percent_update = models.FloatField()
    
class ProductCategory(models.Model):
    # Proposal: the name is in the form MAINCATEGORY::SUBCATEGORY
    # like sourceforge categories
    # Proposta usare solo il nome CATEGORIA::SOTTOCATEGORIA
    # Proposta2 ... si potrebbe usare direttamente il nome come PRIMARY KEY della tabella? Utile per ricerche.
    name = models.CharField(max_length=128, unique=True, blank=False)

    def __unicode__(self):
        return self.name

class Product(models.Model):

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    producer = models.ForeignKey(Supplier)
    supplier = models.ForeignKey(Supplier)
    category = models.ForeignKey(ProductCategory)
    # Fare un riferimento esterno?. Mi sa di si... GasDotto lo fa.
    mu = models.CharField(max_length=16, choices=MU_CHOICES, default=MU_CHOICES[0][0])
    name = models.CharField(max_length=128)
    description = models.TextField()

    def perm_check(self, perm, user):
        if perm == const.SUPPLIER_REFERRER:
            rv = user in self.referrers.values_list('user')
        return rv

    @property
    def referrers(self):
        return self.supplier.referrers.all()

class SupplierStock(models.Model):
    # Il prodotto a disposizione del DES

    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    price = models.FloatField()
    amount_available = models.PositiveIntegerField(default=ALWAYS_AVAILABLE)
    minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    step = models.PositiveSmallIntegerField(null=True, blank=True)

class SupplierStockGAS(models.Model):
    # Product as available to GAS
    gas = models.ForeignKey(GAS)
    supplier_stock = models.ForeignKey(SupplierStock)
    minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    step = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def supplier(self):
        return self.supplier_stock.supplier

    @property
    def price(self):
        # Price is updated by GASSupplierSolidalPact
        price_percent_update = self.supplier.gas_set.get(gas=self.gas).price_percent_update
        return self.supplier_stock.price*price_percent_update

class Place(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    #TODO geolocation: use GeoDjango PointField?
    lon = models.FloatField()
    lat = models.FloatField()


class SupplierOrder(models.Model):

    supplier = models.ForeignKey(Supplier)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    # Dove e quando si consegna
    delivery_date = models.DateTimeField()
    delivery_place = models.ForeignKey(Place, related_name="delivery_for_order_set")
    # Quanto ha consegnato 
    delivery_amount = models.PositiveIntegerField()
    # Dove e quando si ritira
    withdrawal_date = models.DateTimeField()
    withdrawal_place = models.ForeignKey(Place, related_name="withdraw_for_order_set")

    status = models.CharField(max_length=32, choices=STATES_LIST)
    product_set = models.ManyToManyField(SupplierStock)
    

#class GasUserOrder(models.Model):
#
#    gas_user = models.ForeignKey(GASUser)
#    product = models.ForeignKey(Product)
#    order_amount = models.PositiveIntegerField()
#    withdrawal_amount = models.PositiveIntegerField()
#    supplier_order = models.ForeignKey(Supplier)
#    status = models.CharField(choices=STATES_LIST)
#    date_created = models.DateTimeField()
#    date_last_update=models.DateTimeField()
#
#
