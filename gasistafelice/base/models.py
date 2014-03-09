"""
This is the base model for Gasista Felice.
It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.models import permalink
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from workflows.models import Workflow, Transition, State
from history.models import HistoricalRecords

from gasistafelice.consts import GAS_REFERRER_SUPPLIER
from flexi_auth.models import PermissionBase # mix-in class for permissions management
from flexi_auth.models import ParamRole, Param
from flexi_auth.exceptions import WrongPermissionCheck
from flexi_auth.utils import get_parametric_roles

from flexi_auth.models import PrincipalParamRoleRelation

from simple_accounting.models import economic_subject, AccountingDescriptor, LedgerEntry, account_type 

from gasistafelice.lib import ClassProperty, unordered_uniq
from gasistafelice.base import const
from gasistafelice.base.utils import get_resource_icon_path
from gasistafelice.base.accounting import PersonAccountingProxy

from workflows.utils import do_transition
import os
import logging
log = logging.getLogger(__name__)

class Resource(object):
    """Base class for project fundamental objects.

    This is a basic mix-in class used to factor out data/behaviours common
    to the majority of model classes in the project's applications.
    
    Resource API is composed of:
    * Basic methods and properties: 
     * basic type and resource string representation
     * caching operations
    * Relational properties:
     * how the resource relates to other resources
    """

    # Attribute used to make a list of confidential lists
    confidential_fields = ()

    # Attribute used to cache data
    volatile_fields = []

    #-----------------------------------------
    # Basic properites
    #-----------------------------------------

    @ClassProperty
    @classmethod
    def resource_type(cls):
        """String representation of resource type"""
        
        return cls.__name__.lower()

    @property
    def urn(self):
        """Unique resource name"""
        return '%s/%s' % (self.resource_type, self.pk)
    
    @property
    def ancestors(self):
        """List of ancestors of a resource.

        This is te list of parents from root to the resource itself.
        It is used p.e. to display navigation breadcrumbs.

        You SHOULD NOT implement it in subclasses
        """
        
        if self.parent:
            return self.parent.ancestors + [self.parent]
        else:
            return []

    @property
    def parent(self):
        """Identifies resource which includes this resource.

        Stated that there can be only one parent for a resource,
        (no multiple parents allowed), setting this attribute makes the resource
        confident of who includes itself.

        This attribute is then used to make the list of `:ref:ancestors`.
        
        You MUST implement it in subclasses if they have parent.
        """
        return None

    def do_transition(self, transition, user):
        return do_transition(self, transition, user)

    @property
    def allnotes(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        notes = Comment.objects.filter(object_pk=self.pk, content_type=ctype).order_by('-submit_date')
        return notes

    @permalink
    def get_absolute_url(self):
        return ('rest.views.resource_page', (), { 
                'resource_type' : self.resource_type, 
                'resource_id' : self.pk 
        })

    def get_absolute_url_page(self):
        return self.get_absolute_url().replace('/rest', '/rest/#rest')

    def as_dict(self):
        return {
            'name': unicode(self),
            'urn' : self.urn,
        }

    #-- Referrers API --#

    @property
    def referrers(self):
        """Returns User QuerySet bound to resource"""
        raise NotImplementedError("class: %s method: referrers" % self.__class__.__name__)

    @property
    def referrer(self):
        """Return User bound to resource"""
        raise NotImplementedError("class: %s method: referrer" % self.__class__.__name__)

    @property
    def referrers_people(self):
        """Returns Person related to referrers QuerySet"""
        return Person.objects.filter(user__in=self.referrers)

    @property
    def info_people(self):
        """Returns Person to contact for info QuerySet"""
        raise NotImplementedError("class: %s method: info_people" % self.__class__.__name__)

    #-- History API --#

    # Requires that an history manager exists for the resource
    # TODO: encapsulate it in HistoryResource class

    @property
    def created_on(self):
        """Returns datetime instance of when the instance has been created."""
       
        # There could be the case that a deleted id is reused, so, do not use .get method
        self_as_of_creation = \
            self._default_history.filter(id=self.pk, history_type="+")[0]

        return self_as_of_creation.history_date
    
    @property
    def created_by(self):
        """Returns user that created the resource."""
        #COMMENT fero: disabled user in history!
        return User.objects.none()
       
        # There could be the case that a deleted id is reused, so, do not use .get method
        self_as_of_creation = \
            self._default_history.filter(id=self.pk, history_type="+")[0]

        return self_as_of_creation.history_user

    @property
    def created_by_person(self):
        """Returns person bound to the user that created the resource."""
        u = self.created_by
        if u is not None:
            return u.person
        return None

    @property
    def last_update_by(self):
        """Returns user that has made the last update to the resource."""
       
        #COMMENT fero: disabled user in history!
        return User.objects.none()

        # There could be the case that a deleted id is reused, so, do not use .get method
        try:
            self_as_of_last_update = \
                self._default_history.filter(id=self.pk, history_type="~")[0]
        except IndexError:
            # This object has never been update
            return None
        else:
            return self_as_of_last_update.history_user

    @property
    def last_update_by_person(self):
        """Returns person bound to the user that made the last update the resource."""
        u = self.last_update_by
        if u is not None:
            return u.person
        return None

    @property
    def updaters(self):
        """Returns User QuerySet of who has updated the resource."""
       
        self_updaters = unordered_uniq(
                self._default_history.filter(id=self.pk, history_type="~").values_list('history_user')
            )

        return User.objects.filter(pk__in=map(lambda x: x[0].pk, self_updaters))

    #------------------------------------
    # Basic properties: cache management
    #------------------------------------
        
    def save_checkdata_in_cache(self):
        key = Resource.cache_key(self.pk)
        data_to_cache = {}
        for n in self.volatile_fields:
            data_to_cache[n] = getattr(self, n)
        
        if not data_to_cache:
            return False
                    
        try:
            pstore.savedata(key, data_to_cache)
        except Exception, e:
            raise
        return True

    def load_checkdata_from_cache(self):
        if not self.volatile_fields:
            return False
        key = Resource.cache_key(self.pk)
        data = pstore.getalldata(key, self.volatile_fields)
        for n in self.volatile_fields:
            if data.has_key(n):
                setattr(self, n,  data[n])
        return True

    @classmethod
    def cache_key(cls, resource_id):
        #TODO fero CHECK
        #Pay attention because it is connected to class
        return "%s/%s" % (cls.resource_type, resource_id)

    #---------------------------------------------
    # Relational properties: 
    # not all must be implemented by Resource subclasses
    # but just only that makes sense
    #---------------------------------------------

    @property
    def des_list(self):
        """Return DES instances bound to the resource"""
        raise NotImplementedError("class: %s method: des_list" % self.__class__.__name__)

    @property
    def des(self):
        """Return the DES instance bound to the resource"""
        from gasistafelice.des.models import Siteattr
        return Siteattr.get_site()

        raise NotImplementedError("class: %s method: des" % self.__class__.__name__)

    @property
    def gas_list(self):
        """Return GAS list bound to resource"""
        raise NotImplementedError("class: %s method: gas_list" % self.__class__.__name__)

    @property
    def gas(self):
        """Return GAS bound to resource"""
        raise NotImplementedError("class: %s method: gas" % self.__class__.__name__)

    def categories(self):
        """Return ProductCategory bound to resource"""
        raise NotImplementedError("class: %s method: categories" % self.__class__.__name__)

    def category(self):
        """Return ProductCategory bound to resource"""
        raise NotImplementedError("class: %s method: category" % self.__class__.__name__)

    @property
    def persons(self):
        """Return persons bound to resource"""
        raise NotImplementedError("class: %s method: persons" % self.__class__.__name__)

    @property
    def person(self):
        """Return person bound to resource"""
        raise NotImplementedError("class: %s method: person" % self.__class__.__name__)

    @property
    def gasmembers(self):
        """Return GAS members bound to resource"""
        raise NotImplementedError("class: %s method: gasmembers" % self.__class__.__name__)

    @property
    def gasmember(self):
        """Return GAS member bound to resource"""
        raise NotImplementedError("class: %s method: gasmember" % self.__class__.__name__)

    @property
    def pacts(self):
        """Return pacts bound to resource"""
        raise NotImplementedError("class: %s method: pacts" % self.__class__.__name__)

    @property
    def pact(self):
        """Return pact bound to resource"""
        raise NotImplementedError("class: %s method: pact" % self.__class__.__name__)

    @property
    def suppliers(self):
        """Return suppliers bound to resource"""
        raise NotImplementedError("class: %s method: suppliers" % self.__class__.__name__)

    @property
    def supplier(self):
        """Return supplier bound to resource"""
        raise NotImplementedError("class: %s method: supplier" % self.__class__.__name__)

    @property
    def orders(self):
        """Return orders bound to resource"""
        raise NotImplementedError("class: %s method: orders" % self.__class__.__name__)

    @property
    def order(self):
        """Return order bound to resource"""
        raise NotImplementedError("class: %s method: order" % self.__class__.__name__)

    @property
    def deliveries(self):
        """Return deliveries bound to resource"""
        raise NotImplementedError("class: %s method: deliveries" % self.__class__.__name__)

    @property
    def delivery(self):
        """Return delivery bound to resource"""
        raise NotImplementedError("class: %s method: delivery" % self.__class__.__name__)

    @property
    def withdrawals(self):
        """Return withdrawals bound to resource"""
        raise NotImplementedError("class: %s method: withdrawals" % self.__class__.__name__)

    @property
    def withdrawal(self):
        """Return withdrawal bound to resource"""
        raise NotImplementedError("class: %s method: withdrawal" % self.__class__.__name__)

    @property
    def products(self):
        """Return products bound to resource"""
        raise NotImplementedError("class: %s method: products" % self.__class__.__name__)

    @property
    def product(self):
        """Return product bound to resource"""
        raise NotImplementedError("class: %s method: product" % self.__class__.__name__)

    @property
    def stocks(self):
        """Return SupplierStock list bound to resource"""
        raise NotImplementedError("class: %s method: stocks" % self.__class__.__name__)

    @property
    def stock(self):
        """Return SupplierStock bound to resource"""
        raise NotImplementedError("class: %s method: stock" % self.__class__.__name__)

    @property
    def orderable_products(self):
        """Return GASSupplierOrderProduct querySet for orders bound to resource"""
        raise NotImplementedError("class: %s method: orderable_products" % self.__class__.__name__)

    @property
    def ordered_products(self):
        """Return GASMemberOrder querySet for orders bound to resource"""
        raise NotImplementedError("class: %s method: ordered_products" % self.__class__.__name__)

    @property
    def basket(self):
        """Return GASMemberOrder querySet for open orders bound to resource"""
        raise NotImplementedError("class: %s method: basket" % self.__class__.__name__)

    #-- Contacts --#

    @property
    def contacts(self):
        """Contact QuerySet bound to the resource.

        You SHOULD override it when needed
        """
        return self.contact_set.all()

    @property
    def email_address(self):
        return ", ".join(unordered_uniq(map(lambda x: x[0], self.contacts.filter(flavour=const.EMAIL).values_list('value'))))

    @property
    def phone_address(self):
        return ", ".join(unordered_uniq(map(lambda x: x[0], self.contacts.filter(flavour=const.PHONE).values_list('value'))))

    @property
    def preferred_email_address(self):
        """The email address, where we should write if we would know more info on the resource.

        It is not necessarily bound to a person. 

        NOTE that it could be even a list of addresses following syntax in RFC 5322 and RFC 5321,
        or simply http://en.wikipedia.org/wiki/Email_address#Syntax :)

        Usually you SHOULD NOT NEED TO OVERRIDE IT in subclasses
        """
        if settings.EMAIL_DEBUG:
            return settings.EMAIL_DEBUG_ADDR
        else:
            return ", ".join(unordered_uniq(map(lambda x: x[0], self.preferred_email_contacts.values_list('value'))))

    @property
    def preferred_email_contacts(self):
        """Email Contacts, where we should write if we would know more info on the resource.

        It is not necessarily bound to a person. 

        Usually you SHOULD NOT NEED TO OVERRIDE IT in subclasses
        """
        return self.contacts.filter(flavour=const.EMAIL, is_preferred=True) or \
                    self.contacts.filter(flavour=const.EMAIL)

    @property
    def preferred_phone_address(self):
        return ", ".join(unordered_uniq(map(lambda x: x[0], self.preferred_phone_contacts.values_list('value'))))

    @property
    def preferred_phone_contacts(self):
        return self.contacts.filter(flavour=const.PHONE, is_preferred=True) or \
                    self.contacts.filter(flavour=const.PHONE)

#    @property
#    def preferred_www_address(self):
#        return ", ".join(unordered_uniq(map(lambda x: x[0], self.preferred_www_contacts.values_list('value'))))

#    @property
#    def preferred_www_contacts(self):
#        return self.contacts.filter(flavour=const.WWW, is_preferred=True) or \
#                    self.contacts.filter(flavour=const.WWW)

    @property
    def preferred_fax_address(self):
        return ", ".join(unordered_uniq(map(lambda x: x[0], self.preferred_fax_contacts.values_list('value'))))

    @property
    def preferred_fax_contacts(self):
        return self.contacts.filter(flavour=const.FAX, is_preferred=True) or \
                    self.contacts.filter(flavour=const.FAX)

    @property
    def icon(self):
        "Returns default icon for resource"""
        icon = models.ImageField(upload_to="fake")
        basedir = os.path.join(settings.MEDIA_URL, "nui", "img", settings.THEME)
        icon.url = os.path.join(basedir, "%s%s.%s" % (self.resource_type, "128x128", "png"))
        return icon

#TODO CHECK if these methods SHOULD be removed from Resource API
# because they are tied only to a specific resource. Leave commented now.
# If you need them in a specific resource, implement in it
#    @property
#    def gasstocks(self):
#        """Return GASSupplierStock list bound to resource"""
#        raise NotImplementedError
#
#    @property
#    def gasstock(self):
#        """Return GASSupplierStock bound to resource"""
#        raise NotImplementedError
#
#    @property
#    def units(self):
#        """Return unit measure list bound to resource"""
#        raise NotImplementedError
#
#    @property
#    def unit(self):
#        """Return unit measure bound to resource"""
#        raise NotImplementedError

    #--------------------------#


    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        raise NotImplementedError

    @property
    def balance(self):
        """Return an economic state bound to resource (DES, GASMember, GAS or Supplier through )

        Accounting sold for this ressource
        """
        acc_tot = self.person.accounting.system['/wallet'].balance
        return acc_tot



#------------------------------------------------------------------------------


class PermissionResource(Resource, PermissionBase):
    """
    Just a convenience for classes inheriting both from `Resource` and `PermissionBase`
    """

    def _get_roles(self):
        """
        Return a QuerySet containing all the parametric roles which have been assigned
        to this Resource.
        
        """

        # Roles MUST BE a property because roles are bound to a User 
        # with `add_principal()` and not directly to a GAS member
        # costruct the result set by joining partial QuerySets
        roles = []

        ctype = ContentType.objects.get_for_model(self)
        params = Param.objects.filter(content_type=ctype, object_id=self.pk)
        # get all parametric roles assigned to the Resource;
        return ParamRole.objects.filter(param_set__in=params)

    roles = property(_get_roles)

@economic_subject
class Person(models.Model, PermissionResource):
    """
    A Person is an anagraphic record of a human being.
    It can be a User or not.
    """

    name = models.CharField(max_length=128,verbose_name=_('name'))
    surname = models.CharField(max_length=128,verbose_name=_('surname'))
    display_name = models.CharField(max_length=128, blank=True, verbose_name=_('display name'))
    # Leave here ssn, but do not display it
    ssn = models.CharField(max_length=128, unique=True, editable=False, blank=True, null=True, help_text=_('Write your social security number here'),verbose_name=_('Social Security Number'))
    contact_set = models.ManyToManyField('Contact', null=True, blank=True,verbose_name=_('contacts'))
    user = models.OneToOneField(User, null=True, blank=True,
        verbose_name=_('User'), 
        help_text=_("bind to a user if you want to give this person an access to the platform")
    )
    address = models.ForeignKey('Place', null=True, blank=True,verbose_name=_('main address'))
    avatar = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True, verbose_name=_('avatar'))
    website = models.URLField(verify_exists=True, blank=True, verbose_name=_("web site"))

    accounting = AccountingDescriptor(PersonAccountingProxy)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
        ordering = ('display_name',)

    def __unicode__(self):

        rv = self.display_name 

        if not rv:
            # If display name is not provided --> save display name
            rv = u'%(name)s %(surname)s' % {'name' : self.name, 'surname': self.surname}
            self.display_name = rv
            self.save()

        # Removed city visualization following Orlando's and Dominique's agreements
        # WAS: if self.city:
        # WAS:     rv += u" (%s)" % self.city
        return rv

    @property
    def report_name(self):
        return u"%(name)s %(surname)s" % {'name' : self.name, 'surname': self.surname}

    def clean(self):

        if not self.user and self.gasmembers.count():
            raise ValidationError(_("A person without user cannot be a GAS member"))

        self.name = self.name.strip().lower().capitalize()
        self.surname = self.surname.strip().lower().capitalize()
        self.display_name = self.display_name.strip()
        if not self.ssn:
            self.ssn = None
        else:
            self.ssn = self.ssn.strip().upper()


        return super(Person, self).clean()
    
    @property
    def uid(self):
        """
        A unique ID (an ASCII string) for ``Person`` model instances.
        """
        return self.urn.replace('/','-')
    
    @property
    def parent(self):
        return self.des

    @property
    def icon(self):
        return self.avatar or super(Person, self).icon

    ## START Resource API
    # Note that all the following methods return a QuerySet
    
    @property
    def persons(self):
        return Person.objects.filter(pk=self.pk)

    @property
    def person(self):
        return self

    @property
    def gasmembers(self):
        #TODO UNITTEST
        """
        GAS members associated to this person;
        to each of them corresponds a membership of this person in a GAS.        
        """
        return self.gasmember_set.all()

    
    @property
    def gas_list(self):
        #TODO UNITTEST
        """
        All GAS this person belongs to
        (remember that a person may be a member of more than one GAS).
        """ 
        from gasistafelice.gas.models import GAS
        gas_pks = set(member.gas.pk for member in self.gasmembers)
        return GAS.objects.filter(pk__in=gas_pks)
    
    @property
    def des_list(self):
        #TODO UNITTEST
        """
        All DESs this person belongs to 
        (either as a member of one or more GAS or as a referrer for one or more suppliers in the DES).         
        """
        from gasistafelice.des.models import DES
        des_set = set([gas.des for gas in self.gas_list])
        return DES.objects.filter(pk__in=[obj.pk for obj in des_set])
    
    @property
    def des(self):
        from gasistafelice.des.models import Siteattr
        return Siteattr.get_site()
    
    @property
    def pacts(self):
        """
        A person is related to:
        pacts signed with a GAS he/she belongs to
        """
        from gasistafelice.gas.models import GASSupplierSolidalPact
        # initialize the return QuerySet 
        qs = GASSupplierSolidalPact.objects.none()
        
        #add the suppliers who have signed a pact with a GAS this person belongs to
        for gas in self.gas_list:
            qs = qs | gas.pacts

        return qs

    @property
    def suppliers(self):
        #TODO UNITTEST
        """
        A person is related to:
        1) suppliers for which he/she is a referrer
        2) suppliers who have signed a pact with a GAS he/she belongs to
        """
        from gasistafelice.supplier.models import Supplier
        # initialize the return QuerySet 
        qs = Supplier.objects.none()
        
        #add the suppliers who have signed a pact with a GAS this person belongs to
        for gas in self.gas_list:
            qs = qs | gas.suppliers
        
        # add the suppliers for which this person is an agent
        referred_set = set([sr.supplier for sr  in self.supplieragent_set.all()])
        qs = qs | Supplier.objects.filter(pk__in=[obj.pk for obj in referred_set])
        
        return qs
        
    
    @property
    def orders(self):
        #TODO UNITTEST
        """
        A person is related to:
        1) supplier orders opened by a GAS he/she belongs to
        2) supplier orders for which he/she is a referrer
        3) order to suppliers for which he/she is a referrer
        
        """

        from gasistafelice.gas.models import GASSupplierOrder
                
        # initialize the return QuerySet 
        qs = GASSupplierOrder.objects.none()
        
        #add the supplier orders opened by a GAS he/she belongs to
        for gas in self.gas_list:
            qs = qs | gas.orders
        
        return qs
        
    
    @property
    def deliveries(self):
        #TODO UNITTEST
        """
        A person is related to:
        1) delivery appointments for which this person is a referrer
        2) delivery appointments associated with a GAS he/she belongs to
        """
        from gasistafelice.gas.models import Delivery
        # initialize the return QuerySet
        qs = Delivery.objects.none()    
        # add  delivery appointments for which this person is a referrer   
        for member in self.gasmembers:
            qs = qs | member.delivery_set.all()
        # add  delivery appointments associated with a GAS he/she belongs to
        for gas in self.gas_list:
            qs = qs | gas.deliveries
                                
        return qs
    
    @property
    def withdrawals(self):
        #TODO UNITTEST
        """
        A person is related to:
        1) withdrawal appointments for which this person is a referrer
        2) withdrawal appointments associated with a GAS he/she belongs to
        """
        from gasistafelice.gas.models import Withdrawal
        # initialize the return QuerySet
        qs = Withdrawal.objects.none()    
        # add  withdrawal appointments for which this person is a referrer   
        for member in self.gasmembers:
            qs = qs | member.withdrawal_set.all()
        # add  withdrawal appointments associated with a GAS he/she belongs to
        for gas in self.gas_list:
            qs = qs | gas.withdrawals
                                
        return qs  
    
    
    ## END Resource API    
    
    @property
    def city(self):
        if self.address:
            return self.address.city 
        else:
            return None

    def setup_accounting(self):
        """ Accounting hierarchy for Person.

		. ROOT (/)
		|----------- wallet [A]
		+----------- incomes [P,I]	+
		|				+--- other (private order, correction, deposit)
		+----------- expenses [P,E]	+
						+--- other (correction, donation, )
        """

        self.subject.init_accounting_system()
        # create a generic asset-type account (a sort of "virtual wallet")
        system = self.accounting.system
        system.get_or_create_account(
            parent_path='/', name='wallet', kind=account_type.asset
        )

        # Expenses and incomes of other kind...
        system.get_or_create_account(
            parent_path='/expenses', name='other', kind=account_type.expense
        )
        system.get_or_create_account(
            parent_path='/incomes', name='other', kind=account_type.income
        )

    #----------------- Authorization API ------------------------#

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new Person in a DES ?
        # * DES administrators
        allowed_users = User.objects.none()
        try:
            des = context['site']
        except KeyError:
            return User.objects.none()
            #raise WrongPermissionCheck('CREATE', cls, context)
        else:
            allowed_users = des.gas_tech_referrers

        return user in allowed_users 
        
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit a Person in a DES ?
        # * the person itself
        # * administrators of one of the DESs this person belongs to
        des_admins = []
        for des in self.des_list:
            des_admins += des.admins
        allowed_users = list(des_admins) + [self.user]
        return user in allowed_users 
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a Person from the system ?
        allowed_users = [self.user]
        return user in allowed_users      
    
        
    #-----------------------------------------------------#

    @property
    def username(self):
        if self.user:
            return self.user.username
        else:
            return ugettext("has not an account in the system")

    display_fields = (
        name, surname, 
        models.CharField(name="city", verbose_name=_("City")),
        models.CharField(name="username", verbose_name=_("Username")),
        #DO NOT SHOW now models.CharField(name="email_address", verbose_name=_("Email")),
        #DO NOT SHOW now models.CharField(name="phone_address", verbose_name=_("Phone")),
        address,
    )
    
    def has_been_member(self, gas):
        """
        Return ``True`` if this person is bound to the GAS ``gas``
        (GASMember exist whether it is suspended or not), 
        ``False`` otherwise. 
        
        If ``gas`` is not a ``GAS`` model instance, raise ``TypeError``.
        """
        from gasistafelice.gas.models import GAS, GASMember
        if not isinstance(gas, GAS):
            raise TypeError(_(u"GAS membership can only be tested against a GAS model instance"))
        return bool(GASMember.all_objects.filter(gas=gas, person=self).count())
    
    def is_member(self, gas):
        """
        Return ``True`` if this person is an active (not suspended) member 
        of GAS ``gas``, ``False`` otherwise. 
        
        If ``gas`` is not a ``GAS`` model instance, raise ``TypeError``.
        """
        from gasistafelice.gas.models import GAS
        if not isinstance(gas, GAS):
            raise TypeError(_(u"GAS membership can only be tested against a GAS model instance"))
        return gas in [member.gas for member in self.gasmembers]
    
    @property
    def full_name(self):
        return self.name + self.surname
    
    def save(self, *args, **kw):
        if not self.display_name:
            self.display_name = u"%(name)s %(surname)s" % {'name' : self.name, 'surname': self.surname}
        super(Person, self).save(*args, **kw)

class Contact(models.Model):
    """If is a contact, just a contact email or phone"""

    flavour = models.CharField(max_length=32, choices=const.CONTACT_CHOICES, default=const.EMAIL,verbose_name=_('flavour'))
    value = models.CharField(max_length=256,verbose_name=_('value'))
    is_preferred = models.BooleanField(default=False,verbose_name=_('preferred'))
    description = models.CharField(max_length=128, blank=True, default='',verbose_name=_('description'))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __unicode__(self):
        return u"%(t)s: %(v)s" % {'t': self.flavour, 'v': self.value}

    def clean(self):
        self.flavour = self.flavour.strip()
        if self.flavour not in map(lambda x: x[0], const.CONTACT_CHOICES):
            raise ValidationError(_("Contact flavour MUST be one of %s" % map(lambda x: x[0],  const.CONTACT_CHOICES)))
        self.value = self.value.strip()
        self.description = self.description.strip()
        return super(Contact, self).clean()

class Place(models.Model, PermissionResource):
    """Places should be managed as separate entities for various reasons:
    * among the entities arising in the description of GAS' activities,
    there are several being places or involving places,
    so abstracting this information away seems a good thing;
    * in the context of multi-GAS (retina) orders,
    multiple delivery and/or withdrawal locations can be present.
    """

    name = models.CharField(max_length=128, blank=True, help_text=_("You can avoid to specify a name if you specify an address"),verbose_name=_('name'))
    description = models.TextField(blank=True,verbose_name=_('description'))

    # QUESTION: add place type from CHOICE (HOME, WORK, HEADQUARTER, WITHDRAWAL...)     
    # ANSWER: no place type here. It is just a point in the map
    address = models.CharField(max_length=128, blank=True,verbose_name=_('address'))

    #zipcode as a string: see http://stackoverflow.com/questions/747802/integer-vs-string-in-database
    zipcode = models.CharField(verbose_name=_("Zip code"), max_length=128, blank=True)

    city = models.CharField(max_length=128,verbose_name=_('city'))
    province = models.CharField(max_length=2, help_text=_("Insert the province code here (max 2 char)"),verbose_name=_('province')) 
        
    #Geolocation: do not use GeoDjango PointField here. 
    #We can make a separate geo application maybe in future
    lon = models.FloatField(null=True, blank=True,verbose_name=_('lon'))
    lat = models.FloatField(null=True, blank=True,verbose_name=_('lat'))

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _("place")
        verbose_name_plural = _("places")
        ordering = ('name', 'address', 'city')

    def __unicode__(self):

        rv = u"" 
        if self.name:
            rv += self.name + u" - "
        if self.address:
            rv += self.address + u", "

        if self.zipcode:
            rv += u"%s " % self.zipcode

        rv += self.city.lower().capitalize()

        if self.province:
            rv += u" (%s)" % self.province.upper()

        return rv

    def clean(self):

        self.name = self.name.strip().lower().capitalize()
        self.address = self.address.strip().lower().capitalize()

        #TODO: we should compute city and province starting from zipcode using local_flavor in forms
        self.city = self.city.lower().capitalize()
        self.province = self.province.upper()

        self.zipcode = self.zipcode.strip()
        if self.zipcode:
            if settings.VALIDATE_NUMERICAL_ZIPCODES:
                try:
                    int(self.zipcode)
                except ValueError:
                    raise ValidationError(_("Wrong ZIP CODE provided"))

        self.description = self.description.strip()

        return super(Place, self).clean()

    def save(self, *args, **kw):

        #TODO: Copy-on-write model
        # a) check if an already existent place with the same full address exist and in that case force update
        # b) if we are updating a Place --> detach it from other stuff pointing to it and clone 

        super(Place, self).save(*args, **kw)
        
    #----------------- Authorization API ------------------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new Place in a DES ?
        # Everyone belongs to the DES
        
        try:
            des = context['site']
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)
        else:
            # It's ok because only one DES is supported
            return not user.is_anonymous()
            # otherwhise it should be
            # return user in User.objects.filter(person__in=des.persons)
                
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of an existing place in a DES ?
        # (note that places can be shared among GASs)
        # * DES administrators
        # * User that created the place
        # * User who has updated it. How he can do it? 
        #   If a User try to create a new place with the same parameters
        #   of an already existent one, he updates the place
        allowed_users =  self.des.admins | self.created_by | self.updaters
        return user in allowed_users
        
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an existing place from a DES ?
        # (note that places can be shared among GASs)
        # * DES administrators
        # * User that created the place
        # * User who has updated it. How he can do it? see can_edit above
        allowed_users =  self.des.admins | self.created_by | self.updaters
        return user in allowed_users       
                
    #-----------------------------------------------------#

    display_fields = (
        name, description, 
        address, zipcode, city, province
    )
    

# Generic workflow management

class DefaultTransition(models.Model, PermissionResource):

    workflow = models.ForeignKey(Workflow, related_name="default_transition_set",verbose_name=_('workflow'))
    state = models.ForeignKey(State,verbose_name=_('state'))
    transition = models.ForeignKey(Transition,verbose_name=_('transition'))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("default transition")
        verbose_name_plural = _("default transitions")

class WorkflowDefinition(object):
    """
    This class encapsulates all the data and logic needed to create and setup a Workflow
    (as in the `django-workflows` app), including creation of States and Transitions,
    assignment of Transitions to States and specification of the initial state and the
    default Transition for each State.
    To setup a new Workflow, just specify the needed data in the declarative format
    described below, then call the `register_workflow` method.
    ## TODO: workflow declaration's specs go here.
    """
    
    def __init__(self, workflow_name, state_list, transition_list, state_transition_map, initial_state, default_transitions):
        # stash the workflow specs for later use
        self.workflow_name = workflow_name
        self.state_list = state_list
        self.transition_list = transition_list
        self.state_transition_map = state_transition_map
        self.initial_state_name = initial_state
        self.default_transitions = default_transitions
            
    def register_workflow(self):
        # check workflow specifications for internal consistency;
        # return an informative error message to the user if the check fails
        try:
            self.check_workflow_specs()
        except ImproperlyConfigured, e:
            raise ImproperlyConfigured(_("Workflow specifications are not consistent.\n %s") % e)
            
        try:
            # Check for already existent workflow. Operation `register_workflow` is idempotent...
            Workflow.objects.get(name=self.workflow_name)

        except Workflow.DoesNotExist:
            # Initialize workflow

            self.workflow = Workflow.objects.create(name=self.workflow_name)
            ## create States objects
            self.states = {} # dictionary containing State objects for our Workflow
            for (key, name) in self.state_list:
                self.states[key] = State.objects.create(name=name, workflow=self.workflow)
            ## create Transition objects
            self.transitions = {} # dictionary containing Transition objects for the current Workflow
            for (key, transition_name, destination_name) in self.transition_list:
                dest_state = self.states[destination_name]
                self.transitions[key] = Transition.objects.create(name=transition_name, workflow=self.workflow, destination=dest_state)
            ## associate Transitions to States
            for (state_name, transition_name) in self.state_transition_map:
                log.debug("Workflow %(w)s, adding state=%(s)s transition=%(t)s" % {
                    'w' : self.workflow_name,
                    's' : state_name, 
                    't' : transition_name,
                })
                state = self.states[state_name]
                transition = self.transitions[transition_name]
                state.transitions.add(transition)
            ## set the initial State for the Workflow
            state = self.states[self.initial_state_name]
            self.workflow.initial_state = state
            self.workflow.save()
            ## define default Transitions for States in a Workflow,
            ## so we can suggest to end-users what the next "logical" State could be
            for (state_name, transition_name) in self.default_transitions:
                state = self.states[state_name]
                transition = self.transitions[transition_name]
                self.workflow.default_transition_set.add(DefaultTransition(state=state, transition=transition))
    
    def check_workflow_specs(self):
        """Check the provided workflow specifications for internal consistency.

        Return True if the specs are fine, False otherwise.
        """

        state_names = [key for (key, name) in self.state_list]
        transition_names = [key for (key, transition_name, destination_name) in self.transition_list]
        ## States have to be unique
        # TODO
        ## Transitions have to be unique
        # TODO
        ## a Transition must point to an existing State
        for (key, transition_name, destination_name) in self.transition_list:
            if destination_name not in state_names:
                raise ImproperlyConfigured("Transition %s points to the non-existent State %s" % (key, destination_name))
        ## a Transition must be assigned to an existing State
        for (state_name, transition_name) in self.state_transition_map:
            if state_name not in state_names:
                raise ImproperlyConfigured("Transition %s can't be assigned to the non-existent State %s" % (transition_name, state_name))
        ## initial State must exists
        if self.initial_state_name not in state_names:
            raise ImproperlyConfigured("Workflow %s: initial state %s must be included in state names %s" % (self.workflow_name, self.initial_state_name, state_names))
        ## a default Transition for a State must exists and had to be previously assigned to that State
        for (state_name, transition_name) in self.default_transitions:
            if state_name not in state_names:
                raise ImproperlyConfigured("A default Transition can't be defined for the non-existent State %s" % state_name)
            elif transition_name not in transition_names:
                raise ImproperlyConfigured("The default Transition for the State %s can't be set to a non-existent Transitions %s" % (state_name, transition_name))
            elif (state_name, transition_name) not in self.state_transition_map:
                raise ImproperlyConfigured("The default Transition for the State %s must be one of its valid Transitions" % state_name)


#-------------------------------------------------------------------------------

#This is an HACK used just because we need these users use parts of the web admin interface
from gasistafelice.consts import GAS_MEMBER , GAS_REFERRER_TECH, SUPPLIER_REFERRER
from django.contrib.auth.models import Group, Permission

# groups for users
GROUP_TECHS = "techs"
GROUP_SUPPLIERS = "suppliers"
GROUP_REFERRER_SUPPLIERS = "gas_referrer_suppliers"
GROUP_USERS = "users"
GROUP_MEMBERS = "gasmembers"

def init_perms_for_groups():

    from gasistafelice.base.models import Person, Place, Contact
    from gasistafelice.gas.models import GAS, GASConfig, GASMember
    from gasistafelice.supplier.models import (
        SupplierConfig, SupplierProductCategory, ProductCategory,
        SupplierStock, Product, Supplier
    )
    from django.contrib.auth.models import User
    from django.contrib.auth.management import _get_permission_codename
    
    g_techs = Group.objects.get(name=GROUP_TECHS)
    g_suppliers = Group.objects.get(name=GROUP_SUPPLIERS)
    g_referrers_suppliers = Group.objects.get(name=GROUP_REFERRER_SUPPLIERS)
    g_gasmembers = Group.objects.get(name=GROUP_MEMBERS)

    techs_perms_d = {
        Person : ('add', 'change', 'delete'),
        Place : ('add', 'change', 'delete'),
        Contact : ('add', 'change', 'delete'),
        GAS : ('change',),
        GASConfig : ('change',),
        SupplierConfig : ('change',),
        GASMember : ('add', 'change', 'delete'),
        SupplierProductCategory : ('add', 'change', 'delete'),
        ProductCategory : ('add', 'change', 'delete'),
        SupplierStock : ('add', 'change', 'delete'),
        Product : ('add', 'change', 'delete'),
        Supplier : ('add', 'change'),
        User : ('add', 'change',), # add User is important for Add GASMember Form! Leave it here now. TODO
    }

    supplier_perms_d = {
        Person : ('add', 'change'),
        Place : ('add', 'change'),
        Contact : ('add', 'change'),
        SupplierConfig : ('change',),
        SupplierProductCategory : ('add', 'change', 'delete'),
        SupplierStock : ('add', 'change', 'delete'),
        Product : ('add', 'change', 'delete'),
        Supplier : ('change',),
    }

    gas_referrer_supplier_perms_d = supplier_perms_d.copy()
    gas_referrer_supplier_perms_d.update({
        Supplier : ('add', 'change'),
    })

    gm_perms_d = {
        Person : ('change',),
        Place : ('add', 'change',),
        Contact : ('add', 'change',),
    }

    group_perms_d_tuples = (
        (g_techs , techs_perms_d),
        (g_suppliers , supplier_perms_d),
        (g_referrers_suppliers , gas_referrer_supplier_perms_d),
        (g_gasmembers , gm_perms_d),
    )

    for gr, perms_d in group_perms_d_tuples:
        for klass, actions in perms_d.items():
            ctype = ContentType.objects.get_for_model(klass)
            for action in actions:
                codename = _get_permission_codename(action, klass._meta)
                log.debug("Adding perm %s to group %s" % (codename, gr))
                p = Permission.objects.get(
                    content_type=ctype, codename=codename
                )
                gr.permissions.add(p)

def setup_data_handler(sender, instance, created, **kwargs):
    """ Ovverride temporarly for associating some groups to users

    This will be in use until some part of the interface use admin-interface.
    After this can be removed
    """

    if created:

        # Check that groups exist. Create them the first time

        g_techs, created = Group.objects.get_or_create(name=GROUP_TECHS)
        g_suppliers, created = Group.objects.get_or_create(name=GROUP_SUPPLIERS)
        g_referrers_suppliers, created = Group.objects.get_or_create(name=GROUP_REFERRER_SUPPLIERS)
        g_gasmembers, created = Group.objects.get_or_create(name=GROUP_MEMBERS)

        if created:

            # Create all groups needed for this hack
            # Check only last...
            init_perms_for_groups()

        role_group_map = {
            GAS_MEMBER : g_gasmembers,
            GAS_REFERRER_SUPPLIER : g_referrers_suppliers,
            SUPPLIER_REFERRER : g_suppliers,
            GAS_REFERRER_TECH : g_techs,
        }

        # Set "is_staff" to access the admin inteface
        instance.user.is_staff = True
        instance.user.save()

        role_name = instance.role.role.name
        group = role_group_map.get(role_name)
        if group:
            try:
                instance.user.groups.add(group)
            except KeyError:
                log.debug("%s create cannot add %s's group %s(%s)" % 
                    (role_name, group, instance, instance.pk)
                )
# END hack
        
#-------------------------------------------------------------------------------


def validate(sender, instance, **kwargs):
        try:
            # `instance` is the model instance that has just been created
            instance.clean()
        except AttributeError:
            # sender model doesn't specify any sanitize operations, so just ignore the signal
            pass


def setup_data(sender, instance, created, **kwargs):
    """
    Setup proper data after a model instance is saved to the DB for the first time.
    This function just calls the `setup_data()` instance method of the sender model class (if defined);
    actual role-creation/setup logic is encapsulated there.
    """
    if created: # Automatic data-setup should happen only at instance-creation time 

        try:
            # `instance` is the model instance that has just been created
            instance.setup_data()
                                                
        except AttributeError:
            # sender model doesn't specify any data-related setup operations, so just ignore the signal
            pass

# add `validate` function as a listener to the `pre_save` signal
pre_save.connect(validate)

# add `setup_data` function as a listener to the `post_save` signal
post_save.connect(setup_data)
post_save.connect(setup_data_handler, sender=PrincipalParamRoleRelation)
