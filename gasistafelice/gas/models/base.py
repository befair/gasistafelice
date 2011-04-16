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
    description = models.TextField(help_text=_("Who are you? What are yours specialties?"), null=True, blank=True)
    identifier = models.CharField("GAS code (3 letters)", max_length=3, null=False, blank=False, help_text=_("Insert here your GAS unique identier in the DES. For example: CAMERINO--> CAM"))	

    workflow_default_gasmember_order = models.ForeignKey(Workflow, related_name="gasmember_order_set", null=True, blank=True)
    workflow_default_gassupplier_order = models.ForeignKey(Workflow, related_name="gassupplier_order_set", null=True, blank=True)

    suppliers = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True)

    objects = managers.GASRolesManager()
    history = HistoricalRecords()

    account = models.ForeignKey(Account)
    liquidity = models.ForeignKey(Account)

    active = models.BooleanField()
    birthday = models.DateField()
    vat =  models.CharField(max_length=11, null=True, blank=True, help_text=_("Partita IVA"))	
    fiscal_code =  models.CharField(max_length=16, null=True, blank=False, help_text=_("Codice fiscale"))	
    email_gas = models.EmailField()
    email_referrer = models.EmailField(null=True, blank=True, help_text=_("Email responsabili"))
    phone = models.CharField(max_length=50, null=True, blank=True)	
    website = models.URLField(verify_exists=True, null=True, blank=True) 
    #TODO: gallery album
    #TODO: generic class documents 
    #documents = models.ManyToManyField(Document)
    association_act = models.FileField(null=True, blank=True)
    intent_act = models.FileField(null=True, blank=True)
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
    identifier = models.CharField("Numero tessera", max_length=10, null=True, blank=True, help_text=_("Inserire cui il vostro numero di tessera"))	
    available_for_roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members_available")
    roles = models.ManyToManyField(Role, null=True, blank=True, related_name="gas_members")
    account = models.ForeignKey(Account)

    history = HistoricalRecords()

    def __unicode__(self):
        return _("%(person)s of %(gas)s GAS") % {'person' : self.person, 'gas': self.gas}

    
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

    PRODUCTS_GROWN = (
        ('CE', 'CEREAL'),
        ('VE', 'VEGETABLE'),
        ('FR', 'FRUIT'),
        ('LE', 'LEGUME'),
        ('ME', 'MEAT'),
        ('MI', 'MILK_CHEESE'),
        ('OI', 'OIL'),
        ('HO', 'HONEY'),
        ('WI', 'WINE'),
        ('CH', 'CHEESE'),
        ('NF', 'NO_FOOD'),
        ('SW', 'SERVICE'),
    )
    DISTRIBUTION_TYPE = (
        ('CO', 'IN THE COMPANY'),
        ('DD', 'DIRECT DELIVERY'),
        ('DE', 'DELIVERY BY COURIER SERVICE'),
    )
    AVAILABLE_TYPE = (
        ('VI', 'VISITE'),
        ('FH', 'FARM HOLIDAYS'),
        ('RE', 'REFRESHMENT'),
    )

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

    account = models.ForeignKey(Account)
    pds_presentaion = models.TextField(blank=True)
    pds_first_year_of_certification = models.CharField(max_length=50, blank=True)
    pds_last_year_of_certification = models.CharField(max_length=50, blank=True)
    pds_extension_cultivated = models.CharField(max_length=50, blank=True)
    pds_start_year_cultivation_with_biological_method = models.CharField(max_length=50, blank=True)
    pds_altitude_of_the_compagny = models.CharField(max_length=50, blank=True)
    pds_products_grown = models.CharField(max_length=50, choices=PRODUCTS_GROWN, blank=True) 
    pds_products_seasonability = models.ManyToManyField(PDSProductSeasonality, help_text=_("indicative products seasonality and availability"), null=True)
    pds_water_provenance = models.CharField(max_length=100, help_text=_("provenance water for irrigation"), blank=True)
    pds_manure_used = models.CharField(max_length=300, help_text=_("type of manure used"), blank=True)
    pds_manure_provenance = models.CharField(max_length=100, help_text=_("provenance manure used"), blank=True)
    pds_manure_hectare = models.CharField(max_length=300, help_text=_("quantity of manure per hectare and crops concerned the manuring"), blank=True)
    pds_fertilizer_rought = models.CharField(max_length=300, help_text=_("any other fertilizers and rough-treatment"), blank=True)
    pds_pollution_distance = models.CharField(max_length=100, help_text=_("distance from any possible sources of pollution"), blank=True)
    pds_seed_provenance = models.CharField(max_length=300, help_text=_("provenance of the seed"), blank=True)
    pds_distribution_type = models.CharField(max_length=50, choices=DISTRIBUTION_TYPE, blank=True) 
    pds_market = models.CharField(max_length=300, help_text=_("day and town of presence in biological market place"), blank=True) 
    pds_available_for = models.CharField(max_length=50, choices=AVAILABLE_TYPE, blank=True, help_text=_("producer is available for: visit, inspection, examination, farm holidays, refreshment, feeding ...")) 
    pds_farm_holidays_name =  models.CharField(max_length=100, blank=True)
    pds_other_info = models.TextField(blank=True, help_text=_("other information from the manufacturer")) 
    pds_aggreement = models.ManyToManyField(PDSAgreement, help_text=_("producer declarative on honor"), null=True)
    pds_attached_documents = models.ManyToManyField(Documents, help_text=_("producer declarative on honor"), null=True)
    
    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this GAS/Supplier pair
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
     
<<<<<<< HEAD
=======
    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return "" 

#TODO: put in base and import
class AbstractClass(models.Model):
    created_at=models.DateField(_"Created at")
    created_by=models.ForeignKey(User, db_column="created_by", related_name=_"poll_user_created_by")
    updated_at=models.DateTimeField("Updated at")
    updated_by=models.ForeignKey(User, db_column="updated_by", null=True, related_name=_"poll_user_updated_by")
>>>>>>> init GAS models configuration
    class Meta:
        app_label = 'gas'


