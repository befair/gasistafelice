""""
This is the base model for Gasista Felice.
It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from permissions import PermissionBase # mix-in class for permissions management
from workflows.models import Workflow, Transition, State
from history.models import HistoricalRecords

from gasistafelice.base.const import CONTACT_CHOICES


class Resource(object):
    """
A basic mix-in class used to factor out data/behaviours common
to the majority of model classes in the project's applications.
"""

class PermissionResource(Resource, PermissionBase):
    """
Just a convenience for classes inheriting both from Resource and PermissionBase
"""
    pass

class Person(models.Model, PermissionResource):
    """A Person is an anagraphic record of a human being.
It can be a User or not.
"""

    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    #TODO: Verify if this information is necesary
    #uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    uuid = models.CharField(max_length=128, unique=True, editable=False, blank=True, null=True, help_text=_('Write your social security number here'))
    contacts = models.ManyToManyField('Contact', null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True)
    address = models.OneToOneField('Place')

    history = HistoricalRecords()

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname) 

    @property
    def city(self):
        return self.address.city 

    def save(self, force_insert=False, force_update=False):
        self.name = self.name.upper()
        self.surname = self.surname.title() #capitalized
        if self.uuid == "":
            self.uuid = None
        if self.pk is None:
            if len(self.address.name) == 0:
                self.address.name = _("main address")
            if len(self.address.description) == 0:
                self.address.description = _("auto insert from admin interface")
        super(Person, self).save(force_insert, force_update)

   
class Contact(models.Model, PermissionResource):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

    history = HistoricalRecords()

class Place(models.Model, PermissionResource):
    """Places should be managed as separate entities for various reasons:
* among the entities arising in the description of GAS' activities,
there are several being places or involving places,
so abstracting this information away seems a good thing;
* in the context of multi-GAS (retina) orders,
multiple delivery and/or withdrawal locations can be present.
"""
    name = models.CharField(max_length=128, blank=True, editable=False)
    description = models.TextField(blank=True, editable=False)
    address = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=2, help_text=_("Insert the province code here (max 2 char)"))
        
    #TODO geolocation: use GeoDjango PointField?
    #If we want to allow blank values in a date or numeric field, we will need to use both null=True and blank=True.
    lon = models.FloatField(null=True, blank=True, editable=False)
    lat = models.FloatField(null=True, blank=True, editable=False)

    history = HistoricalRecords()

    def __unicode__(self):
        return u"%s (%s)" % (self.city, self.province)

    def save(self, force_insert=False, force_update=False):
        self.city = self.city.upper()
        self.province = self.province.upper()
        #if self.pk is not None:
        #    orig = Place.objects.get(pk=self.pk)
        #    if orig.city != self.city and len(self.city) > 0:
        #if len(self.lon) == 0:
        #    self.lon = 
        super(Place, self).save(force_insert, force_update)


# Generic workflow management

class DefaultTransition(models.Model, PermissionResource):

    workflow = models.ForeignKey(Workflow, related_name="default_transition_set")
    state = models.ForeignKey(State)
    transition = models.ForeignKey(Transition)

    history = HistoricalRecords()

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
            self.states[key] = State.objects.create(name=_(name), workflow=self.workflow)
        ## create Transition objects
        self.transitions = {} # dictionary containing Transition objects for the current Workflow
        for (key, transition_name, destination_name) in self.transition_list:
            dest_state = self.states[destination_name]
            self.transitions[key] = Transition.objects.create(name=_(transition_name), workflow=self.workflow, destination=dest_state)
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



class AbstractClass(models.Model):
    created_at=models.DateField(_("Created at"))
    created_by=models.ForeignKey(User, db_column="created_by", related_name=_("%(app_label)s_%(class)s_created"))
    updated_at=models.DateTimeField(_("Updated at"))
    updated_by=models.ForeignKey(User, db_column="updated_by", null=True, related_name=_("%(app_label)s_%(class)s_updated"))
    class Meta:
        abstract = True
    
class Document(AbstractClass):
    """
    General document that refers to a special entity
    """
    DOC_TYPE = (
        ('gas', 'GAS'),
        ('supplier', 'SUPPLIER'),
        ('product', 'PRODUCT'),
        ('member', 'MEMBER'),
        ('pds', 'PDS'),
        ('order', 'ORDER'),
    )
    name = models.CharField(max_length=300, help_text=_("title and brief description"))
    type_doc = models.CharField(max_length=1, choices=DOC_TYPE)
    #TODO: how to access to a volatile foreign key 
    parent_class_id = models.AutoField(primary_key=True)
    file_doc = models.FileField(upload_to='docs/%Y/%m/%d')
    date = models.DateField()

    class Meta:
        app_label = 'doc'


