""""
This is the base model for Gasista Felice.
It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models import permalink
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from workflows.models import Workflow, Transition, State
from history.models import HistoricalRecords

from gasistafelice.consts import GAS_REFERRER_ORDER, GAS_REFERRER_SUPPLIER
from flexi_auth.models import PermissionBase # mix-in class for permissions management
from flexi_auth.exceptions import WrongPermissionCheck
from flexi_auth.utils import get_parametric_roles

from gasistafelice.lib import ClassProperty, unordered_uniq
from gasistafelice.base import const
from gasistafelice.base.utils import get_resource_icon_path

from workflows.utils import do_transition
import os

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
       
        # There could be the case that a deleted id is reused, so, do not use .get method
        self_as_of_last_update = \
            self._default_history.filter(id=self.pk, history_type="~")[0]

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
       
        self_updaters = \
            unordered_uniq(self._default_history.filter(id=self.pk, history_type="~").values_list('history_user'))

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
        raise NotImplementedError("class: %s method: des" % self.__class__.__name__)

    @property
    def gas_list(self):
        """Return GAS list bound to resource"""
        raise NotImplementedError("class: %s method: gas_list" % self.__class__.__name__)

    @property
    def gas(self):
        """Return GAS bound to resource"""
        raise NotImplementedError("class: %s method: gas" % self.__class__.__name__)

    @property
    def accounts(self):
        """Return economic state bound to resource  (DES, GASMember, GAS or Supplier through )"""
        raise NotImplementedError("class: %s method: accounts" % self.__class__.__name__)

    @property
    def account(self):
        """Return an economic state bound to resource (DES, GASMember, GAS or Supplier through )"""
        raise NotImplementedError("class: %s method: account" % self.__class__.__name__)

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
    def preferred_email_address(self):
        """The email address, where we should write if we would know more info on the resource.

        It is not necessarily bound to a person. 

        NOTE that it could be even a list of addresses following syntax in RFC 5322 and RFC 5321,
        or simply http://en.wikipedia.org/wiki/Email_address#Syntax :)

        Usually you SHOULD NOT NEED TO OVERRIDE IT in subclasses
        """
        return ", ".join(ordered_uniq(map(lambda x: x[0], self.preferred_email_contacts.values_list('value'))))

    @property
    def preferred_email_contacts(self):
        """Email Contacts, where we should write if we would know more info on the resource.

        It is not necessarily bound to a person. 

        Usually you SHOULD NOT NEED TO OVERRIDE IT in subclasses
        """
        return self.contacts.filter(flavour=const.EMAIL, is_preferred=True) or \
                    self.contacts.filter(flavour=const.EMAIL)

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
#
#    @property
#    def transacts(self):
#        """Return transact list bound to resource"""
#        raise NotImplementedError
#
#    @property
#    def transact(self):
#        """Return transact bound to resource"""
#        raise NotImplementedError
#

class PermissionResource(Resource, PermissionBase):
    """
    Just a convenience for classes inheriting both from `Resource` and `PermissionBase`
    """
    pass

class Person(models.Model, PermissionResource):
    """
    A Person is an anagraphic record of a human being.
    It can be a User or not.
    """

    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, blank=True)
    #TODO: Verify if this information is necessary
    #uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    uuid = models.CharField(max_length=128, unique=True, editable=False, blank=True, null=True, help_text=_('Write your social security number here'))
    contact_set = models.ManyToManyField('Contact', null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True)
    address = models.OneToOneField('Place', null=True, blank=True)
    avatar = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __unicode__(self):
        return self.display_name or u'%(name)s %(surname)s' % {'name' : self.name, 'surname': self.surname}

    @property
    def icon(self):
        return self.avatar 

    ## START Resource API
    # Note that all the following methods return a QuerySet
    
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
        gas_set = set([member.gas for member in self.gasmembers])
        return GAS.objects.filter(pk__in=[obj.pk for obj in gas_set])
    
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
    def pacts(self):
        # TODO: what pacts are associated to a Person ?
        pass
    
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
        referred_set = set([sr.supplier for sr  in self.supplieragent_set])
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
        
        if self.user: #if a Person has not an account, he can't have any role in the system
            # retrieve all parametric roles assigned to this person
            roles = get_parametric_roles(self.user)
            for pr in roles:
                # add the supplier orders for which this person is a referrer
                if pr.role.name == GAS_REFERRER_ORDER:
                    qs = qs | GASSupplierOrder.objects.get(pk=pr.order.pk)
                # add orders to suppliers for which this person is a referrer
                if pr.role.name == GAS_REFERRER_SUPPLIER:
                    GASSupplierOrder.objects.filter(pact__gas=pr.gas, pact__supplier=pr.supplier)
                
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
        return self.address.city 

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.surname = self.surname.capitalize()
        if self.uuid == '':
            self.uuid = None
        super(Person, self).save(*args, **kwargs)
        
    #----------------- Authorization API ------------------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new Person in a DES ?
        # * DES administrators
        try:
            des = context['des']
            allowed_users = des.admins            
            return user in allowed_users 
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)
        
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
   
class Contact(models.Model):

    flavour = models.CharField(max_length=32, choices=const.CONTACT_CHOICES, default=const.EMAIL)
    value = models.CharField(max_length=32)
    is_preferred = models.BooleanField(default=False)
    description = models.CharField(max_length=128, blank=True, default='')

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __unicode__(self):
        return u"%(t)s: %(v)s" % {'t': self.flavour, 'v': self.value}

class Place(models.Model, PermissionResource):
    """Places should be managed as separate entities for various reasons:
    * among the entities arising in the description of GAS' activities,
    there are several being places or involving places,
    so abstracting this information away seems a good thing;
    * in the context of multi-GAS (retina) orders,
    multiple delivery and/or withdrawal locations can be present.
    """

    name = models.CharField(max_length=128, blank=True, help_text=_("You can avoid to specify a name if you specify an address"))
    description = models.TextField(blank=True)
    #TODO: ADD place type from CHOICE (HOME, WORK, HEARTHQUARTER, WITHDRAWAL...)     
    address = models.CharField(max_length=128, blank=True)
    zipcode = models.CharField(verbose_name=_("Zip code"), max_length=128, blank=True)

    city = models.CharField(max_length=128)
    province = models.CharField(max_length=2, help_text=_("Insert the province code here (max 2 char)")) 
        
    #TODO geolocation: use GeoDjango PointField?
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _("place")
        verbose_name_plural = _("places")

    def __unicode__(self):
        return _("%(name)s in %(city)s (%(pr)s)") % {
                    'name' : self.name or self.address, 
                    'city' : self.city,
                    'pr' : self.province,
        }

    def save(self, *args, **kw):

        #TODO: check if an already existent place with the same full address exist and in that case force update

        #TODO: we should compute city and province starting from zipcode using local_flavor in forms
        self.city = self.city.capitalize()
        self.province = self.province.upper()

        if not self.name:
            # Separate check for name and address because we must set a name for a place.
            # Otherwise error occurs.
            if self.address:
                self.name = self.address
            else:
                raise ValueError("Name or address should be set for a Place")

        super(Place, self).save(*args, **kw)
        
    #----------------- Authorization API ------------------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new Place in a DES ?
        # * DES administrators
        # * GAS members
        # * Suppliers 
        
        try:
            des = context['des']
            all_gas_members = set()
            for gas in des.gas_list:
                all_gas_members = all_gas_members | gas.members 
            all_suppliers = set()
            for supplier in des.suppliers:
                all_suppliers = all_suppliers | supplier.referrers
            allowed_users =  des.admins | all_gas_members | all_suppliers
            return user in allowed_users 
        except KeyError:
            raise WrongPermissionCheck('CREATE', self, context)
                
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

# Generic workflow management

class DefaultTransition(models.Model, PermissionResource):

    workflow = models.ForeignKey(Workflow, related_name="default_transition_set")
    state = models.ForeignKey(State)
    transition = models.ForeignKey(Transition)

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
        """
Check the provided workflow specifications for internal consistency;
return True if the specs are fine, False otherwise.
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


