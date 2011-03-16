"""Order management. Includes state machine."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base.models import Person, Role
from gasistafelice.supplier.models import Supplier, SupplierStock
from gasistafelice.gas.const import STATES_LIST

class State(models.Model):

    name = models.CharField(max_length=128) 
    value = models.IntegerField() 
    description = models.TextField(blank=True)

    action_set = models.ManyToManyField(Action, through="StateActionMap")

    def __unicode__(self):
        return self.name

class Action(models.Model):
    
    name = models.CharField(max_length=128) 
    value = models.IntegerField() 
    description = models.TextField(blank=True)

    states_set = models.ManyToManyField(State, through="StateActionMap")

    def __unicode__(self):
        return self.name

class StateActionMap(models.Model):

    from_state = models.ForeignKey(State)
    input_action = models.ForeignKey(Action)
    to_state = models.ForeignKey(State)
     
class Workflow(models.Model):
    
    name = models.CharField(max_length=128) 
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class WorkflowStep(models.Model):

    workflow = models.ForeignKey(Workflow)
    
    
    auto = models.BooleanField(default=False)

    

