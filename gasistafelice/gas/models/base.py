from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from permissions.models import Role
from workflows.models import Workflow
from history.models import HistoricalRecords

from gasistafelice.base.models import PermissionResource, Person

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, Product

from gasistafelice.gas import managers

from gasistafelice.bank.models import Account, Movement

class GAS(PermissionResource, models.Model):

    """A group of people which make some purchases together.
    Every GAS member has a Role where the basic Role is just to be a member of the GAS.

    """
    #TODO: Prevedere qui tutta la parte di configurazione del GAS
    config_change_price = models.BooleanField(help_text=_("GAS change supplier list price or not"))  
    config_view_subjective = models.BooleanField(help_text=_("GAS use subjective or economic views "))  
    config_deliver_only_one = models.BooleanField(help_text=_("GAS use only one delivery place"))  
    config_close_day = models.DateField(auto_now=False, null=True, help_text=_("default order closing day of the week")) 
    config_close_time = models.TimeField(help_text=_("default order closing hour and minutes"))  
    config_deliver_day = models.BooleanField(help_text=_("default delivery closing day of the week"))  
    config_deliver_time = models.TimeField(help_text=_("default delivery closing hour and minutes"))  

    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to="/images/", null=True, blank=True)
    identifier = models.CharField("GAS code (3 letters)", max_length=3, null=False, blank=False, help_text=_("Insert here your GAS unique identier in the DES. For example: CAMERINO--> CAM"))	
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"), null=True, blank=True)

    workflow_default_gasmember_order = models.ForeignKey(Workflow, related_name="gasmember_order_set", null=True, blank=True)
    workflow_default_gassupplier_order = models.ForeignKey(Workflow, related_name="gassupplier_order_set", null=True, blank=True)

    suppliers = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True)

    objects = managers.GASRolesManager()
    history = HistoricalRecords()

    account = models.ForeignKey(Account, null=True, blank=True, related_name="gas_account")
    liquidity = models.ForeignKey(Account, null=True, blank=True, related_name="gas_liquidity")

    active = models.BooleanField()
    birthday = models.DateField()
    vat =  models.CharField(max_length=11, null=True, blank=True, help_text=_("VAT number"))	
    fiscal_code =  models.CharField(max_length=16, null=True, blank=False, help_text=_("Fiscal code"))	
    email_gas = models.EmailField()
    email_referrer = models.EmailField(null=True, blank=True, help_text=_("Email coordinator"))
    phone = models.CharField(max_length=50, null=True, blank=True)	
    website = models.URLField(verify_exists=True, null=True, blank=True) 
    #TODO: gallery album
    #TODO: generic class documents 
    #documents = models.ManyToManyField(Document)
    association_act = models.FileField(upload_to='gasdocs', null=True, blank=True)
    intent_act = models.FileField(upload_to='gasdocs', null=True, blank=True)
    #TODO: Widget wysywig
    note = models.TextField(null=True, blank=True)
    #TODO: rotation turn --> referrer through GASMemberSupplier
    #TODO: motor
    motor_active = models.BooleanField()  
   
    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'

    def __unicode__(self):
        return self.name
    
    def setup_roles(self):
        # register a new `GAS_MEMBER` Role for this GAS
        register_parametric_role(name=GAS_MEMBER, gas=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_TECH, gas=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_CASH, gas=self)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv  
    

class GASMember(PermissionResource, models.Model):
    """A bind of a Person into a GAS.
    Each GAS member specifies which Roles he is available for.
    This way, every time there is a need to assign one or more GAS Members to a given Role,
    there is already a group of people to choose from. 
    
    """

    person = models.ForeignKey(Person)
    gas = models.ForeignKey(GAS)
    identifier = models.CharField(_("Card number"), max_length=10, null=True, blank=True, help_text=_("Insert your Card Number"))	
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members_available")
    roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members")
    account = models.ForeignKey(Account)

    history = HistoricalRecords()

    def __unicode__(self):
        #return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}
        #See ticket #54
        return _("%(identifier)s %(person)s") % {'person' : self.person, 'identifier': self.identifier}
    
    def setup_roles(self):
        # automatically add a new GASMember to the `GAS_MEMBER` Role
        user = self.person.user
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
       
    def save(self):
    #    self.first_name = self.name
    #    self.last_name = self.last_name
        super(GASMember, self).save()         
   
    class Meta:
        app_label = 'gas'

class GASSupplierSolidalPact(PermissionResource, models.Model):
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
    
    history = HistoricalRecords()

    #if GAS's configuration use only one 
    #default withdrawal time
    withdrawal_day = models.DateField(auto_now=False, null=True, help_text=_("a week day"))
    #defaultfavorite withdrawal time
    withdrawal_time = models.TimeField(auto_now=False, null=True, help_text=_("an hour and minutes"))    
    #default withdrawal Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', related_name="default_Withdrawal")

    account = models.ForeignKey(Account)

    pds_available_for = models.CharField(max_length=50, choices=AVAILABLE_TYPE, blank=True, help_text=_("producer is available for: visit, inspection, examination, farm holidays, refreshment, feeding ...")) 

    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this GAS/Supplier pair
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    class Meta:
        app_label = 'gas'
     
    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return "" 
