"""This is the base model for Gasista Felice. 

It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from gasistafelice.base.const import CONTACT_CHOICES
from workflows.models import Workflow, Transition

class Person(models.Model):
    """A Person is an anagraphic record of a human being.
    It can be a User or not.
    """

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    contacts = models.ManyToManyField('Contact')
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)
   
class Contact(models.Model):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

class Role(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()


class Place(models.Model):
    """Places should be managed as separate entities for various reasons:
    * among the entities arising in the description of GAS' activities, 
      there are several being places or involving places, 
      so abstracting this information away seems a good thing;
    * in the context of multi-GAS (retina) orders,  
      multiple delivery and/or withdrawal locations can be present.  
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
        
    #TODO geolocation: use GeoDjango PointField?
    lon = models.FloatField(blank=True)
    lat = models.FloatField(blank=True)


# Generic workflow management

class WorkflowDefaultTransitionOrder(models.Model):

    workflow = models.ForeignKey(Workflow)
    transition = models.ForeignKey(Transition)
    order = models.PositiveIntegerField()

