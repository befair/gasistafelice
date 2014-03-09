from django.db import models
from django.utils.translation import ugettext as ug, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator, MinLengthValidator


from permissions.models import Role
from workflows.models import Workflow
from workflows.utils import get_workflow
from history.models import HistoricalRecords

from flexi_auth.utils import register_parametric_role
from flexi_auth.models import ParamRole, Param, PrincipalParamRoleRelation
from flexi_auth.exceptions import WrongPermissionCheck

from simple_accounting.models import (economic_subject, Account, 
    AccountingDescriptor, LedgerEntry, account_type,
    AccountSystem
)

from gasistafelice.lib import ClassProperty
from gasistafelice.lib.fields.models import CurrencyField, PrettyDecimalField
from gasistafelice.lib.fields import display
from gasistafelice.utils import long_date

from gasistafelice.base.models import PermissionResource, Person, Place, Contact
from gasistafelice.base import const
from gasistafelice.base import utils as base_utils

from gasistafelice.gas.accounting import GasAccountingProxy

from gasistafelice.consts import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, GAS_REFERRER

from gasistafelice.supplier.models import Supplier, SupplierStock, Product, ProductCategory
from gasistafelice.gas.managers import GASMemberManager, IncludeSuspendedGASMemberManager
from gasistafelice.des.models import DES

from gasistafelice.gf_exceptions import NoSenseException, DatabaseInconsistent

from decimal import Decimal
import datetime
import logging
log = logging.getLogger(__name__)


# Some template stuff needed for template rendering
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from django.utils.encoding import smart_unicode
# End

#-------------------------------------------------------------------------------
@economic_subject
class GAS(models.Model, PermissionResource):

    """A group of people who makes some purchases together.

    Every GAS member has a Role where the basic Role is just to be a member of the GAS.
    """
    name = models.CharField(max_length=128, unique=True,verbose_name=_('name'))
    id_in_des = models.CharField(_("GAS code"), max_length=8, null=False, blank=False, unique=True, help_text=_("GAS unique identifier in the DES. Example: CAMERINO--> CAM"))
    logo = models.ImageField(upload_to=base_utils.get_resource_icon_path, null=True, blank=True)
    headquarter = models.ForeignKey(Place, related_name="gas_headquarter_set", help_text=_("main address"), null=False, blank=False,verbose_name=_('headquarter'))
    description = models.TextField(blank=True, help_text=_("Who are you? What are yours specialties?"),verbose_name=_('description'))
    membership_fee = CurrencyField(default=Decimal("0"), help_text=_("Membership fee for partecipating in this GAS"), blank=True,verbose_name=_('membership fee'))

    supplier_set = models.ManyToManyField(Supplier, through='GASSupplierSolidalPact', null=True, blank=True, help_text=_("Suppliers bound to the GAS through a solidal pact"),verbose_name=_('Suppliers'))
    
    birthday = models.DateField(null=True, blank=True, help_text=_("When this GAS is born"), verbose_name=_('birthday'))
    vat = models.CharField(max_length=11, blank=True, help_text=_("VAT number"),verbose_name=_('VAT'))
    fcc = models.CharField(max_length=16, blank=True, help_text=_("Fiscal code card"),verbose_name=_('Fiscal code card'))

    contact_set = models.ManyToManyField(Contact, null=True, blank=True,verbose_name=_('contacts'))

    # Orders email contact is the mailing-list where we can send notification about orders
    orders_email_contact = models.ForeignKey(Contact, limit_choices_to = { 'flavour' : const.EMAIL }, null=True, blank=True, related_name="gas_use_for_orders_set")

    website = models.URLField(verify_exists=True, null=True, blank=True,verbose_name=_('web site'))

    #Persons who are active in GAS and can give info about it
    activist_set = models.ManyToManyField(Person, through="GASActivist", null=True, blank=True,verbose_name=_('GAS activists'))

    association_act = models.FileField(upload_to=base_utils.get_association_act_path, null=True, blank=True, verbose_name=_("association act"))
    intent_act = models.FileField(upload_to=base_utils.get_intent_act_path, null=True, blank=True, verbose_name=_("intent act"))

    note = models.TextField(blank=True,verbose_name =_('notes'))

    # Resource API
    des = models.ForeignKey(DES,verbose_name=_('des'))

    #TODO: Notify system

    #-- Managers --#
    accounting =  AccountingDescriptor(GasAccountingProxy)
    history = HistoricalRecords()

    display_fields = (
        website, 
        models.CharField(max_length=32, name="city", verbose_name=_("City")),
        headquarter, birthday, description, 
        membership_fee, vat, fcc,
        association_act, intent_act,
        display.ResourceList(name="info_people", verbose_name=_("info people")),
        display.ResourceList(name="tech_referrers_people", verbose_name=_("tech referrers")),
        display.ResourceList(name="supplier_referrers_people", verbose_name=_("supplier referrers")),
        display.ResourceList(name="cash_referrers_people", verbose_name=_("cash referrers")),
        #TODO WAS: do not work with current django-pro-history implementation
        # display.ResourceList(verbose_name=_("created by"), name="created_by_person"),
        # display.ResourceList(verbose_name=_("last update by"), name="last_update_by_person"),
    )

    #-- Meta --#
    class Meta:
        verbose_name_plural = _('GAS')
        app_label = 'gas'
        ordering = ('-birthday',)

    #-- Overriding built-in methods --#
    def __unicode__(self):
        return self.name

    def clean(self):
        try:
            self.name = self.name.strip()
        except TypeError as e:
            raise ValidationError(ug("Name must be set"))
        try:
            self.id_in_des = self.id_in_des.strip()
        except TypeError as e:
            raise ValidationError(ug("GAS code must be set"))
        try:
            self.note = self.note.strip()
        except TypeError as e:
            pass

        try:
            assert self.headquarter
        except Place.DoesNotExist as e:
            raise ValidationError(ug("Default headquarter place must be set"))

        return super(GAS, self).clean()

    #-- Authorization API --#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new GAS in a DES ?
        # * DES administrators
        allowed_users = User.objects.none()
        try:
            des = context['site']
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)   
        return user in allowed_users
    
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing GAS ?
        # * GAS tech referrers
        # * administrators of the DES that GAS belongs to
        allowed_users =  self.tech_referrers 
        return user in allowed_users  
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing GAS from a DES ?
        # * administrators of the DES that GAS belongs to
        allowed_users = User.objects.none()
        return user in allowed_users

    def can_cash(self, user, context):
        #WAS: return user in self.cash_referrers
        #NOTE LF: this is due to role/permission pyramid: see commit on 26th of april
        return user in self.cash_referrers or \
            user in self.tech_referrers
        

    @property
    def roles(self):
        "GAS involves also roles related to pacts"""

        roles = super(GAS, self).roles
        for pact in self.pacts:
            roles |= pact.roles
        return roles

    #--------------------------#
    
    #-- Properties --#
    
    @property
    def uid(self):
        """
        A unique ID (an ASCII string) for ``GAS`` model instances.
        """
        return self.urn.replace('/','-')
    
    @property
    def icon(self):
        return self.logo or super(GAS, self).icon

    #-- Referrers API --#

    @property
    def referrers(self):
        """Returns GAS referrers which are TECH referrers."""
        return self.tech_referrers

        #TODO: can add person with GAS_REFERRER role if needed, but don't mind for it now
        #pr = ParamRole.get_role(GAS_REFERRER, gas=self)
        #return pr.get_users() | self.tech_referrers

    @property
    def info_people(self):
        return Person.objects.filter(gasactivist__in=self.activist_set.all())

    @property
    def persons(self):
        qs = Person.objects.filter(gasmember__in=self.gasmembers) | self.info_people | self.referrers_people
        return qs.distinct()

    @property
    def tech_referrers(self):
        """
        Return all users being technical referrers for this GAS.
        """
        # retrieve 'tech referrer' parametric role for this GAS
        pr = ParamRole.get_role(GAS_REFERRER_TECH, gas=self)
        # retrieve all Users having this role
        return pr.get_users()       

    @property
    def cash_referrers(self):
        """
        Return all users being accounting referrers for this GAS.
        """
        # retrieve 'cash referrer' parametric role for this GAS
        pr = ParamRole.get_role(GAS_REFERRER_CASH, gas=self)
        # retrieve all Users having this role
        return pr.get_users()  
    
    @property
    def supplier_referrers(self):
        """
        Return all users being supplier referrers for this GAS
        """
        # retrieve 'GAS supplier referrer' parametric role for all pacts of this GAS
        ctype = ContentType.objects.get_for_model(GASSupplierSolidalPact)
        params = Param.objects.filter(content_type=ctype, object_id__in=map(lambda x: x.pk, self.pacts))
        prs = ParamRole.objects.filter(param_set__in=params, role__name=GAS_REFERRER_SUPPLIER)
        # retrieve all Users having this role
        us = User.objects.none()
        for pr in prs:
            us |= pr.get_users()
        return us

    @property
    def tech_referrers_people(self):
        return Person.objects.filter(user__in=self.tech_referrers)
        
    @property
    def cash_referrers_people(self):
        return Person.objects.filter(user__in=self.cash_referrers)
        
    @property
    def supplier_referrers_people(self):
        return Person.objects.filter(user__in=self.supplier_referrers)
        
    @property
    def city(self):
        return self.headquarter.city 

    @property
    def economic_state(self):
        return u"%s - %s" % (self.balance, self.liquidity)

    #-- Contacts --#

    @property
    def contacts(self):
        cs = self.contact_set.all()
        if not cs.count():
            cs = Contact.objects.filter(person__in=self.info_people)
        return cs

    #-- Methods --#

    def setup_roles(self):
        # register a new `GAS_MEMBER` Role for this GAS
        register_parametric_role(name=GAS_MEMBER, gas=self)
        # register a new `GAS_REFERRER` Role for this GAS. This is the President of the GAS or other VIP.
        # COMMENT fero: we do not need GAS_REFERRER role now
        #register_parametric_role(name=GAS_REFERRER, gas=self)
        # register a new `GAS_REFERRER_TECH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_TECH, gas=self)
        # register a new `GAS_REFERRER_CASH` Role for this GAS
        register_parametric_role(name=GAS_REFERRER_CASH, gas=self)

    def save(self, *args, **kw):

        if not self.id_in_des:
            self.id_in_des = self.name[:3]
            while True:
                try:
                    GAS.objects.get(id_in_des=self.id_in_des)
                    self.id_in_des = self.id_in_des[:2] + chr(ord(self.id_in_des[2]) + 1)
                except: #DoesNotExist or MultipleObjectsReturned
                    break
                    
        self.id_in_des = self.id_in_des.upper()

        created = False
        if not self.pk:
            created = True

        try:
            self.des
        except DES.DoesNotExist:
            # This should never happen, but it is reasonable
            # that an installation has only one DES
            if DES.objects.count() > 1:
                raise AttributeError(ug("You have to bind GAS %s to a DES") % self.name)
            else:
                self.des = DES.objects.all()[0]

        super(GAS, self).save(*args, **kw)

        try:
            self.config
        except GASConfig.DoesNotExist:
            self.config = GASConfig.objects.create(
                gas=self, auto_populate_products=True
            )

    def setup_accounting(self):
        """ Accounting hierachy for GAS.

        . ROOT (/)
        |----------- cash [A]
        +----------- members [P,A]+
        |                +--- <UID member #1>  [A]
        |                | ..
        |                +--- <UID member #n>  [A]
        +----------- expenses [P,E]+
        |                +--- OutOfDES
        |                +--- member (correction or other)
        |                +--- suppliers [P, E] +
        |                        +--- <UID supplier #1>  [E]
        |                        | ..
        |                        +--- <UID supplier #n>  [E]
        +----------- incomes [P,I]+
        |                +--- recharges [I]
        |                +--- fees [I]
        |                +--- OutOfDES
        """

        try:
            system = self.accounting.system
        except AttributeError as e:
            self.subject.init_accounting_system()
            system = self.accounting.system

        # GAS's cash
        system.get_or_create_account(
            parent_path='/', name='cash', kind=account_type.asset
        )
        # root for GAS members' accounts
        system.get_or_create_account(
            parent_path='/', name='members', kind=account_type.asset, is_placeholder=True
        )
        # a placeholder for organizing transactions representing payments to suppliers
        system.get_or_create_account(
            parent_path='/expenses', name='suppliers', kind=account_type.expense, is_placeholder=True
        )
        #For each GASSuplierSolidalPact we expects to create the relative
        #parent_path='/expenses/suppliers/', name=''

        # recharges made by GAS members to their own account
        system.get_or_create_account(
            parent_path='/incomes', name='recharges', kind=account_type.income
        )
        # membership fees
        system.get_or_create_account(
            parent_path='/incomes', name='fees', kind=account_type.income
        )

        # incomes from out of DES
        system.get_or_create_account('/incomes', 'OutOfDES', account_type.income)

        # expenses to out of DES
        system.get_or_create_account('/expenses', 'OutOfDES', account_type.expense)

        system.get_or_create_account('/expenses', 'member', account_type.expense)
        system.get_or_create_account('/expenses', 'gas', account_type.expense)
        system.get_or_create_account('/incomes', 'member', account_type.income)

    #-- Resource API --#

    @property
    def parent(self):
        return self.des

    @property
    def gas_list(self):
        return GAS.objects.filter(pk=self.pk)

    @property
    def gas(self):
        return self

    @property
    def gasmembers(self):
        """All GASMember not suspended for this GAS"""
        gm_qs = self.gasmember_set.filter(person__user__is_active=True)
        #gm_qs = gm_qs.filter(is_active=True)

        #WAS: default ordering follows diplay name
        #WAS: gm_qs = gm_qs.order_by('person__surname', 'person__name')
        return gm_qs

    @property
    def all_gasmembers(self):
        """All GASMember (included suspended) for this GAS"""
        gm_qs = GASMember.all_objects.filter(gas=self)
        return gm_qs

    @property
    def orders(self):
        """
        Return orders bound to resource
        """

        from gasistafelice.gas.models.order import GASSupplierOrder
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def open_orders(self):
        """
        Return open orders bound to resource. 
        NOTE: this has been added for simple real_rest.ModelSerializers
        """
        return self.orders.open()

    @property
    def order(self):
        raise NoSenseException("calling gas.order is a no-sense. GAS is related to more than one order")

    @property
    def deliveries(self):
        from gasistafelice.gas.models.order import Delivery
        # The GAS deliveries appointments take from orders. Do distinct operation. 
        rv = Delivery.objects.none()
        for obj in self.orders:
            if obj.delivery: 
                rv |= obj.delivery
        return rv

    @property
    def delivery(self):
        raise NoSenseException("calling gas.delivery is a no-sense. GAS is related to more than one delivery")

    @property
    def withdrawals(self):
        from gasistafelice.gas.models.order import Withdrawal
        # The GAS withdrawal appointments. Do distinct operation.
        rv = Withdrawal.objects.none()
        for obj in self.orders:
            if obj.withdrawal: 
                rv |= obj.withdrawal
        return rv

    @property
    def withdrawal(self):
        raise NoSenseException("calling gas.withdrawal is a no-sense. GAS is related to more than one withdrawal")

    @property
    def pacts(self):
        # Return pacts bound to a GAS
        return self.pact_set.all().order_by('supplier')

    @property
    def suppliers(self):
        """Return suppliers bound to a GAS"""
        return self.supplier_set.all()

    @property
    def stocks(self):
        return SupplierStock.objects.filter(supplier__in=self.suppliers)

    @property
    def products(self):
        #TODO OPTIMIZE
        return Product.objects.filter(pk__in=[obj.product.pk for obj in self.stocks])

    @property
    def categories(self):
        """All disctinct categories for all suppliers with solidal pact with the gas"""
        return ProductCategory.objects.filter(product_set__in=self.products).distinct()

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.filter(gas=self)

    @property
    def orderable_products(self):
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open())

    @property
    def ordered_products(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(order__in=self.orders)

    @property
    def basket(self):
        from gasistafelice.gas.models import GASMemberOrder
        return GASMemberOrder.objects.filter(order__in=self.orders.open())

    #--------------------------#

    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        return self.accounting.entries()

    @property
    def balance(self):
        """Cash balance available for GAS"""
        acc_tot = self.accounting.system['/cash'].balance
        return acc_tot

    @property
    def balance_gasmembers(self):
        """Cash balance available for GASMembers of the GAS"""
        #return self.accounting.system['/members'].balance
        acc_tot = 0
        for gm in self.all_gasmembers:
            acc_tot += self.accounting.system['/members/' + gm.person.uid].balance
        return acc_tot

    @property
    def balance_suppliers(self):
        """How much money has been given to suppliers by this GAS."""
        acc_tot = 0
        for pact in self.pacts:
            acc_path = '/expenses/suppliers/' + pact.supplier.uid
            acc_tot += self.accounting.system[acc_path].balance
        return acc_tot

    @property
    def liquidity(self):
        """Accounting sold for all members of this gas.

        """
        acc_tot = 0
        for gm in self.all_gasmembers:
            acc_tot += gm.balance
        return acc_tot

    def send_email_to_gasmembers(self, subject, message, more_to=[]):

        log.debug("GAS send_email: %s" % message)

        try:
            sender = self.preferred_email_contacts[0].value
        except IndexError as e:
            msg = ug("GAS cannot send email, because no preferred email for GAS specified")
            message += '\n' + msg
            sender = settings.DEFAULT_FROM_EMAIL
            message += '\n%s --> %s' % (msg, sender)

        to = []

        for gm in self.gasmembers:
            to.append(gm.email)

        for addr in to + more_to:

            email = EmailMessage(
                subject = subject,
                body = message,
                from_email = sender,
                to = [addr]
            )

            email.send()
        return

    @property
    def insolutes(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        orders = GASSupplierOrder.objects.closed().filter(pact__gas=self) | \
            GASSupplierOrder.objects.unpaid().filter(pact__gas=self)
        return orders

#------------------------------------------------------------------------------


def get_supplier_order_default():
    return Workflow.objects.get(name="SimpleSupplierOrderDefault")

def get_gasmember_order_default():
    return Workflow.objects.get(name="GASMemberOrderDefault")

class GASConfig(models.Model):
    """
    Encapsulate here gas settings and configuration facilities
    """

    # Link to parent class
    gas = models.OneToOneField(GAS, related_name="config")

    default_workflow_gasmember_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gmow_gasconfig_set", blank=True, default=get_gasmember_order_default
    )
    default_workflow_gassupplier_order = models.ForeignKey(Workflow, editable=False, 
        related_name="gsopw_gasconfig_set", blank=True, default=get_supplier_order_default
    )

    can_change_price = models.BooleanField(default=False,
        help_text=_("GAS can change supplier products price (i.e. to hold some funds for the GAS itself)")
    )

#    show_order_by_supplier = models.BooleanField(default=True, 
#        help_text=_("GAS views open orders by supplier. If disabled, views open order by delivery appointment")
#    )

    order_show_only_next_delivery = models.BooleanField(verbose_name=_('Show only next delivery'), default=False, 
        help_text=_("GASMember can choose to filter order block among one or more orders that share the next withdrawal appointment"))
    order_show_only_one_at_a_time = models.BooleanField(
        verbose_name=_('Select only one order at a time'), default=True, 
        help_text=_("GASMember can select only one open order at a time in order block")
    )

    #TODO: see ticket #65
    default_close_day = models.CharField(
        max_length=16, blank=True, choices=const.DAY_CHOICES, 
        help_text=_("default closing order day of the week"),
        verbose_name=_('default close day')
    )
    #TODO: see ticket #65
    default_delivery_day = models.CharField(
        max_length=16, blank=True, choices=const.DAY_CHOICES, 
        help_text=_("default delivery day of the week"),
        verbose_name=_('default delivery day')
    )

    #Do not provide default for time fields because it has no sense set it to the moment of GAS configuration
    #TODO placeholder domthu: Default time to be set to 00:00
    default_close_time = models.TimeField(verbose_name=_('Default close time'), blank=True, null=True,
        help_text=_("default order closing hour and minutes")
    )
  
    default_delivery_time = models.TimeField(verbose_name=_('Default delivery day time'), blank=True, null=True,
        help_text=_("default delivery closing hour and minutes")
    )

    use_withdrawal_place = models.BooleanField(verbose_name=_('Use concept of withdrawal place'), 
        default=False,
        help_text=_("If False, GAS never use concept of withdrawal place that is the default")
    )
    can_change_withdrawal_place_on_each_order = models.BooleanField(
        verbose_name=_('can change withdrawal place on each order'), default=False, 
        help_text=_("If False, GAS uses only one withdrawal place that is the default or if not set it is the GAS headquarter")
    )

    can_change_delivery_place_on_each_order = models.BooleanField(
        verbose_name=_('can change delivery place on each order'), default=False, 
        help_text=_("If False, GAS uses only one delivery place that is the default or if not set it is the GAS headquarter")
    )

    # Do not set default to both places because we want to have the ability
    # to follow headquarter value if it changes.
    # Provide delivery place and withdrawal place properties to get the right value
    default_withdrawal_place = models.ForeignKey(Place, 
        verbose_name=_('default withdrawal place'), 
        blank=True, null=True, related_name="gas_default_withdrawal_set", 
        help_text=_("to specify if different from headquarter")
    )
    default_delivery_place = models.ForeignKey(Place, 
        verbose_name=_('default delivery place'), blank=True, null=True, 
        related_name="gas_default_delivery_set", 
        help_text=_("to specify if different from withdrawal place")
    )

    #auto_populate_products always True until Gasista Felice 2.0
    auto_populate_products = models.BooleanField(
        verbose_name=_('auto populate products'), default=True, 
        help_text=_("automatic selection of all products bound to a supplier when a relation with the GAS is activated")
    )

    use_scheduler = models.BooleanField(default=False, 
        verbose_name=_("use scheduler"), 
        help_text=_("Enable scheduler for automatic and planned operations")
    )

    gasmember_auto_confirm_order = models.BooleanField(
        verbose_name=_('GAS members orders are auto confirmed'), 
        default=True, 
        help_text=_("if checked, gasmember's orders are automatically confirmed. If not, each gasmember must confirm by himself his own orders")
    )

    # Fields for suspension management:
    is_suspended = models.BooleanField(verbose_name=_("is suspended"),
        default=False, db_index=True, 
        help_text=_("The GAS is not available (holidays, closed). The scheduler uses this flag to operate or not some automatisms")
    )

    suspend_datetime = models.DateTimeField(default=None, null=True, blank=True) # When this gas was suspended
    suspend_reason = models.TextField(blank=True, default='', db_index=False)
    suspend_auto_resume = models.DateTimeField(default=None, null=True, blank=True, db_index=True) # If not NULL and is_suspended, auto resume at specified time

    notice_days_before_order_close = models.PositiveIntegerField(
        verbose_name=_("Notice days before order close"),
        null=True, default=1, 
        help_text=_("How many days before do you want your GAS receive reminder on closing orders?"),
    )
    
    use_order_planning = models.BooleanField(default=False, 
        help_text=_("Show order planning section when creating a new order"),
        verbose_name=_("use order planning")
    )

    send_email_on_order_close = models.BooleanField(default=False, 
        help_text=_("Default value for pact option to let the system send an email to supplier and gas referrer supplier as soon as an order is closed"),
        verbose_name=_("default for pacts: send email on order close")
    )

    registration_token = models.CharField(max_length=32,
        default='', blank=True,
        validators= [ RegexValidator(
            regex='\w*\d+\w+\d*|\d*\w+\d+\w*',
            message=_('The token should be at least 5 characters, and must include a cipher'),
        ), MinLengthValidator(5)],
        verbose_name=_("Registration token"),
        help_text=_("If set, this token can be used in the registration phase by a new user to be enabled in the software as soon as he confirms its email. So it IS IMPORTANT, to not make a blind distribution of the token, to choose a token composed of letters and numbers, and to change it each 3 months or occasionally")
    )

    intergas_connection_set = models.ManyToManyField(GAS,
        verbose_name=_("possible interGAS orders with"),
        blank=True, null=True,
        help_text=_("Choose GAS that could be chosen when an interGAS order is created")
    )

    NOBODY = 'nobody'
    GAS = 'gas'
    INTERGAS = 'intergas'
    DES = 'des'
    GAS_SUPPLIERS = 'gas,suppliers'
    INTERGAS_SUPPLIERS = 'intergas,suppliers'
    DES_SUPPLIERS = 'des,suppliers'
    
    PRIVACY_CHOICES = (
        (NOBODY, _('Nobody')), 
        (GAS, _('Only to GAS members')), 
        (INTERGAS, _('To every possible intergas members')), 
        (DES, _('To DES members')), 
        (GAS_SUPPLIERS, _('GAS and suppliers')), 
        (INTERGAS_SUPPLIERS, _('To every possible intergas members and suppliers')), 
        (DES_SUPPLIERS, _('DES and suppliers')), 
    )

    privacy_phone = models.CharField(max_length=24, 
        verbose_name = _("Show gas members phone number to"),
        choices = PRIVACY_CHOICES,
        default = GAS_SUPPLIERS,
    )
    privacy_email = models.CharField(max_length=24, 
        verbose_name=_("Show gas members email address to"),
        choices = PRIVACY_CHOICES,
        default = GAS_SUPPLIERS,
    )
    privacy_cash = models.CharField(max_length=24, 
        verbose_name=_("Show gas members cash amount to"),
        choices = PRIVACY_CHOICES,
        default = GAS_SUPPLIERS,
    )


    #notice_days_after_gmo_update = models.PositiveIntegerField(
    #   null=True, default=1, help_text=_("After how many days do 
    #   you want a gasmember receive updates on his own orders?")
    #)

    history = HistoricalRecords()

    #-- Meta --#
    class Meta:
        verbose_name = _('GAS options')
        verbose_name_plural = _('GAS options')
        app_label = 'gas'

    def __unicode__(self):
        return ug('Configuration for GAS "%s"') % self.gas 

    @property
    def delivery_place(self):
        return self.default_delivery_place or self.gas.headquarter

    @property
    def withdrawal_place(self):
        return self.default_withdrawal_place or self.gas.headquarter

#----------------------------------------------------------------------------------------------------

class GASActivist(models.Model):
    """Relation between a `GAS` and a `Person`.

    If you need information on the GAS, ask to this person.
    This is not necessarily a user in the system. You can consider it just as a contact.
    """

    gas = models.ForeignKey(GAS,verbose_name=_('gas'))
    person = models.ForeignKey(Person,verbose_name=_('person'))
    info_title = models.CharField(max_length=256, blank=True)
    info_description = models.TextField(blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('GAS activist')
        verbose_name_plural = _('GAS activists')
        app_label = 'gas'

    @property
    def parent(self):
        return self.gas

#----------------------------------------------------------------------------------------------------

class GASMember(models.Model, PermissionResource):
    """A bind of a Person into a GAS.
    Each GAS member specifies which Roles he is available for.
    This way, every time there is a need to assign one or more GAS Members to a given Role,
    there is already a group of people to choose from. 
    
    """
    # Resource API
    person = models.ForeignKey(Person,verbose_name=_('person'))
    # Resource API
    gas = models.ForeignKey(GAS,verbose_name=_('gas'))

    id_in_gas = models.CharField(verbose_name=_("card number"), 
        max_length=10, blank=True, null=True, 
        help_text=_("GAS card number")
    )
    available_for_roles = models.ManyToManyField(Role, null=True, 
        blank=True, related_name="gas_member_available_set",
        verbose_name=_('available for roles')
    )
    membership_fee_payed = models.DateField(auto_now=False, 
        verbose_name=_("membership_fee_payed"), auto_now_add=False, 
        null=True, blank=True, help_text=_("When was the last the annual quote payment")
    )

    use_planned_list = models.BooleanField(default=False,verbose_name=_('use_list'))

    # Fields for suspension management:
    is_suspended = models.BooleanField(verbose_name=_('is suspended'),
        default=False, db_index=True, help_text=_("GAS member is not active now")
    )
    suspend_datetime = models.DateTimeField(default=None, null=True, blank=True) # When this pact was suspended
    suspend_reason = models.TextField(blank=True, default='', db_index=False)
    suspend_auto_resume = models.DateTimeField(default=None, null=True, blank=True, db_index=True) # If not NULL and is_suspended, auto resume at specified time

    objects = GASMemberManager()
    all_objects = IncludeSuspendedGASMemberManager()

    history = HistoricalRecords()

    display_fields = (
        display.Resource(name="gas", verbose_name=_("GAS")),
        person,
        membership_fee_payed,
        id_in_gas,
        models.CharField(max_length=32, name="city", verbose_name=_("City")),
#        models.CharField(max_length=200, name="email", verbose_name=_("Email")),
#        models.CharField(max_length=100, name="phone", verbose_name=_("Phone")),
#        models.CharField(max_length=200, name="www", verbose_name=_("Web site")),
#        models.CharField(max_length=100, name="fax", verbose_name=_("Fax")),
        models.CharField(max_length=32, name="economic_state", verbose_name=_("Account")),
    )
        #display.Resource(name="person", verbose_name=_("Person")),

    #FUTURE TODO: display_fields should be DisplayField classes with properties is_confidential
    confidential_fields = ('economic_state',) 

    class Meta:
        verbose_name = _('GAS member')
        verbose_name_plural = _('GAS members')
        app_label = 'gas'
        unique_together = (('gas', 'id_in_gas'), ('person', 'gas'))
        ordering = ('gas__name', 'person__display_name')

    def __unicode__(self):
        #rv = _('%(person)s in GAS "%(gas)s"') % {'person' : self.person, 'gas': self.gas}
        rv = '%(gas)s - %(person)s' % {'person' : self.person, 'gas': self.gas.id_in_des}
        #if settings.DEBUG:
        #    rv += " [%s]" % self.pk
        return rv

    def statistic_name(self):
        rv = '%(gas)s - %(person)s ' % {'person' : self.person, 'gas': self.gas.id_in_des}
        #rv = _('%(person)s ') % {'person' : self.person}
        return rv

    def _get_roles(self):
        """
        Return a QuerySet containing all the parametric roles which have been assigned
        to the User associated with this GAS member.
        
        Only roles which make sense for the GAS member belongs to are returned 
        (excluding roles the User may have been assigned with respect to other GAS).
        """
        # Roles MUST BE a property because roles are bound to a User 
        # with `add_principal()` and not directly to a GAS member
        # costruct the result set by joining partial QuerySets
        roles = []
        # get all parametric roles assigned to the User associated with this GAS member;
        # note that "spurious" roles can be included, since a User can be a member of more
        # than one GAS, while here we're interested only in roles bound to the GAS this 
        # GAS member belongs to
        qs = ParamRole.objects.filter(principal_param_role_set__user = self.person.user)
        # add  `GAS_REFERRER`, `GAS_REFERRER_CASH`, `GAS_REFERRER_TECH`, `GAS_REFERRER_SUPPLIER` and `GAS_MEMBER` roles
        roles += [pr for pr in qs if pr.gas == self.gas]
        # add  `GAS_REFERRER_ORDER` roles
        roles += [pr for pr in qs if pr.order.pact.gas == self.gas]
        # add  `GAS_REFERRER_DELIVERY` roles
        roles += [pr for pr in qs if self.gas in pr.delivery.gas_list]
        # add  `GAS_REFERRER_WITHDRAWAL` roles
        roles += [pr for pr in qs if self.gas in pr.withdrawal.gas_list]
        # HACK: convert a list of model instances to a QuerySet by filtering on instance's primary keys
        qs = ParamRole.objects.filter(pk__in=[obj.pk for obj in roles]) 
        return qs 

    def _set_roles(self, list):
        raise NotImplementedError

    roles = property(_get_roles, _set_roles)

    @property
    def verbose_name(self):
        """Return GASMember representation along with his own card number in GAS"""
        #See ticket #54
        return ug("%(id_in_gas)s - %(gas_member)s") % {'gas_member' : self, 'id_in_gas': self.id_in_gas}

    @property
    def parent(self):
        return self.gas

    #COMMENT domthu: fero added id_in_des (or id_in_gas ) for GASMember. That it not required: ask to community if necesary.
    @property
    def id_in_des(self):
        """TODO: Return unique GAS member "card number" in the DES.
        This must be referred to a Person, not to a GAS membership.
        Think about its use cases.."""
        # TODO:
        # return self.person.id_in_des
        # or
        # return something
        raise NotImplementedError

    @property
    def city(self):
        return self.person.city

    @property
    def email(self):
        return self.person.preferred_email_contacts[0].value

    @property
    def phone(self):
        return self.person.preferred_phone_contacts[0].value

    @property
    def fax(self):
        return self.person.preferred_fax_contacts[0].value

    @property
    def economic_state(self):
        """Show summary of GASMember economic state.

        It uses the following syntax:

        %(account_money)s - ( %(tot_confirmed_gmo_for_open_gso)s - %(tot_confirmed_gmo_for_closed_gso)s) = %(account_decurted)s

        where:

        * account_money: is the amount of money that exist now in the GASMember account
        * tot_confirmed_gmo_for_open_gso: is the amount of money due for confirmed GASMemberOrder of GASSupplierOrder that are not closed
        * tot_confirmed_gmo_for_closed_gso: is the amount of money due for confirmed GASMemberOrder of GASSupplierOrder that are closed
        * account_decurted: is the result of the operation
        """

        st1 = self.total_basket
        st2 = self.total_basket_to_be_delivered
        try:
            return u"%s - (%s + %s) = %s"  % (self.balance, st1, st2, (self.balance - (st1 + st2)))
        except AttributeError:
            # Account descriptor is not implemented yet
            return u"(%s + %s)"  % (st1, st2)

    @property
    def total_basket(self):
        tot = 0
        for gmord in self.basket:
            tot += gmord.price_expected
        return tot

    @property
    def total_basket_to_be_delivered(self):
        tot = 0
        for gmord in self.basket_to_be_delivered:
            tot += gmord.price_expected
        return tot

    def setup_roles(self):
        # Automatically add the new GASMember to the `GAS_MEMBER` Role for its GAS
        if not self.is_suspended:
            self.add_gmrole()

    def add_gmrole(self):
        role = ParamRole.get_role(GAS_MEMBER, gas=self.gas)
        user = self.person.user
        role.add_principal(user)

    def remove_gmrole(self):
        role = ParamRole.get_role(GAS_MEMBER, gas=self.gas)
        user = self.person.user
        PrincipalParamRoleRelation.objects.get(user=user, role=role).delete()

    def clean(self):
        # Clean method is for validation. Validation errors are meant to be
        # catched in forms
        try:
            assert self.person.user # GAS members must have an account on the system
        except User.DoesNotExist:
            raise ValidationError(ug("GAS Members must be registered users"))
        return super(GASMember, self).clean()

    def save(self, *args, **kw):
        # Save method is meant to do some trickery at saving time
        # and to do some low-level checks raising low-level exceptions.
        # These exceptions do not need to be translated.
        if not self.person.user: # GAS members must have an account on the system
            raise AttributeError('GAS Members must be registered users')
        if not self.id_in_gas:
            self.id_in_gas = None

        # Check for role update
        activate_gmrole = False
        remove_gmrole = False

        if self.pk:
            # Search among all_objects! (even suspended)
            old_gm = GASMember.all_objects.get(pk=self.pk)
            if self.is_suspended and not old_gm.is_suspended:
                remove_gmrole = True
            if old_gm.is_suspended and not self.is_suspended:
                activate_gmrole = True
            
        super(GASMember, self).save(*args, **kw)

        if activate_gmrole:
            self.add_gmrole()
        elif remove_gmrole:
            self.remove_gmrole()

    def setup_accounting(self):
        """ GASMember contributes to GAS and Person accounting hierarchies.

        #GAS-side
        . ROOT (/)
        +----------- members [P,A]+
        |                +--- <UID member #1>  [A]
        |                | ..
        |                +--- <UID member #n>  [A]

        #Person-side
        . ROOT (/)
        |--- wallet [A]
        +--- expenses [P,E]+
                +--- gas [P, E] +
                        +--- <UID gas #1>  [P, E]+
                        |            +--- recharges [E]
                        |            +--- fees [E]
                        | ..
                        +--- <UID gas #n>  [P, E]
                                    +--- recharges [E]
                                    +--- fees [E]
        """

        person_system = self.person.accounting.system
        gas_system = self.gas.accounting.system
        
        ## Person-side
        # placeholder for payments made by this person to GASs (s)he belongs to
        try:
            person_system['/expenses/gas']
        except Account.DoesNotExist:
            person_system.get_or_create_account(
                parent_path='/expenses', name='gas', kind=account_type.expense, is_placeholder=True
            )

        # base account for expenses related to this GAS membership
        person_system.get_or_create_account(
            parent_path='/expenses/gas', name=self.gas.uid, kind=account_type.expense, 
            is_placeholder=True
        )
        # recharges
        person_system.get_or_create_account(
            parent_path='/expenses/gas/' + self.gas.uid, name='recharges', kind=account_type.expense
        )
        # membership fees
        person_system.get_or_create_account(
            parent_path='/expenses/gas/' + self.gas.uid, name='fees', kind=account_type.expense
        )

        ## GAS-side
        gas_system.get_or_create_account(
            parent_path='/members', name=self.person.uid, kind=account_type.asset
        )

    @property
    def des(self):
        # A GAS member belongs to the DES its GAS belongs to.
        return self.gas.des

    @property
    def gas_list(self):
        return [self.gas]

    @property
    def pacts(self):
        # A GAS member is interested primarily in those pacts (`GASSupplierSolidalPact` instances) subscribed by its GAS
        return self.gas.pacts

    @property
    def suppliers(self):
        # A GAS member is interested primarily in those suppliers dealing with its GAS
        return self.gas.suppliers

    @property
    def orders(self):
        # A GAS member is interested primarily in those suppliers orders to which he/she can submit orders
        return self.gas.orders

    @property
    def deliveries(self):
        # A GAS member is interested primarily in delivery appointments scheduled for its GAS
        return self.gas.deliveries

    @property
    def withdrawals(self):
        # A GAS member is interested primarily in withdrawal appointments scheduled for its GAS
        return self.gas.withdrawals

    @property
    def products(self):
        # A GAS member is interested primarily to show products
        return self.gas.products

    @property
    def stocks(self):
        # A GAS member is interested primarily to show products and price
        return self.gas.stocks

    @property
    def gasstocks(self):
        # A GAS member is interested primarily in those products and price per GAS
        return self.gas.gasstocks

    @property
    def gasmember(self):
        return self

    @property
    def basket(self):
        from gasistafelice.gas.models import GASMemberOrder
        #TODO FIXME AFTER 6: there should be no entry with ordered_amount = 0 in GASMemberOrder table
        return self.gasmember_order_set.filter(ordered_product__order__in=self.orders.open(), ordered_amount__gt=0)

    @property
    def basket_to_be_delivered(self):
        """GAS member's products ordered of closed orders"""

        #WAS: from gasistafelice.gas.models import GASMemberOrder
        #WAS: return GASMemberOrder.objects.filter(
        #WAS:     purchaser=self,
        #WAS:     ordered_product__order__in=self.orders.closed()
        #WAS: )
        return self.gasmember_order_set.filter(
            ordered_product__order__in=self.orders.closed()
        )

    @property
    def orderable_products(self):
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open())
    
    @property
    def issued_orders(self):
        """
        The queryset of orders this member has issued against his/her GAS. 
        """
        return self.gasmember_order_set.all()
        
    
    #-- Authorization API --#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new Person to a GAS ?
        # * administrators for that GAS
        allowed_users = User.objects.none()
        try:
            gas = context['gas']
            allowed_users = gas.tech_referrers
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)

        return user in allowed_users
    
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a GAS member ?
        # * the member itself
        # * tech referrers for that GAS
        allowed_users = list(self.gas.tech_referrers) + [self.person.user] 
        return user in allowed_users  
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can remove a member from a GAS ?
        # * tech referrers for that GAS
        allowed_users = self.gas.tech_referrers  
        return user in allowed_users

    def can_view_confidential(self, user, context):
        return user == self.person.user

    #--------------------------#

    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        return self.person.accounting.entries_gasmember(self)

    @property
    def balance(self):
        """Accounting sold for this gasmember"""
        #FIXME: only for this person in this GAS! Not for the person himself
        #acc_tot = self.person.accounting.system['/wallet'].balance
        acc_tot = self.gas.accounting.system['/members/' + self.person.uid].balance
        return acc_tot

    @property
    def last_recharge(self):
        """last reharge for this gasmember"""
        rv = ''
        latest = self.person.accounting.last_entry('/expenses/gas/' + self.gas.uid + '/recharges')
        if latest:
            return u"%(amount)s \u20AC %(date)s<br />%(note)s" % {
                'amount' : "%.2f" % latest.amount,
                'date': long_date(latest.date),
                'note': latest.description,
            }
        return rv

    @property
    def last_fee(self):
        """last fee for this gasmember"""
        rv = ''
        latest = self.gas.accounting.last_person_fee(self.person)
        if latest:
            return u"%(amount)s\u20AC %(date)s<br />%(note)s" % {
                'amount' : "%.2f" % latest.amount,
                'date': long_date(latest.date),
                'note': latest.description,
            }
        return rv

    
    #----------------------------------------------#

    def send_email(self, to, cc=[], more_info='', issued_by=None):

        log.debug("Basket send_email: %s" % to)
        if not isinstance(to, list):
            to = [to]

        try:
            sender = self.gas.preferred_email_contacts[0].value
        except IndexError as e:
            msg = ug("GAS cannot send email, because no preferred email for GASMember specified")
            sender = settings.DEFAULT_FROM_EMAIL
            more_info += '%s --> %s' % (msg, sender)

        subject = u"[ORD] %(gas_id_in_des)s - %(ord)s" % {
            'gas_id_in_des' : self.gas.id_in_des,
            'ord' : self
        }

        message = u"In allegato il paniere del gasista %(gasmember)s." % { 'gasmember': self }
        message += more_info

        email = EmailMessage(
            subject = subject,
            body = message,
            from_email = sender,
            to = to, cc = cc,
        )

        #FIXME: No handlers could be found for logger "xhtml2pdf"
        pdf_data = self.get_pdf_data(requested_by=issued_by)
        if not pdf_data:
            email.body += ug('We had some errors in report generation. Please contact %s') % settings.SUPPORT_EMAIL
        else:
            email.attach(
                u"%s.pdf" % self.get_valid_name(),
                pdf_data,
                'application/pdf'
            )

        email.send()
        return 

    def get_valid_name(self):
        from django.template.defaultfilters import slugify
        from django.utils.encoding import smart_str
        n = "%(id)s_%(datetime)s" % {
            'id'        : smart_str(slugify(self.id_in_gas).replace('-', '_')),
            'datetime'  : '{0:%Y%m%d_%H%M}'.format(datetime.datetime.now())
        }
        return n

    def send_email_to_gasmember(self, cc=[], more_info='', issued_by=None):
        gasmember_email = self.preferred_email_address
        return self.send_email(
            [gasmember_email],
            cc=cc, more_info=more_info,
            issued_by=issued_by
        )

    def get_pdf_data(self, requested_by=None):
        """Return PDF raw content to be rendered somewhere (email, or http)"""

        if not requested_by:
            requested_by = User.objects.get(username=settings.INIT_OPTIONS['su_username'])

        querySet = self.basket | self.basket_to_be_delivered
        querySet = querySet.order_by('ordered_product__order__pk') 
        context_dict = {
            'gasmember' : self,
            'records' : self._get_pdfrecords(querySet),
            'rec_count' : querySet.count(),
            'user' : requested_by,
            'total_amount' : self.total_basket,
            'CSS_URL' : settings.MEDIA_ROOT,
        }

        REPORT_TEMPLATE = "blocks/basket/report.html"

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("iso-8859-1", "ignore")), result)
        pisadoc = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8", "ignore")), result)
        if not pisadoc.err:
            rv = result.getvalue()
        else:
            log.debug('Some problem while generate pdf err: %s' % pisadoc.err)
            rv = None
        return rv

    def _get_pdfrecords(self, querySet):
        """Return records of rendered table fields."""

        records = []
        actualProduttore = -1
        rowOrder = -1
        description = ""
        producer = ""
        tot_prod = 0

        for el in querySet:
            rowOrder = el.order.pk
            if actualProduttore == -1 or actualProduttore != rowOrder:
                if actualProduttore != -1:
                    tot_prod = 0
                actualProduttore = rowOrder
                description = unicode(el.order)
                producer = el.supplier
            tot_prod += el.price_expected

            records.append({
               'order' : rowOrder,
               'order_description' : description,
               'supplier' : producer,
               'amount' : el.ordered_amount,
               'product' : el.product,
               'price_ordered' : el.ordered_price,
               'price_delivered' : el.ordered_product.order_price,
               'price_changed' : el.has_changed,
               'tot_price' : el.price_expected,
               'tot_prod' : tot_prod,
               'order_confirmed' : el.is_confirmed,
               'note' : el.note,
            })

        return records

    #-----------------------------------------------#


#------------------------------------------------------------------------------


class GASSupplierStock(models.Model, PermissionResource):
    """A Product as available to a given GAS (including price, order constraints and availability information)."""

    pact = models.ForeignKey("GASSupplierSolidalPact", related_name="gasstock_set")
    stock = models.ForeignKey(SupplierStock, related_name="gasstock_set")
    # if a Product is available to GAS Members; policy is GAS-specific
    # A product can be disabled at supplier level. In this case the GASSupplierStock is ALWAYS disabled
    # else the GASSupplierStock can be enabled or not at the GAS level
    enabled = models.BooleanField(default=True,verbose_name=_('enabled'))

    # how many Product units a GAS Member is able to order
    minimum_amount = PrettyDecimalField(max_digits=5, decimal_places=2, 
                        default=1, verbose_name=_('minimum order amount')
    )
    # increment step (in Product units) for amounts exceeding minimum;
    # useful when a Product has a fixed step of increment
    step = PrettyDecimalField(max_digits=5, decimal_places=2,
                        default=1, verbose_name=_('step of increment')
    )

    history = HistoricalRecords()

    def __unicode__(self):
        return u"%s%s" % (self.stock, self.father_price)
        #return unicode(self.stock)

    def __init__(self, *args, **kw):
        super(GASSupplierStock, self).__init__(*args, **kw)
    
    @property
    def gasmembers(self):
        return self.gas.gasmembers

    @property
    def gas(self):
        return self.pact.gas
    
    @property
    def supplier(self):
        return self.stock.supplier

    @property
    def product(self):
        return self.stock.product

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.filter(pk=self.pk)

    @property
    def gasstock(self):
        return self

    @property
    def price(self):
        # Product base price as updated by agreements contained in GASSupplierSolidalPact
        price_percent_update = self.pact.order_price_percent_update or 0
        return self.stock.price*(1 + price_percent_update)

    @property
    def report_price(self):
        symb = self.stock.product.pu.symbol
        if self.stock.product.mu and self.stock.product.muppu == 1 and (self.stock.product.mu.symbol == "Kg" or self.stock.product.mu.symbol == "Lt"):
                symb = self.stock.product.mu.symbol
        rv = u" %(price)s\u20AC/%(symb)s" % {
            'symb' : symb,
            'price': "%.2f" % round(self.price,2),
        }
        return rv
        
    @property
    def father_price(self):
        """Parent price is the price in respect to parent unit.

        This is useful to say how much it cost at liter or at kilo.
        """

        if self.stock.product.mu:

            #find relative UnitsConversion
            #TODO 1a) add boolean flag into UnitsConversion table to define father units 
            #TODO or 1b) add boolean flag into UnitsConversion table to define father units 
            if self.stock.product.mu.symbol == "DAM":
                return self.set_father_price(self.price / 5, 'Lt')
            if self.stock.product.mu.symbol == "Lt" and self.stock.product.muppu != 1:
                return self.set_father_price(self.price / self.stock.product.muppu, self.stock.product.mu.symbol)
            if self.stock.product.mu.symbol == "Ml":
                return self.set_father_price(self.price * 1000 / self.stock.product.muppu, 'Lt')
            if self.stock.product.mu.symbol == "Cl":
                return self.set_father_price(self.price * 100 / self.stock.product.muppu, 'Lt')
            if self.stock.product.mu.symbol == "Dl":
                return self.set_father_price(self.price * 10 / self.stock.product.muppu, 'Lt')
            if self.stock.product.mu.symbol == "Gr":
                return self.set_father_price(self.price * 1000 / self.stock.product.muppu, 'Kg')
            if self.stock.product.mu.symbol == "Hg":
                return self.set_father_price(self.price * 10 / self.stock.product.muppu, 'Kg')
            if self.stock.product.mu.symbol == "Kg" and self.stock.product.muppu != 1:
                return self.set_father_price(self.price / self.stock.product.muppu, self.stock.product.mu.symbol)
        else:
            #This case should not be possible but the PU list offer the possibility to do it 
            if self.stock.product.pu.symbol.strip() == "Ml":
                return self.set_father_price(self.price * 1000 / self.stock.product.muppu, 'Lt')
            if self.stock.product.pu.symbol.strip() == "Cl":
                return self.set_father_price(self.price * 100 / self.stock.product.muppu, 'Lt')
            if self.stock.product.pu.symbol.strip() == "Dl":
                return self.set_father_price(self.price * 10 / self.stock.product.muppu, 'Lt')
            if self.stock.product.pu.symbol.strip() == "Gr":
                return self.set_father_price(self.price * 1000 / self.stock.product.muppu, 'Kg')
            if self.stock.product.pu.symbol.strip() == "Hg":
                return self.set_father_price(self.price * 10 / self.stock.product.muppu, 'Kg')
        return ""

    @classmethod
    def set_father_price(self, price_per_unit, father_unit):
        return u" a %(ppu)s\u20AC/%(mu)s" % {
            'ppu' : "%.2f" % round(price_per_unit,2),
            'mu'  : father_unit
        }

    class Meta:
        app_label = 'gas'
        verbose_name = _("GAS supplier stock")
        verbose_name_plural = _("GAS supplier stocks")

    @property
    def has_changed_availability(self):
        #TODO: add to GASSupplierSolidalPact model the inactive state of a solidal pact
        #if (not pact.is_active):
        #    log.debug('Solidal pact unactive')
        #    return False;
        try:
            # WAS: FIXME: Generate error raise self.model.DoesNotExist: GASSupplierStock matching query does not exist
            # COMMENT LF: It was because you called it in non-existent GASSupplierStock
            # COMMENT LF: see "if self.pk" in self.save()
            gss = GASSupplierStock.objects.get(pk=self.pk)
            if not gss is None:
                return bool(self.enabled != gss.enabled)
            else:
                return False
        except GASSupplierStock.DoesNotExist:
            return False

    def save(self, *args, **kwargs):

        # CASCADING
        if self.pk:
            created = False
            if self.has_changed_availability:

                log.debug('   Changing for PDS %s(%s) and stock %s(%s)' %  (
                    self.pact, self.pact.pk, self.stock, self.stock.pk
                ) )
                #For each GASSupplierOrder in Open or Closed state Add or delete GASSupplierOrderProduct
                for order in self.orders.open():
                    log.debug("Change availability GSO order %s" % order)
                    if self.enabled:
                        order.add_product(self)
                    else:
                        # Delete GASSupplierOrderProduct for GASSupplierOrder 
                        # in Open State or Closed state. Delete GASMemberOrder associated
                        order.remove_product(self)
        else:
            created = True

        super(GASSupplierStock, self).save(*args, **kwargs)

        if created:
            log.debug('   Adding product %s(%s) to open orders' %  (
                self.stock, self.stock.pk
            ) )
            #For each GASSupplierOrder in Open or Closed state Add or delete GASSupplierOrderProduct
            for order in self.orders.open():
                log.debug("Change availability GSO order %s" % order)
                if self.enabled:
                    order.add_product(self)

    #-- Resource API --#

    @property
    def orders(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        return GASSupplierOrder.objects.filter(pact=self.pact)

    @property
    def orderable_products(self):
        from gasistafelice.gas.models import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders.open(), gasstock=self)

    #-- Authorization API --#

    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new supplier stock for a GAS ?
        # * referrers for the pact the supplier stock is associated to
        # * GAS administrators
        allowed_users = User.objects.none()
        try:
            pact = context['pact']
            allowed_users = pact.gas.tech_referrers | pact.referrers
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)
        return user in allowed_users
    
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details for an existing supplier stock for a GAS ?
        # * referrers for the pact the supplier stock is associated to
        # * GAS administrators 
        allowed_users = self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing supplier stock for a GAS ?
        # * referrers for the pact the supplier stock is associated to
        # * GAS administrators 
        allowed_users = self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    #-- Production data --#

    # how many items of this gas supplier stock were ordered (globally by the GAS for this GASSupplierProduct)
    @property
    def tot_amount(self):
        amount = 0 
#        for gsop in self.orderable_products.values('tot_amount'):
#            amount += gsop['tot_amount']
        for gsop in self.orderable_products:
            amount += gsop.tot_amount
        return amount 

    @property
    def tot_gasmembers(self):
        persons = 0
        for gsop in self.orderable_products:
            persons += gsop.tot_gasmembers
        return persons

    @property
    def tot_price(self):
        tot = 0
        for gsop in self.orderable_products:
            tot += gsop.tot_price
        return tot




#-----------------------------------------------------------------------------------------------------
    
class GASSupplierSolidalPact(models.Model, PermissionResource):
    """Define a GAS <-> Supplier relationship agreement.

    Each Supplier comes into relationship with a GAS by signing a pact,
    where are factorized behaviour agreements between these two entities.
    This pact acts as a configurator for order and delivery management with respect to the given Supplier.

    >>> from gasistafelice.gas.models.base import GAS, GASSupplierSolidalPact
    >>> from gasistafelice.supplier.models import Supplier
    >>> g1 = GAS(name='GAS1')
    >>> g1.save()
    >>> s1 = Supplier(name='Supplier1')
    >>> s1.save()

    >>> pds = GASSupplierSolidalPact()
    >>> pds.gas = g1
    >>> pds.supplier = s1
    >>> pds.save()
    >>> print pds
    Pact between GAS1 and Supplier1

    >>> from gasistafelice.gas.models.base import *
    >>> from gasistafelice.gas.models.order import *
    >>> from gasistafelice.supplier.models import *
    >>> p = GASSupplierSolidalPact(gas=GAS.objects.get(id=1), supplier=Supplier.objects.get(id=1))
    >>> p.save()
    >>> st = SupplierStock.objects.filter(supplier__id=3).count()
    >>> gst = GASSupplierStock.objects.filter(pact__id=p.pk).count()
    >>> st==gst
    True
    >>> p.account_id>0
    True

    """

    gas = models.ForeignKey(GAS, related_name="pact_set",verbose_name=_('GAS'))
    supplier = models.ForeignKey(Supplier, related_name="pact_set",verbose_name=_('Supplier'))
    date_signed = models.DateField(verbose_name=_('Date signed'), auto_now=False, auto_now_add=False, blank=True, null=True, default=None, help_text=_("date of first meeting GAS-Producer"))

    # which Products GAS members can order from Supplier
    stock_set = models.ManyToManyField(SupplierStock, through=GASSupplierStock, null=True, blank=True)
    order_minimum_amount = CurrencyField(verbose_name=_('Order minimum amount'), null=True, blank=True)

    # Delivery cost. i.e: transport cost
    order_delivery_cost = CurrencyField(verbose_name=_('Order delivery cost'), null=True, blank=True)

    #time needed for the delivery since the GAS issued the order disposition
    order_deliver_interval = models.TimeField(verbose_name=_('Order delivery interval'), null=True, blank=True)

    # how much (in percentage) base prices from the Supplier are modified for the GAS
    order_price_percent_update = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=3, verbose_name=_('order price percent update'))
    
    # default_delivery_day should holds a "datetime string syntax" to be interpreted by software.
    # It must express "first day of the month", "first day of the first and third week of the month", ... : see ticket #65
    default_delivery_day = models.CharField(max_length=16, 
        choices=const.DAY_CHOICES, blank=True, help_text=_("delivery week day agreement"),
        verbose_name=_('default delivery day')
    )
    default_delivery_time = models.TimeField(null= True, blank=True, 
        help_text=_("delivery time agreement"), verbose_name=_('default delivery time')
    )

    default_delivery_place = models.ForeignKey(Place, 
        verbose_name=_('Default delivery place'), 
        related_name="pact_default_delivery_place_set", null=True, blank=True
    )

    # Field to reflect
    # http://www.jagom.org/trac/REESGas/wiki/BozzaAnalisiFunzionale/Gestione dei fornitori e dei listini
    # This MUST NOT be shown in form if GASConfig.auto_populate_products is True
    auto_populate_products = models.BooleanField(default=True, 
        help_text=_("automatic population of all products bound to a supplier in gas supplier stock"),
        verbose_name=_('auto populate products')
    )

    orders_can_be_grouped = models.BooleanField(verbose_name=_('can be InterGAS'), 
        default=False, 
        help_text=_("If true, this supplier can aggregate orders from several GAS")
    )

    document = models.FileField(upload_to=base_utils.get_pact_path, 
        null=True, blank=True, verbose_name=_("document"), 
        help_text=_("Document signed by GAS and Supplier")
    )

    send_email_on_order_close = models.BooleanField(default=False, 
        help_text=_("Automatically send email to supplier and gas referrer supplier as soon as an order is closed"),
        verbose_name=_("send email on order close")
    )

    # Fields for suspension management:
    is_suspended = models.BooleanField(verbose_name=_("is suspended"),
        default=False, db_index=True, 
        help_text=_("A pact can be broken or removed by one of the partner. If it is not active no orders can be done and the pact will not appear anymore in the interface. When a pact is suspended you can specify when it could be resumed")
    )
    suspend_datetime = models.DateTimeField(default=None, null=True, blank=True) # When this pact was suspended
    suspend_reason = models.TextField(blank=True, default='', db_index=False)
    suspend_auto_resume = models.DateTimeField(default=None, null=True, blank=True, db_index=True) # If not NULL and is_suspended, auto resume at specified time

    history = HistoricalRecords()

    display_fields = (
        display.Resource(name="gas", verbose_name=_("GAS")),
        display.Resource(name="supplier", verbose_name=_("Supplier")),
        display.ResourceList(name="referrers_people", verbose_name=_("Referrers")),
        order_minimum_amount, order_delivery_cost, order_deliver_interval,
        default_delivery_place, document
    )

    class Meta:
        app_label = 'gas'
        unique_together = (('gas', 'supplier'),)

    def __unicode__(self):
#        return ug("Pact between %(gas)s and %(supplier)s") % \
#                      { 'gas' : self.gas, 'supplier' : self.supplier}
        return ug("%(gas)s - %(supplier)s") % \
                      { 'gas' : self.gas.id_in_des, 'supplier' : self.supplier}

    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "pact"

    @property
    def referrers(self):
        """
        Return all users being referrers for this solidal pact (GAS-to-Supplier interface).
        """
        # FIXME: should be def supplier_referrers. referrers should be == to info_people
        # retrieve 'GAS supplier referrer' parametric role for this pact
        pr = ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=self)
        # retrieve all Users having this role
        return pr.get_users()    

    #FIXME: remove when this property is subsituted by referrers_people's property in all part of the application
    @property
    def supplier_referrers_people(self):
        return self.referrers_people
 
    @property
    def referrers_people(self):
        prs = Person.objects.none()
        if self.referrers:
            prs = Person.objects.filter(user__in=self.referrers)
        return prs

    def setup_roles(self):
        # register a new `GAS_REFERRER_SUPPLIER` Role for this solidal pact
        register_parametric_role(name=GAS_REFERRER_SUPPLIER, pact=self)

    def setup_accounting(self):
        """ GASSupplierSolidalPact contributes to GAS and Supplier accounting hierarchies.

        # GAS-side
        . ROOT (/)
        +----------- expenses [P,E]+
        |               +--- suppliers [P, E] +
        |                       +--- <UID supplier #1>  [E]
        |                       | ..
        |                       +--- <UID supplier #n>  [E]
        +----------- incomes [P,I]+
                        +--- suppliers [P, I] +
                                +--- <UID supplier #1>  [P, I]
                                | ..
                                +--- <UID supplier #n>  [P, I]

        # SUPPLIER-side
        . ROOT (/)
        +----------- incomes [P,I]+
        |               +--- gas [P, I] +
        |                       +--- <UID gas #1>  [P, I]
        |                       | ..
        |                       +--- <UID gas #n>  [P, I]
        +----------- expenses [P,E]+
                        +--- gas [P, E] +
                                +--- <UID gas #1>  [E]
                                | ..
                                +--- <UID gas #n>  [E]
        """

        gas_system = self.gas.accounting.system
        gas_system.get_or_create_account(
            parent_path='/expenses/suppliers', name=self.supplier.uid, kind=account_type.expense
        )
        gas_system.get_or_create_account(
            parent_path='/expenses/suppliers', name=self.supplier.uid, kind=account_type.expense
        )
        supplier_system = self.supplier.accounting.system
        supplier_system.get_or_create_account(
            parent_path='/incomes/gas', name=self.gas.uid, kind=account_type.income
        )

    def setup_data(self):
        for st in self.supplier.stocks:
            #see GASSupplierStock.enabled comment
            #enabled = [False, self.auto_populate_products][bool(st.amount_available)]
            if not self.auto_populate_products:
                enabled = False
            else:
                enabled = bool(st.amount_available)
            GASSupplierStock.objects.create(pact=self, stock=st, enabled=enabled, \
                                minimum_amount=st.detail_minimum_amount,
                                step=st.detail_step,
            )

    def save(self, *args, **kw):
        if self.gas.config.auto_populate_products:
            self.auto_populate_products = True

        super(GASSupplierSolidalPact, self).save(*args, **kw)

    #-- Resource API --#

    @property
    def parent(self):
        return self.gas

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.supplier.pk)

    @property
    def des(self):
        return self.gas.des

    @property
    def gas_list(self):
        return [self.gas]

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def orders(self):
        return self.order_set.all()

    @property
    def gasstocks(self):
        return self.gasstock_set.all()

    @property
    def stock(self):
        raise NoSenseException("A GASSupplierSolidalPact is ALWAYS connected to more than one stock")
        
    @property
    def gasstock(self):
        raise NoSenseException("A GASSupplierSolidalPact is ALWAYS connected to more than one gas stock")

    @property
    def pacts(self):
        # itself in queryset
        return GASSupplierSolidalPact.objects.filter(pk=self.pk)

    @property
    def pact(self):
        return self

    @property
    def persons(self):
        qs = self.gas.persons | self.supplier.persons
        return qs.distinct()

    @property
    def referrers_people(self):
        return self.persons.filter(user__in=self.referrers)

    @property
    def info_people(self):
        return self.gas.info_people | self.supplier.info_people

    #-- Authorization API --#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        """Who can create a new pact?

        In general:
            * GAS supplier referrers (of other pacts)
            * GAS administrators
        In depth we have to switch among multiple possible contexts

        If we are checking for a "unusual key" (not in ctx_keys_to_check),
        just return False, do not raise an exception.
        """

        allowed_users = User.objects.none()
        ctx_keys_to_check = set(('gas', 'site', 'supplier'))
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
        elif k == 'gas':
            # gas context
            gas = context[k]
            allowed_users = gas.tech_referrers | gas.supplier_referrers 

        elif k == 'supplier':
            # supplier context
            # Every GAS tech referrers and referrers suppliers can create a pact for this supplier
            # Within the form and authorization check, GAS choices will be limited
            supplier = context[k]
            des = supplier.des
            allowed_users = des.gas_tech_referrers | des.gas_supplier_referrers

        elif k == 'site': 
            # des context
            # all GAS tech referrers and referrers suppliers can create a pact in a DES.
            # Within the form and authorization check, GAS choices will be limited
            des = context[k]
            allowed_users = des.gas_tech_referrers | des.gas_supplier_referrers

        return user in allowed_users

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details for a pact in a GAS ?
        # * GAS administrators 
        # * referrers for that pact
        allowed_users = self.gas.tech_referrers | self.gas.supplier_referrers 
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a pact in a GAS ?
        # * GAS administrators 
        allowed_users = self.gas.tech_referrers 
        return user in allowed_users 
    
    @property
    def roles(self):
        "Pact involves also roles related to Suppliers"""

        roles = super(GASSupplierSolidalPact, self).roles
        #for supplier in self.suppliers:
        #    roles |= supplier.roles
        return roles

    #--------------------------#

    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        #Limit only entries_pact for this solidal pact
        return self.supplier.accounting.entries_pact(self.gas)

    @property
    def balance(self):
        """Accounting sold for this pact"""

        return self.supplier.accounting.get_pact_balance(self)

    @property
    def insolutes(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        orders = GASSupplierOrder.objects.closed().filter(pact=self) | \
            GASSupplierOrder.objects.unpaid().filter(pact=self)
        return orders

#------------------------------------------------------------------------------



