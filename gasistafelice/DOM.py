ATTIBUTI PATTO SOLIDALE AGGIUNTI DA DOMINIQUE E DA VALUTARE...
"pds_" should be avoided. 

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

    pds_other_info = models.TextField(blank=True, help_text=_("other information from the manufacturer")) 
    pds_farm_holidays_name =  models.CharField(max_length=100, blank=True)
    pds_aggreement = models.ManyToManyField(PDSAgreement, help_text=_("producer declarative on honor"), null=True)
    pds_attached_documents = models.ManyToManyField(Documents, help_text=_("producer declarative on honor"), null=True)
    
    #COMMENT fero: following is insteresting, but 
    #it MUST be ManyToManyField or at least not AVAILABLE_TYPE choices
    supplier_available_for = models.CharField(max_length=50, choices=AVAILABLE_TYPE, blank=True, help_text=_("producer is available for: visit, inspection, examination, farm holidays, refreshment, feeding ...")) 

#TODO: put in base and import
class Documents(AbstractClass):
    """
    General document that refers to a special entity
    """
    DOC_TYPE = (
        ('01', 'GAS'),
        ('02', 'SUPPLIER'),
        ('03', 'PRODUCT'),
        ('04', 'MEMBER'),
        ('05', 'PDS'),
        ('06', 'ORDER'),
    )
    name = models.CharField(max_length=300, help_text=_("title and brief description"))
    type_doc = models.CharField(max_length=1, choices=DOC_TYPE)
    #TODO: how to access to a volatile foreign key 
    parent_class_id = models.AutoField(primary_key=True)
    file_doc = models.FileField(upload_to='docs/%Y/%m/%d')
    date = models.DateField()
     
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


