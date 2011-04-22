from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from permissions.models import Role
from workflows.models import Workflow
from history.models import HistoricalRecords

from gasistafelice.base.models import Resource, Person, AbstractClass, Document

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER
from gasistafelice.auth.utils import register_parametric_role 
from gasistafelice.auth.models import ParamRole

from gasistafelice.supplier.models import Supplier, Product

from gasistafelice.gas import managers

from gasistafelice.bank.models import Account, Movement

class GAS(models.Model, Resource, PermissionBase, AbstractClass):
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
    identifier = models.CharField("GAS code (3 letters)", max_length=3, null=False, blank=False, help_text=_("Insert here your GAS unique identier in the DES. For example: CAMERINO--> CAM"))	

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
    

class GASMember(models.Model, Resource, PermissionBase, AbstractClass):
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

class PDSAgreement(models.Model):
    """list of agreement with YES/NO response with optional note and date
    default values are 3: put in requirements?
     1: It recognizes and work consistently to the charter of intent of purchasing groups (organization and working conditions).
     2: It is available for visits to the company and control by the engineers of confidence of GAS
     3: Puts at the disposal of GAS certification documents provided for by the marks.
     4: Has carried out analyzes of products in date (if yes use note and date)
    """
    gas_question = models.CharField(max_length=1000)
    producer_response = models.NullBooleanField(null=True, help_text=_("producer response encharge responsability about the above question"))
    producer_note = models.CharField(max_length=200, blank=True)
    declaration_date = models.DateTimeField(auto_now_add=True)
  
class PDSProductSeasonality(models.Model):
    """Products type, variety and periodical availability"""
    #YEAR_MONTH = (
    #    ('01', 'JANUARY'),
    #    ('02', 'FEBRUARY'),
    #    ('03', 'MARCH'),
    #    ('04', 'APRIL'),
    #    ('05', 'MAY'),
    #    ('06', 'JUNE'),
    #    ('07', 'JULY'),
    #    ('08', 'AUGUST'),
    #    ('09', 'SEPTEMBER'),
    #    ('10', 'OCTOBER'),
    #    ('11', 'NOVEMBER'),
    #    ('12', 'DECEMBER'),
    #)
    product_type = models.CharField(max_length=100)
    #product_transformation = models.BooleanField(null=True, help_text=_("fresh product or human operation done on it"))
    product_transformation = models.NullBooleanField(null=True, help_text=_("fresh product or human operation done on it"))
    variety = models.CharField(max_length=100, blank=True)
    #seasonality = models.CharField(max_length=50, choices=YEAR_MONTH, null=True, blank=True)
    seasonality = models.DateField(auto_now=False, null=True, help_text=_("a month"))
    medium_available_quantity = models.CharField(max_length=100, blank=True)

class PDSMarketPlace(models.Model):
    """Town and Days of market"""
    #WEEK_DAYS = (
    #    ('01', 'MONDAY'),
    #    ('02', 'TUESDAY'),
    #    ('03', 'WEDNESDAY'),
    #    ('04', 'THURSDAY'),
    #    ('05', 'FRIDAY'),
    #    ('06', 'SATURDAY'),
    #    ('07', 'SUNDAY'),
    #)
    #DAY_HOURS = (
    #    ('01', '01'),
    #    ('02', '02'),
    #    ('03', '03'),
    #    ('04', '04'),
    #    ('05', '05'),
    #    ('06', '06'),
    #    ('07', '07'),
    #    ('08', '08'),
    #    ('09', '09'),
    #    ('10', '10'),
    #    ('11', '11'),
    #    ('12', '12'),
    #    ('13', '13'),
    #    ('14', '14'),
    #    ('15', '15'),
    #    ('16', '16'),
    #    ('17', '17'),
    #    ('18', '18'),
    #    ('19', '19'),
    #    ('20', '20'),
    #    ('21', '21'),
    #    ('22', '22'),
    #    ('23', '23'),
    #)
    #TODO: Geo location Gmap
    town = models.CharField(max_length=100)
    #day = models.CharField(max_length=50, choices=WEEK_DAYS, null=True, blank=True)
    day = models.DateField(auto_now=False, null=True, help_text=_("a week day"))
    #from_hour = models.CharField(max_length=50, choices=DAY_HOURS, null=True, blank=True)
    from_hour = models.TimeField(auto_now=False, null=True, help_text=_("an hour"))    

class GASSupplierSolidalPact(models.Model, Resource, PermissionBase):
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
   
    #if GAS's configuration use only one
    #default withdrawal time
    withdrawal_day = models.DateField(auto_now=False, null=True, help_text=_("a week day"))
    #defaultfavorite withdrawal time
    withdrawal_time = models.TimeField(auto_now=False, null=True, help_text=_("an hour and minutes"))
    #default withdrawal Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', related_name="default_Withdrawal")

    account = models.ForeignKey(Account)
    pds_presentation = models.TextField(blank=True)
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
    pds_aggreements = models.ManyToManyField(PDSAgreement, help_text=_("producer declarative on honor"), null=True)
    pds_attached_documents = models.ManyToManyField(Document, help_text=_("producer declarative on honor"), null=True)
    
    #if GAS's configuration use only one 
    #default withdrawal time
    withdrawal_day = models.DateField(auto_now=False, null=True, help_text=_("a week day"))
    #defaultfavorite withdrawal time
    withdrawal_time = models.TimeField(auto_now=False, null=True, help_text=_("an hour and minutes"))    
    #default withdrawal Where and when Withdrawal occurs
    withdrawal = models.ForeignKey('Withdrawal', related_name="default_Withdrawal")

    account = models.ForeignKey(Account)
    pds_presentation = models.TextField(blank=True)
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
    pds_aggreements = models.ManyToManyField(PDSAgreement, help_text=_("producer declarative on honor"), null=True)
    pds_attached_documents = models.ManyToManyField(Document, help_text=_("producer declarative on honor"), null=True)
    
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
        app_label = 'pds'
     
    def elabore_report(self):
        #TODO return report like pdf format. Report has to be signed-firmed by partners
        return "" 

