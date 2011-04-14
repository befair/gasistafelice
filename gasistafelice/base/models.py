"""
This is the base model for Gasista Felice.
It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from permissions import PermissionBase # mix-in class for permissions management
from workflows.models import Workflow, Transition, State

from gasistafelice.base.const import CONTACT_CHOICES


class Resource(object):
    """
    A basic mix-in class used to factor out data/behaviours common
    to the majority of model classes in the project's applications.
    """
    pass

class Person(Resource, PermissionBase, models.Model):
    """A Person is an anagraphic record of a human being.
    It can be a User or not.
    """

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    contacts = models.ManyToManyField('Contact', null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)
   
class Contact(Resource, PermissionBase, models.Model):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

class Place(Resource, PermissionBase, models.Model):
    """Places should be managed as separate entities for various reasons:
    * among the entities arising in the description of GAS' activities,
    there are several being places or involving places,
    so abstracting this information away seems a good thing;
    * in the context of multi-GAS (retina) orders,
    multiple delivery and/or withdrawal locations can be present.
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    province = models.CharField(max_length=128, blank=True)
        
    #TODO geolocation: use GeoDjango PointField?
    lon = models.FloatField(blank=True)
    lat = models.FloatField(blank=True)


# Generic workflow management

class DefaultTransition(Resource, PermissionBase, models.Model):

    workflow = models.ForeignKey(Workflow, related_name="default_transition_set")
    state = models.ForeignKey(State)
    transition = models.ForeignKey(Transition)

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
            raise ImproperlyConfigured("Workflow specifications are not consistent.\n" + e)
            
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
            self.workflow.default_transition_set.add(state, transition)
    
            
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
            raise ImproperlyConfigured("Initial state %s must exists" % self.initial_state_name)
        ## a default Transition for a State must exists and had to be previously assigned to that State
        for (state_name, transition_name) in self.default_transitions:
            if state_name not in state_names:
                raise ImproperlyConfigured("A default Transition can't be defined for the non-existent State %s" % state_name)
            elif transition_name not in transition_names:
                raise ImproperlyConfigured("The default Transition for the State %s can't be set to a non-existent Transitions %s" % (state_name, transition_name))
            elif (state_name, transition_name) not in self.state_transition_map:
                raise ImproperlyConfigured("The default Transition for the State %s must be one of its valid Transitions" % state_name)
