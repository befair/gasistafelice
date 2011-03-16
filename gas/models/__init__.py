"""This model includes all thing necessary to manage GAS activity.

It relies on base model and on supplier model to get products and stock infos.

Definition: `Vocabolario - GAS <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#GAS>`__ (ita only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base.models import Person, Role
from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.gas.const import STATES_LIST
from gasistafelice.gas import managers

class GAS(models.Model):
    """A a group of people which make some purchases altogether.
    Every GAS member has a role where the basic role is just to be a member of the GAS.

    """

    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to="/images/")
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"))
    supplier_set = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact')

    objects = managers.GASRolesManager()

    #TODO: Prevedere qui tutta la parte di configurazione del GAS

    class Meta:
        verbose_name_plural = _('GAS')

    def __unicode__(self):
        return self.name
    

class GASMember(models.Model):
    """A bind of a Person into a GAS.
    Each GAS member specifies for which role he is available for.
    In this way every time a user (i.e. user with proper rights) has to bind a role to
    a GAS member he can choose among available users.

    """

    person = models.ForeignKey(Person)
    gas = models.ForeignKey(GAS)
    available_for_role_set = models.ManyToManyField(Role, null=True, blank=True, related_name="gasmember_available_for_roles_set")
    role_set = models.ManyToManyField(Role, null=True, blank=True, related_name="gasmember_set")

    def __unicode__(self):
        return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}

#    def save(self):
#        self.first_name = self.name
#        self.last_name = self.last_name
#        super(GASUser, self).save()
    
class GASSupplierSolidalPact(models.Model):
    """Define GAS <-> Supplier relationship agreement
    Each supplier come into relathionship with a GAS by signing this pact.
    In this pact we factorize behaviour agreements 
    between these two entities.
    It acts as configuration for order and delivery management 
    to the specific supplier.
    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_signed = models.DateField()
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    order_delivery_cost = models.PositiveIntegerField(null=True, blank=True)
    order_deliver_interval = models.TimeField()
    order_price_percent_update = models.FloatField()
    
class GASSupplierStock(models.Model):
    """Product as available to GAS"""
    gas = models.ForeignKey(GAS)
    supplier_stock = models.ForeignKey(SupplierStock)
    # Amount and step refers to what a single GAS member could purchase
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def supplier(self):
        return self.supplier_stock.supplier

    @property
    def price(self):
        # Price is updated by GASSupplierSolidalPact
        price_percent_update = self.gas.supplier_set.get(supplier=self.supplier).price_percent_update
        return self.supplier_stock.price*price_percent_update

class GASSupplierOrder(models.Model):
    """Order managed in a GAS.

    * status is a meaningful parameter... TODO
    * product_set references specified products available for the specific order \
      (they can be a subset of all available products from that supplier for the order);
    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_start = models.DateTimeField(help_text=_("when the order will be available"))
    date_end = models.DateTimeField(help_text=_("when the order will be closed"))
    # Where and when delivery occurs
    delivery_date = models.DateTimeField(help_text=_("when the order will be delivered by supplier"))
    delivery_place = models.ForeignKey('Place', related_name="delivery_for_order_set", help_text=_("where the order will be delivered by supplier"))
    # How much has been delivered 
    delivery_amount = models.PositiveIntegerField()
    # Where and when withdraw occurs
    withdraw_date = models.DateTimeField(help_text=_("when the order will be withdrawn by GAS members"))
    withdraw_place = models.ForeignKey('Place', related_name="withdraw_for_order_set", help_text=_("where the order will be withdrawn by GAS members"))

    status = models.CharField(max_length=32, choices=STATES_LIST, help_text=_("which is the state of the order"))
    product_set = models.ManyToManyField(GASSupplierStock, help_text=_("products available for the order"), blank=True)

    def save(self):
        # If no product_set has been specified --> use all products bound to the supplier
        super(GASSupplierOrder, self).save()
        if not self.product_set.all():
            for product in self.gas.supplier_set.get(self.supplier).all():
                self.product_set.add(product)
        return
    

class Place(models.Model):
    """Place should be managed as a separate entity because of:

    * multiple Place useful for retina orders
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    #TODO geolocation: use GeoDjango PointField?
    lon = models.FloatField(blank=True)
    lat = models.FloatField(blank=True)


