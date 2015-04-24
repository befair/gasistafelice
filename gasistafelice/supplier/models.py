"""These models include information about Products, Suppliers, Producers.

These are fundamental DES data to rely on. They represent market offering.

Models here rely on base model classes.

Definition: `Vocabolario - Fornitori <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#Fornitori>`__ (ITA only)
"""

from django.db import models, transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save

#WAS: from history.models import HistoricalRecords

from flexi_auth.utils import register_parametric_role
from flexi_auth.models import ParamRole
from flexi_auth.exceptions import WrongPermissionCheck

from simple_accounting.models import economic_subject, AccountingDescriptor, LedgerEntry, account_type

from gasistafelice.gf_exceptions import NoSenseException
from gasistafelice.lib import ClassProperty, unordered_uniq
from gasistafelice.lib.fields.models import CurrencyField, PrettyDecimalField
from gasistafelice.lib.fields import display

from gasistafelice.base.const import SUPPLIER_FLAVOUR_LIST, ALWAYS_AVAILABLE
from gasistafelice.base.utils import get_resource_icon_path
from gasistafelice.base.models import PermissionResource, Person, Place, Contact
from gasistafelice.des.models import DES, Siteattr

from gasistafelice.consts import SUPPLIER_REFERRER
from gasistafelice.supplier.accounting import SupplierAccountingProxy
from gasistafelice.gas import signals

from gasistafelice.base import const

from decimal import Decimal
import logging, reversion
log = logging.getLogger(__name__)

@economic_subject
class Supplier(models.Model, PermissionResource):
    """An actor having a stock of Products for sale to the DES."""

    name = models.CharField(max_length=128, verbose_name=_("name")) 
    seat = models.ForeignKey(Place, null=True, blank=True, verbose_name=_("seat"))
    vat_number = models.CharField(max_length=128, unique=True, null=True, blank=True, verbose_name=_("VAT number")) #TODO: perhaps a custom field needed here ? (for validation purposes)
    ssn = models.CharField(max_length=128, unique=True, null=True, blank=True, verbose_name=_("Social Security Number")) #TODO: perhaps a custom field needed here ? (for validation purposes)
    website = models.URLField(verify_exists=True, blank=True, verbose_name=_("web site"))
    agent_set = models.ManyToManyField(Person, through="SupplierAgent")
    frontman = models.ForeignKey(Person, null=True, related_name="supplier_frontman_set")
    flavour = models.CharField(max_length=128, choices=SUPPLIER_FLAVOUR_LIST, default=SUPPLIER_FLAVOUR_LIST[0][0], verbose_name=_("flavour"))
    n_employers = models.PositiveIntegerField(default=None, null=True, blank=True, verbose_name=_("amount of employers"))
    certifications = models.ManyToManyField('Certification', null=True, blank=True, verbose_name = _('certifications'))
    logo = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True, verbose_name=_("logo"))
    contact_set = models.ManyToManyField(Contact, null=True, blank=True)
    iban = models.CharField(blank=True, max_length=64, verbose_name=_("IBAN"))
    description = models.TextField(blank=True, default='', verbose_name=_("description"))

    accounting =  AccountingDescriptor(SupplierAccountingProxy)
    #WAS: history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ('name',)

    def __unicode__(self):
        #DOMTHU: rawfromiso = iso8859string.encode('iso-8859-1')
        #DOMTHU: properUTF8string = unicode(rawfromiso, 'utf-8')
        #DOMTHU: rv = unicode(self.name, 'utf-8')
        rv = self.name
        #if settings.DEBUG:
        #    rv += u" [%s]" % self.pk
        return rv

    @property
    def subject_name(self):
        if self.frontman:
            return self.frontman.report_name
        else:
            return ugettext("frontman: unset")

    @property
    def report_name(self):
        return "%s %s" % (self.name, self.subject_name)

    def setup_roles(self):
        # register a new `SUPPLIER_REFERRER` Role for this Supplier
        register_parametric_role(name=SUPPLIER_REFERRER, supplier=self) 
    
    def setup_accounting(self):
        """Accounting hieararchy for Supplier.

        #SUPPLIER
        . ROOT (/)
        |----------- wallet [A]
        +----------- incomes [P,I]+
        |                +--- gas [P, I] +
        |                        +--- <UID gas #1>  [P, I]
        |                        | ..
        |                        +--- <UID gas #n>  [P, I]
        |                +--- TODO: Other (Bonus? Subvention? Investment?)
        +----------- expenses [P,E]+
                        +--- TODO: Other (Correction?, Donation?, )
        """

        self.subject.init_accounting_system()
        system = self.accounting.system

        # a generic asset-type account (a sort of "virtual wallet")
        system.get_or_create_account(
            parent_path='/', name='wallet', kind=account_type.asset
        )
        # a placeholder for organizing transactions representing GAS payments
        system.get_or_create_account(
            parent_path='/incomes', name='gas', kind=account_type.income, is_placeholder=True
        )

    @property
    def uid(self):
        """
        A unique ID (an ASCII string) for ``Supplier`` model instances.
        """
        # in a real word scenario, UIDs should be generated by a more robust algorithm
        return self.urn.replace('/','-')
    
    @property
    def icon(self):
        return self.logo or super(Supplier, self).icon

    #-- Contacts --#

    @property
    def contacts(self):
        cs = self.contact_set.all()
        if not cs.count():
            cs = Contact.objects.filter(person__in=self.info_people)
        return cs

    #-- Resource API --#

    @property
    def des(self):
        return Siteattr.get_site()

    @property
    def parent(self):
        return self.des

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.pk)

    @property
    def supplier(self):
        return self

    @property
    def tech_referrers(self):
        """GAS tech referrers are also Supplier tech referrers"""
        rv = User.objects.none()
        for p in self.pacts:
            rv |= p.gas.tech_referrers
        return rv

    #FUTURE TODO LF: in 1.x we SHOULD evaluate to deprecate "referrers" properties for a resource 
    @property
    def referrers(self):
        """All User linked as platform operators for this resource.

        User who have role SUPPLIER_REFERRER."""

        # retrieve 'Supplier Referrer' parametric role for this supplier
        pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=self)
        # retrieve all Users having this role
        return pr.get_users() | self.tech_referrers

    @property
    def supplier_referrers(self):
        """
        Return all users being supplier referrers for this Supplier for all pacts it have
        """
        rv = User.objects.none()
        for p in self.pacts:
            rv |= p.gas.supplier_referrers
        return rv

    @property
    def supplier_referrers_people(self):
        """
        Return all users being supplier referrers for this Supplier for all pacts it have
        """
        prs = Person.objects.none()
        for p in self.pacts:
            prs |= p.gas.supplier_referrers_people
        return prs

    @property
    def info_people(self):
        """Return Person that can give info on this resource QuerySet."""
        return self.agent_set.all()

    @property
    def persons(self):
        """Return evryone (Person) related to this resource."""
        qs = self.info_people | self.referrers_people
        return qs.distinct()

    @property
    def users(self):
        """All User linked as platform operators for this resource.

        User who have role SUPPLIER_REFERRER."""

        # retrieve 'Supplier Referrer' parametric role for this supplier
        pr = ParamRole.get_role(SUPPLIER_REFERRER, supplier=self)
        # retrieve all Users having this role
        return pr.get_users() 

        return self.supplier_referrers

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def tot_stocks(self):
        """count All stocks _supplied_ by this supplier"""
        tot = 0
        if self.stocks:
            tot = self.stocks.count()
        return tot

    @property
    def pacts(self):
        return self.pact_set.all().order_by('gas')

    @property
    def tot_pacts(self):
        """count All pacts _supplied_ by this supplier"""
        tot = 0
        if self.pacts:
            tot = self.pacts.count()
        return tot

    @property
    def pact(self):
        raise NoSenseException("calling supplier.pact is a no-sense. Supplier is related to more than one pact")

    @property
    def orders(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def order(self):
        raise NotImplementedError("calling supplier.order is a no-sense. Supplier is related to more than one order")

    @property
    def gas_list(self):
        from gasistafelice.gas.models.base import GAS
        return GAS.objects.filter(pact_set__in=self.pacts)

    @property
    def gas(self):
        #raise NotImplementedError("calling supplier.gas is a no-sense. Supplier is related to more than one gas")
        #Use in OpenOrderForm
        #TODO: if none the form must retrieve the gas related user logged in. What happend if superuser is the logged in?
        return None

    @property
    def products(self):
        """All products _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all products __produced__ by this supplier
        return Product.objects.filter(stock_set__in=self.stocks).distinct()

    @property
    def categories(self):
        """All categories _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all categories __produced__ by this supplier
        return ProductCategory.objects.filter(product_set__in=self.products).distinct()

    @property
    def city(self):
        return self.seat.city

    @property
    def address(self):
        return self.seat

    @property
    def certifications_list(self):
        #Value symbol, name and description
        #TODO: add PRIVATE
        return ", ".join(unordered_uniq(map(lambda x: x[0], self.certifications.values_list('description'))))

    @property
    def is_private(self):
        x = self.certifications.filter(symbol=const.PRIVATE)
        if x and x.count() > 0:
            return True
        return False

    #-------------- Authorization API ---------------#

    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        """Who can create a new supplier?
        
        In general:
            * DES administrators
            * referrers and administrators of every GAS in the DES
        In depth we have to switch among multiple contexts.

        If we are checking for a "unusual key" (not in ctx_keys_to_check),
        just return False, do not raise an exception.
        """

        allowed_users = User.objects.none()
        ctx_keys_to_check = set(('gas', 'site'))
        ctx_keys = context.keys()

        if len(ctx_keys) > 1:
            raise WrongPermissionCheck('CREATE [only one key supported for context]', cls, context)

        k = ctx_keys[0]

        if k not in ctx_keys_to_check:
            # No user is allowed, just return False 
            # (user is not in User empty querySet)
            # Do not raise an exception
            pass

        # Switch among possible different contexts
        elif k == 'site':
            des = context[k]
            allowed_users = des.gas_tech_referrers | des.gas_supplier_referrers

        elif k == 'gas':
            gas = context[k]
            allowed_users = gas.tech_referrers | gas.supplier_referrers

        return user in allowed_users
 
    # Row-level EDIT permission
    def can_edit(self, user, context=None):
        # Who can edit details of a Supplier in a DES ?
        # * DES administrators
        # * referrers for that supplier        

        #WAS: * gas supplier_referrers for that supplier
        #NOTE LF: to update supplier info and stocks the user must have at least
        #NOTE LF: SUPPLIER_REFERRER role GAS_REFERRER_SUPPLIER is not enough

        allowed_users = self.des.admins | self.referrers 
        #WAS: allowed_users |= self.supplier_referrers
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can remove a supplier from a DES ?
        # * DES administrators
        allowed_users = self.des.admins
        return user in allowed_users 
    
    #-----------------------------------------------#       

    def clean(self):
        self.name = self.name.strip()
        self.flavour = self.flavour.strip()

        if self.flavour not in map(lambda x: x[0], SUPPLIER_FLAVOUR_LIST):
            raise ValidationError(
                _("The specified flavour is not valid. Valid choices are %(choices)s" % { 
                    'supplier' : self, 
                    'choiches' : SUPPLIER_FLAVOUR_LIST
                }
            ))

        if not self.vat_number:
            self.vat_number = None
        if not self.ssn:
            self.ssn = None
    
        return super(Supplier, self).clean()

    def setup_data(self):
        # Needed to be called by fixture import
        try:
            self.config
        except SupplierConfig.DoesNotExist:
            self.config = SupplierConfig.objects.create(supplier=self)

    display_fields = (
        display.Resource(name="frontman", verbose_name=_("Frontman")),
        seat, vat_number, website, flavour, 
        display.ResourceList(name="info_people", verbose_name=_("Contacts")),
        display.ResourceList(name="referrers_people", verbose_name=_("Platform referrers")),
        display.ResourceList(name="pacts", verbose_name=_("Pacts")),
    )
    #COMMENT domthu: i don't understand where referrers_people is defined?
    #COMMENT fero: you are tired :) they are in the Resource super class :)

    #--------------------------#

    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        all_sup_trx = LedgerEntry.objects.none()   #set()
        for pact in self.pacts:
            all_sup_trx |= pact.economic_movements
        return all_sup_trx

    @property
    def balance(self):
        """Accounting sold for this supplier"""
        acc_tot = self.accounting.system['/wallet'].balance
        return acc_tot

#register to revisions
if not reversion.is_registered(Supplier):
    reversion.register(Supplier)

#------------------------------------------------------------------------------


class SupplierConfig(models.Model):
    """
    Encapsulate here supplier settings and configuration facilities
    """

    # Link to parent class
    supplier = models.OneToOneField(Supplier, related_name="config")

    products_made_by_set = models.ManyToManyField(Supplier, verbose_name=_("products made by"), help_text=_("Select here producers of products you sell. YOU will be always enabled in this list"))

    receive_order_via_email_on_finalize = models.BooleanField(verbose_name=_("receive order via email on finalize"), default=True, help_text=_("Check this option if you want to let the GAS be able to send order via mail on finalize"))

    use_custom_categories = models.BooleanField(verbose_name=_("use custom categories"), default=False, help_text=_("Check this option if you use your own categories"))

    def setup_data(self):

        if self.supplier not in self.products_made_by_set.all():
           self.products_made_by_set.add(self.supplier)


class SupplierAgent(models.Model):
    """Relation between a `Supplier` and a `Person`.

    If you need information on the Supplier, ask this person.
    This is not necessarily a user in the system. You can consider it just as a contact.
    """

    supplier = models.ForeignKey(Supplier)
    person = models.ForeignKey(Person)
    job_title = models.CharField(max_length=256, blank=True)
    job_description = models.TextField(blank=True)

    #WAS: history = HistoricalRecords()

    class Meta:
        verbose_name = _('supplier agent')
        verbose_name_plural = _('supplier agents')

    @property
    def parent(self):
        return self.supplier

    def clean(self):
        self.job_title = self.job_title.strip()
        self.job_description = self.job_description.strip()
#        if self.supplier.agent_set.filter(is_referrer).count() > 1:
#            raise ValidationError(_("There can be only one referrer for each supplier"))
        return super(SupplierAgent, self).clean()

# COMMENT fero: this should be related to EDIT and CREATE permissions for related Supplier object
#    #-------------- Authorization API ---------------#
#    
#    # Table-level CREATE permission    
#    @classmethod
#    def can_create(cls, user, context):
#        # Who can add a new referrer for an existing supplier in a DES ?
#        # * DES administrators
#        # * referrers and administrators of every GAS in the DES
#        try:
#            des = context['site']
#            all_gas_referrers = set()
#            #TOERASE: new  gas.referrers returns also tech_referrers. Answer to question: who is GAS operator in this platform?
#            #TOERASE: all_gas_referrers_tech = set()
#            for gas in des.gas_list:
#                all_gas_referrers = all_gas_referrers | gas.referrers
#                #TOERASE all_gas_referrers_tech = all_gas_referrers_tech | gas.tech_referrers
#            allowed_users = des.admins | all_gas_referrers #TOERASE | all_gas_referrers_tech 
#            return user in allowed_users
#        except KeyError:
#            raise WrongPermissionCheck('CREATE', cls, context)
#        
#    # Row-level EDIT permission
#    def can_edit(self, user, context):
#        # Who can edit details of a supplier referrer ?
#        # * DES administrators
#        # * the referrer itself
#        allowed_users = set(self.supplier.des.admins) | set([self.person.user]) 
#        return user in allowed_users 
#    
#    # Row-level DELETE permission
#    def can_delete(self, user, context):
#        # Who can delete a supplier referrer ?
#        # * DES administrators
#        # * other referrers for that supplier  
#        allowed_users = self.supplier.des.admins | self.supplier.referrers
#        return user in allowed_users 

#register to revisions
if not reversion.is_registered(SupplierAgent):
    reversion.register(SupplierAgent)

class Certification(models.Model, PermissionResource):

    name = models.CharField(max_length=128, unique=True,verbose_name=_('name'))
    symbol = models.CharField(max_length=5, unique=True, verbose_name=_('symbol'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    #WAS: history = HistoricalRecords()

    def __unicode__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip()
        self.symbol = self.symbol.strip()
        self.description = self.description.strip()
        return super(Certification, self).clean()

    class Meta:
        verbose_name = _("certification")
        verbose_name_plural = _("certifications")
        ordering = ["name"]

    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new certification ?
        # * DES administrators
        try:            
            allowed_users = DES.admins_all()
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing certification ?
        # * DES administrators    
        allowed_users = DES.admins_all()    
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing certification ?
        # * DES administrators
        allowed_users = DES.admins_all()
        return user in allowed_users     
        
    #-----------------------------------------------#

#register to revisions
if not reversion.is_registered(Certification):
    reversion.register(Certification)

class ProductCategory(models.Model, PermissionResource):

    # The name is in the form MAINCATEGORY::SUBCATEGORY
    # accept arbitrary sublevels

    name = models.CharField(max_length=128, unique=True, blank=False,verbose_name=_('name'))
    description = models.TextField(blank=True,verbose_name=_('description'))
    image = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True,verbose_name=_('image'))

    #WAS: history = HistoricalRecords()

    class Meta:
        verbose_name=_('Product category')
        verbose_name_plural = _("Product categories")
        ordering = ('name',)

    def __unicode__(self):
        return self.name
    
    @property
    def icon(self):
        return self.image or super(ProductCategory, self).icon

    def delete(self, *args, **kw):
        if self.name == settings.DEFAULT_CATEGORY_CATCHALL:
            raise ValueError(_("Cannot delete default category %s") % settings.DEFAULT_CATEGORY_CATCHALL)

        return super(ProductCategory, self).delete(*args, **kW)

    def save(self, *args, **kw):

        if self.name == settings.DEFAULT_CATEGORY_CATCHALL:
            raise ValueError(_("Cannot change default category, nor create a new one with the same name"))

        super(ProductCategory, self).save(*args, **kw)

    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new category for products ?
        # * DES administrators
        try:  
            allowed_users = DES.admins_all()          
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing category ?
        # * DES administrators  
        allowed_users = DES.admins_all()       
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing category ?
        # * DES administrators
        allowed_users = DES.admins_all()
        return user in allowed_users

    #-----------------------------------------------#

    @property
    def categories(self):
        return ProductCategory.objects.filter(pk=self.pk)

#register to revisions
if not reversion.is_registered(ProductCategory):
    reversion.register(ProductCategory)

class ProductMU(models.Model, PermissionResource):
    #TODO: rename it to MU and place it in base
    """Measurement unit for a Product.

    A measure unit is recognized as a standard. So it is provided 
    as a fixture "as is" and can be changed only by DES admins.

    If a measure unit for a Product is not specified, software will 
    not able to perform conversions, thus cannot compute price-per-liter,
    or price-per-kilo. 
    
    Implemented as a separated entity like GasDotto software. 
    Kudos to Roberto `madbob` Guido. 
    Then we evolved in decoupling Measure Unit from Product Unit.
    
    # examples: gr, Kg, Lt, m
    """
    
    name = models.CharField(max_length=32, unique=True)
    symbol = models.CharField(max_length=5, unique=True)

    #WAS: history = HistoricalRecords()

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name=_("measure unit")
        verbose_name_plural=_("measure units")
        ordering = ('name',)
    
        #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new unit of measure for products ?
        # * DES administrators
        try:            
            allowed_users = DES.admins_all()
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing unit of measure for products ?
        # * DES administrators         
        allowed_users = DES.admins_all()
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing unit of measure for products ?
        # * DES administrators
        allowed_users = DES.admins_all()
        return user in allowed_users

    #-----------------------------------------------#

#register to revisions
if not reversion.is_registered(ProductMU):
    reversion.register(ProductMU)

class ProductPU(models.Model, PermissionResource):
    """Product unit for a Product.

    Represents how the product is sold.
    Limit ProdutPU creation and update to DES admins 
    and GAS_REFERRER_TECHs TODO TO BE DONE: seldon
    If this is not enough, we could evaluate another policy that
    involves SUPPLIER_REFERRERs.

    examples: box, slice, bottle, tanks
    it can be also the same as a measure unit.
    
    """

    name = models.CharField(max_length=32, unique=True)
    symbol = models.CharField(max_length=5, unique=True)
    description = models.TextField(blank=True)

    #WAS: history = HistoricalRecords()

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name=_("product unit")
        verbose_name_plural=_("product units")
        ordering = ('name',)
    
        #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new unit of measure for products ?
        # * DES administrators
        try:            
            allowed_users = DES.admins_all()
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing unit of measure for products ?
        # * DES administrators         
        allowed_users = DES.admins_all()
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing unit of measure for products ?
        # * DES administrators
        allowed_users = DES.admins_all()
        return user in allowed_users

#register to revisions
if not reversion.is_registered(ProductPU):
    reversion.register(ProductPU)

#------------------------------------------------------------------------------

class UnitsConversion(models.Model):
    """TODO: 
    Conversion between product units and measure units.

    TOCHANGE: 
    - src = ProductPU. ProductPU should include also grams, kilo, liters, etc.
    TOADD:
    - is_parent_conversion boolean as suggested by Dominique: there will be 
    ONE AND ONLY ONE is_parent_conversion == True for each different ProductPU.
    This flag states that this is the conversion to be called when display report
    """

    src = models.ForeignKey(ProductMU, verbose_name=_("source"), related_name="src_conversion_set")
    dst = models.ForeignKey(ProductMU, verbose_name=_("destination"), related_name="dst_conversion_set")
    amount = PrettyDecimalField(max_digits=10, decimal_places=4, verbose_name=_("amount"), default=1)

    def __unicode__(self):
        return _(u"%(src)s to %(dst)s") % {'src': self.src, 'dst':self.dst}

    class Meta:
        verbose_name = _("units conversion")
        verbose_name_plural = _("units conversions")
        ordering = ('src','dst', 'amount')
        unique_together = (('src','dst'),)


#------------------------------------------------------------------------------

def category_catchall():
    return ProductCategory.objects.get(name=settings.DEFAULT_CATEGORY_CATCHALL)

class Product(models.Model, PermissionResource):

    MU_SEPARATOR   = _("MU_SEP")
    PROD_SEPARATOR = _("PROD_SEP")

    # Some producers don't have product codification. 
    # That's why code could be blank AND null. See save() method
    code = models.CharField(max_length=128, unique=True, blank=True, null=True, 
                verbose_name=_('code'), 
                help_text=_("Identification provided by the producer")
    )

    producer = models.ForeignKey(Supplier, related_name="produced_product_set", 
                verbose_name = _("producer")
    )

    # Resource API
    category = models.ForeignKey(ProductCategory, blank=True, 
                related_name="product_set", verbose_name = _("category"), 
                default=category_catchall
    )

    # Measure unit, it can be null in order to make it easier to define 
    # a new product. If a user specifies a `pu` which is also a `mu`,
    # the software assigns:
    # * `instance.muppu` = 1
    # * `instance.mu` = `instance.pu`
    # thus avoiding NULL values for `mu` itself
    # See `ProductMU` doc for more details
    # TODO: mu cannot be NULL
    # TODO: if instance.mu == instance.pu --> muppu == 1
    # TODO: user interaction. User choose PU --> autocomplete muppu and mu
    mu = models.ForeignKey(ProductMU, null=True, verbose_name=_("measure unit"), blank=True)

    # Product unit: how is sell this product:
    # box, tanks, bottles, or even a measure unit
    # This must be specified.
    pu = models.ForeignKey(ProductPU, verbose_name=_("product unit"))

    # See help text
    # Can be null when no measure is specified and pu is not a measure
    muppu = PrettyDecimalField(verbose_name=_('measure unit per product unit'), 
                decimal_places=2, max_digits=6, default=Decimal("1.00"),
                help_text=_("How many measure units fit in your product unit?"),
                null=True
    )
    muppu_is_variable = models.BooleanField(verbose_name=_("variable volume"), default=False,
                help_text=_("Check this if measure units per product unit is not exact")
    )

    vat_percent = models.DecimalField(max_digits=3, decimal_places=2, 
                default=Decimal("0.21"), verbose_name=_('vat percent')
    )

    name = models.CharField(max_length=128, verbose_name = _("name"))
    description = models.TextField(blank=True, verbose_name = _("description"))

    deleted = models.BooleanField(default=False,verbose_name=_('deleted'))

    #WAS: history = HistoricalRecords()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('name',)

    def __unicode__(self):
        rv = u" %s " % (self.name)
        if self.mu:
            rv += u"(%(symb)s %(mu_sep)s %(muppu)s%(mu)s" % {
                'symb' : self.pu.symbol,
                'mu_sep' : Product.MU_SEPARATOR,
                'muppu'  : self.muppu,
                'mu'     : self.mu.symbol,
            }
        else:
            #In this case and if the user entered muppu we should interpret 
            #that the muppu is referenced to the mu and not the pu
            #COMMENT: domthu May be we need to limit this case only for "measure unit"
            if self.muppu and self.muppu != 1:
                rv += u"(%(muppu)s %(symb)s" % {
                    'symb' : self.pu.symbol,
                    'muppu'  : self.muppu
                }
            else:
                rv += u"(%s" % (self.pu.symbol)
        rv += ")"
        return rv

    def clean(self):

        # Set default DES category for a product
        if not self.category:
            self.category = category_catchall()

        if self.muppu == 0:
            self.muppu = None

        return super(Product, self).clean()
        
    @property
    def uuid(self):
        raise NotImplementedError("""UUID stuff MUST be developed as external app: 
it has to take care of UUIDs for every resource of the platform. To be effective it
MUST interact with a global UUIDs registry on the Internet. It is useful only if
the UUID is unique in the world. Annotated as "future todo" see
http://www.jagom.org/trac/reesgas/ticket/157
.
""")

    @property
    def referrers(self):
        return self.producer.referrers
  
    def save(self, *args, **kw):

        created = False
        if not self.pk:
            created = True
        
        return super(Product, self).save(*args, **kw)

        if created:
            self.config = SupplierConfig.objects.create(supplier=self)

    #-- Resource API --#

    @property
    def products(self):
        return Product.objects.filter(pk=self.pk)

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def categories(self):
        return ProductCategory.objects.filter(product_set__in=[self])

    @property
    def suppliers(self):
        return Supplier.objects.filter(stock_set__in=self.stocks)

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(stock_set__in=self.stocks)

    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new product to a supplier catalog ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a product in a supplier catalog ?
        #KO by fero * referrers for that supplier
        #KO by fero: allowed_users = self.supplier.referrers
        #KO by fero: return user in allowed_users 
        #COMMENT fero: is it right to go like this?!?
        # * anyone can edit supplier
        return self.producer.can_edit(user)
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a product from a supplier catalog ?
        #KO by fero * referrers for that supplier
        #KO by fero: allowed_users = self.supplier.referrers
        #KO by fero: return user in allowed_users 
        #COMMENT fero: is it right to go like this?!?
        # * anyone can edit supplier
        return self.producer.can_edit(user)
    
#register to revisions
if not reversion.is_registered(Product):
    reversion.register(Product)
    #-----------------------------------------------#

class SupplierStock(models.Model, PermissionResource):
    """A Product that a Supplier offers in the DES marketplace.
        
       Includes price, order constraints and availability information.

    # TODO UNITTEST
    >> from supplier.models import *
    >> ss = SupplierStock.objects.get(pk=1)
    >> isinstance(ss, SupplierStock)
    True
    >> ss.has_changed_availability
    False
    >> ss.amount_available = ss.amount_available + 1
    >> ss.has_changed_availability
    True

    """


    # Resource API
    supplier = models.ForeignKey(Supplier, related_name="stock_set", verbose_name = _('supplier'))
    # Resource API
    product = models.ForeignKey(Product, related_name="stock_set", verbose_name = _('product'))

    # Custom category defined by Supplier
    supplier_category = models.ForeignKey("SupplierProductCategory", null=True, blank=True, verbose_name = _('supplier category'))
    image = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True, verbose_name = _('image'))

    price = CurrencyField(verbose_name=_("price"))

    code = models.CharField(verbose_name=_("code"), max_length=128, null=True, blank=True, help_text=_("Product supplier identifier"))
    amount_available = models.PositiveIntegerField(verbose_name=_("availability"), default=ALWAYS_AVAILABLE)

    ## constraints posed by the Supplier on orders issued by *every* GAS
    # minimum amount of Product units a GAS can order 
    units_minimum_amount = models.PositiveIntegerField(default=1, verbose_name = _('units minimum amount'))

    # increment step (in Product units) for amounts exceeding minimum; 
    # useful when a Product ships in packages containing multiple units.
    units_per_box = PrettyDecimalField(verbose_name=_("units per box"), 
                        default=1, max_digits=5, decimal_places=2
    )

    ## constraints posed by the Supplier on orders issued by *every* GASMember
    ## they act as default when creating a GASSupplierSolidalPact
    # minimum amount of Product units a GASMember can order 
    detail_minimum_amount = PrettyDecimalField(null=True, blank=True, 
                        default=1, verbose_name = _('detail minimum amount'),
                        max_digits=5, decimal_places=2
    )

    # increment step (in Product units) for amounts exceeding minimum; 
    # useful when a Product has a fixed step of increment
    detail_step = PrettyDecimalField(null=True, blank=True, 
                        max_digits=5, decimal_places=2,
                        verbose_name=_("detail step"), default=1
    )

    # How the Product will be delivered
    delivery_notes = models.TextField(blank=True, default='', verbose_name = _('delivery notes'))

    deleted = models.BooleanField(default=False,verbose_name=_('deleted'))

    #WAS: history = HistoricalRecords()

    class Meta:
        verbose_name = _('supplier stock')
        verbose_name_plural = _('supplier stocks')
        ordering = ('supplier_category__sorting', 'product__category')
        #Fixtures do not work: to be checked and then re-enabled TODO
        #unique_together = (('code', 'supplier'),)

    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "stock"

    def __init__(self, *args, **kw):
        super(SupplierStock, self).__init__(*args, **kw)

    def __unicode__(self):
        return unicode(self.product)
#        return u"%(detail_step)s %(product)s" % {
#            'detail_step' : self.detail_step,
#            'product': self.product,
#        }

    @property
    def parent(self):
        return self.supplier

#    @property
#    def description(self):
#        #Required for editing
#        return self.product.description

    @property
    def net_price(self):
        return self.price/(1 + self.product.vat_percent)

    @property
    def umprice(self):
        try:
            return self.price/self.product.muppu
        except TypeError as e:
            # muppu can be None -> see doc related to field
            return None
        except ZeroDivisionError as e:
            # ERROR! muppu must not be 0 -> autofix it!
            log.error("MUPPU FOR %s IS 0, I set it to None" % self.product)
            self.product.muppu = None
            self.product.save()
            return None

    @property
    def icon(self):
        return self.image or self.category.icon

    @property
    def producer(self):
        return self.product.producer

    @property
    def category(self):
        return self.product.category

    @property
    def description(self):
        return self.product.description

    @property
    def name(self):
        return unicode(self)

    @property
    def vat_percent(self):
        return self.product.vat_percent
    @property
    def availability(self):
        return bool(self.amount_available)

    @property
    def has_changed_availability(self):
        try:
            ss = SupplierStock.objects.get(pk=self.pk)
            if not ss is None:
                return bool(self.amount_available != ss.amount_available)
            else:
                log.debug('SS.has_changed_availability cannot find pk %s ' % self.pk)
                return False
        except SupplierStock.DoesNotExist:
            return False

    @property
    def has_changed_price(self):
        try:
            ss = SupplierStock.objects.get(pk=self.pk)
            if not ss is None:
                return bool(self.price != ss.price)
            else:
                log.debug('SS.has_changed_price cannot find pk %s ' % self.pk)
                return False
        except SupplierStock.DoesNotExist:
            return False

    @transaction.commit_on_success
    def save(self, *args, **kwargs):

        # if `code` is set to an empty string, set it to `None`, instead, before saving,
        # so it's stored as NULL in the DB, avoiding integrity issues.
        if not self.code:
            self.code = None

        # CASCADING 
        if self.has_changed_availability:
            log.debug('Availability has changed for product %s' %  self.product)
            #For each GASSupplierStock (present for each GASSupplierSolidalPact) set new availability and save
            for gss in self.gasstocks:
                if (self.availability != gss.enabled):
                    log.debug("Save SingleSupplierStock product availability has changed old(%s) new(%s)" % (gss.enabled, self.availability))
                    gss.enabled = self.availability
                    gss.save()
                    if not gss.enabled:
                        signals.gasstock_product_disabled.send(sender=gss)
                    else:
                        signals.gasstock_product_enabled.send(sender=gss)
                    
            log.debug('Ended(%d)' % self.gasstocks.count())

        # CASCADING set until GASMemberOrder
        if self.has_changed_price:
            log.debug('Price has changed for product %s' %  self.product)
            for gsop in self.orderable_products:
                gsop.order_price = self.price
                gsop.save()

            for gmo in self.basket:
                if gmo.has_changed:
                    signals.gmo_price_update.send(sender=gmo)
            
        created = False
        if not self.pk:
            created = True

        super(SupplierStock, self).save(*args, **kwargs)

        #CASCADING is needed for NEW product
        #COMMENT fero: the whole machinery of updating stuff in gas models,
        #COMMENT fero: should be managed by signals in order to make supplier app
        #COMMENT fero: independent from gas app. But pay attention to fixtures import!

        if created:

            for gas in self.gas_list:
                
                # Get the pact
                pact = gas.pacts.get(supplier=self.supplier)
                enabled = self.availability and gas.config.auto_populate_products
                self.gasstock_set.create(
                    pact=pact, enabled=enabled, 
                    minimum_amount=self.detail_minimum_amount,
                    step=self.detail_step,
            )
        else:
            for gasstock in self.gasstocks:

                gasstock.minimum_amount = self.detail_minimum_amount
                gasstock.step = self.detail_step
                gasstock.save()

    #-- Resource API --#

    @property
    def gas_list(self):
        return self.supplier.gas_list

    @property
    def gasstocks(self):
        return self.gasstock_set.all()
    
    @property
    def pacts(self):
        from gasistafelice.gas.models import GASSupplierSolidalPact
        return GASSupplierSolidalPact.objects.filter(order_set__in=self.orders.open())

    @property
    def orders(self):
        from gasistafelice.gas.models import GASSupplierOrder
        return GASSupplierOrder.objects.filter(gasstock_set__in=self.gasstocks)

    @property
    def orderable_products(self):
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open(), gasstock__in=self.gasstocks)

    @property
    def ordered_products(self):
        #DOUBT: All API reguarding dynamic data such as order, ordereble product or gas member product should take workflow state as parameter. 
        #ANSWER: GASSupplierOrder manager takes care of this thing, the following should be changed to self.orders.exclude(state="open") 
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(ordered_product__order__in=self.orders)

    @property
    def basket(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(ordered_product__order__in=self.orders.open())

    @property
    def stocks(self):
        return SupplierStock.objects.filter(pk=self.pk)

    @property
    def stock(self):
        return self
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new stock to a supplier catalog ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a stock in  a supplier catalog ?
        #KO by fero * referrers for that supplier
        #KO by fero: allowed_users = self.supplier.referrers
        #KO by fero: return user in allowed_users 
        #COMMENT fero: is it right to go like this?!?
        # * anyone can edit supplier
        return self.supplier.can_edit(user)
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a stock from  a supplier catalog ?
        #KO by fero:  * referrers for that supplier
        #KO by fero: allowed_users = self.supplier.referrers
        #KO by fero: return user in allowed_users 
        #COMMENT fero: is it right to go like this?!?
        # * anyone can edit supplier
        return self.supplier.can_edit(user)
    
    #-----------------------------------------------#

    @property
    def display_price(self):
        return u"%(price)s (%(vat_name)s %(vat)s%%)" % {
            'price' : self.price,
            'vat_name' : _('VAT'),
            'vat' : self.vat_percent*100,
        }

    display_fields = (
        supplier,
        models.TextField(name="description", verbose_name=_("Description")),
        code,
        models.CharField(max_length=32, name="display_price", verbose_name=_("Price")),
        display.Resource(name="category", verbose_name=_("Category")),
        supplier_category,
        detail_minimum_amount, detail_step, 
        models.BooleanField(max_length=32, name="availability", verbose_name=_("Availability")),
    )

#register to revisions
if not reversion.is_registered(SupplierStock):
    reversion.register(SupplierStock)

class SupplierProductCategory(models.Model):
    """Let supplier to specify his own categories for products he sells.

    This is useful to know WHICH categories a supplier CAN sell,
    and so limiting the choice in product selections."""

    supplier = models.ForeignKey(Supplier)
    name = models.CharField(verbose_name=_('name'), max_length=128)
    sorting = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("supplier product category")
        verbose_name_plural = _("supplier product categories")
        ordering = ('supplier', 'sorting')

    def __unicode__(self):
        return self.name
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new supplier-specific category ?
        # * referrers for that supplier
        try:
            supplier = context['supplier']
            allowed_users = supplier.referrers
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
 
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a supplier-specific category ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a supplier-specific category ?
        # * referrers for that supplier
        allowed_users = self.supplier.referrers
        return user in allowed_users 
    
    #-----------------------------------------------#
