from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from permissions.models import Role
from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.models import Resource, Person

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, Product

from gasistafelice.gas import managers

from workflows.models import Workflow, Transition

class GAS(Resource, PermissionBase, models.Model):
    """A group of people which make some purchases together.
    Every GAS member has a Role where the basic Role is just to be a member of the GAS.

    """
    #TODO: Prevedere qui tutta la parte di configurazione del GAS

    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to="/images/", null=True, blank=True)
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"), null=True, blank=True)

    workflow_default_gasmember_order = models.ForeignKey(Workflow, related_name="gasmember_order_set", null=True, blank=True)
    workflow_default_gassupplier_order = models.ForeignKey(Workflow, related_name="gassupplier_order_set", null=True, blank=True)

    suppliers = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True)
    objects = managers.GASRolesManager()

    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'

    def __unicode__(self):
        return self.name
    
    def setup_roles(self):
        # register a new `GAS_MEMBER` Role for this GAS
        register_parametric_role(name=GAS_MEMBER, param1=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_TECH, param1=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_CASH, param1=self)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv  
    

class GASMember(Resource, PermissionBase, models.Model):
    """A bind of a Person into a GAS.
    Each GAS member specifies which Roles he is available for.
    This way, every time there is a need to assign one or more GAS Members to a given Role,
    there is already a group of people to choose from. 
    
    """

    person = models.ForeignKey(Person)
    gas = models.ForeignKey(GAS)
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members_available")
    roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members")

    def __unicode__(self):
        return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}

    
    def setup_roles(self):
        # automatically add a new GASMember to the `GAS_MEMBER` Role
        user = self.person.user
        role = register_parametric_role(name=GAS_MEMBER, param1=self.gas)
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
       
    def save(self):
    #    self.first_name = self.name
    #    self.last_name = self.last_name
        super(GASMember, self).save()         
   
    class Meta:
        app_label = 'gas'

class GASSupplierSolidalPact(Resource, PermissionBase, models.Model):
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
    # TODO: should be a `CurrencyField` 
    order_minimum_amount = models.FloatField(null=True, blank=True)
    # TODO: should be a `CurrencyField`
    order_delivery_cost = models.FloatField(null=True, blank=True)
    #time needed for the delivery since the GAS issued the order disposition
    order_deliver_interval = models.TimeField()  
    # how much (in percentage) base prices from the Supplier are modified for the GAS  
    order_price_percent_update = models.FloatField()
    # TODO must be a property (use django-permissions)
    #supplier_referrers = ...
    
    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this GAS/Supplier pair
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, param1=self.gas, param2=self.supplier)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
     
    class Meta:
        app_label = 'gas'


