"""These models include everything necessary to manage GAS activity.

They rely on base models and Supplier-related ones to get Product and Stock infos.

Definition: `Vocabolario - GAS <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#GAS>`__ (ita only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base.models import Person, Role
from gasistafelice.supplier.models import Supplier, SupplierStock, Product

from gasistafelice.base.utils import register_role
from gasistafelice.gas.const import STATES_LIST, GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER
from gasistafelice.gas import managers

from workflows.models import Workflow, Transition

class GAS(models.Model):
    """A group of people which make some purchases together.
    Every GAS member has a Role where the basic Role is just to be a member of the GAS.

    """
    #TODO: Prevedere qui tutta la parte di configurazione del GAS

    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to="/images/")
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"))

    workflow_default_gasmember_order = models.ForeignKey(Workflow, related_name="gasmember_order_set")
    workflow_default_gassupplier_order = models.ForeignKey(Workflow, related_name="gassupplier_order_set")

    suppliers = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact')

    objects = managers.GASRolesManager()

    class Meta:
        verbose_name_plural = _('GAS')

    def __unicode__(self):
        return self.name
    
    def save(self):
        super(GAS, self).save()
        # register a new `GAS_MEMBER` Role for this GAS
        register_role(name=GAS_MEMBER, gas=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_role(name=GAS_REFERRER_TECH, gas=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_role(name=GAS_REFERRER_CASH, gas=self)
    

class GASMember(models.Model):
    """A bind of a Person into a GAS.
    Each GAS member specifies which Roles he is available for.
    This way, every time there is a need to assign one or more GAS Members to a given Role,
    there is already a group of people to choose from. 
    
    """

    person = models.ForeignKey(Person)
    gas = models.ForeignKey(GAS)
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members_available_for_this_role")
    roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members_with_this_role")

    def __unicode__(self):
        return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}

    def save(self):
    # TODO: automatically add a new GASMember to the `GAS_MEMBER` Role
    #    self.first_name = self.name
    #    self.last_name = self.last_name
         super(GASMember, self).save()
   
class GASSupplierSolidalPact(models.Model):
    """Define a GAS <-> Supplier relationship agreement.
    
    Each Supplier comes into relationship with a GAS by signing this pact,
    where are factorized behaviour agreements between these two entities.
    This pact acts as a configurator for order and delivery management with respect to the given Supplier.
    """

    gas = models.ForeignKey(GAS)
    supplier = models.ForeignKey(Supplier)
    date_signed = models.DateField()
    # which Products GAS members can order from Supplier
    supplier_gas_catalog = models.ManyToManyField(Product, null=True, blank=True)
    # FIXME: perhaps should be a `CurrencyField` ?
    order_minimum_amount = models.FloatField(null=True, blank=True)
    # FIXME: perhaps should be a `CurrencyField` ?
    order_delivery_cost = models.PositiveIntegerField(null=True, blank=True)
    #time needed for the delivery since the GAS issued the order disposition
    order_deliver_interval = models.TimeField()  
    # how much (in percentage) base prices from the Supplier are modified for the GAS  
    order_price_percent_update = models.FloatField()
    # TODO
    #supplier_referrers = ...
    
    def save(self):
        super(GASSupplierSolidalPact, self).save()
        # register a new `GAS_REFERRER_SUPPLIER` Role for this GAS/Supplier pair
        register_role(name=GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)

    
