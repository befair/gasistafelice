"""This is the base model for Gasista Felice. 

It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from gasistafelice.base.const import CONTACT_CHOICES
from permissions import PermissionBase # mix-in class for permissions management
from permissions.models import Permission, Role as BaseRole 
from workflows.models import Workflow, Transition, State
from django.db.models.fields.related import ManyToManyField, ForeignKey

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
    contacts = models.ManyToManyField('Contact')
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)
   
class Contact(Resource, PermissionBase, models.Model):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

class Role(Resource, BaseRole):
    """
    A custom `Role` model class inheriting from `django-permissions`'s`Role` model.
    
    This way, we are able to augment the base `Role` model 
    (carrying only a `name` field attribute) with additional information
    needed to describe those 'parametric' roles arising in this application domain
    (e.g. GAS' supplier|tech|cash referrers).    
    """
    # link to the base model class (`BaseRole`)
    base_role = models.OneToOneField(BaseRole, parent_link=True)
    # a Role can be tied to a given GAS (e.g. GAS_REFERRER_CASH, GAS_REFERRER_TECH)
    gas = models.ForeignKey('gas.models.GAS', null=True, blank=True) 
    # a Role can be tied to a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER)
    supplier = models.ForeignKey('supplier.models.Supplier', null=True, blank=True)
    # a Role can be tied to a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
    delivery = models.ForeignKey('gas.models.order.Delivery', null=True, blank=True)
    # a Role can be tied to a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
    withdrawal = models.ForeignKey('gas.models.order.Withdrawal', null=True, blank=True)
    # a Role can be tied to a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
    order = models.ForeignKey('gas.models.order.GASSupplierOrder', null=True, blank=True)
    #TODO: roles can be retina-specific
    #retina = ForeignKey('gas.models.retina')
    class Meta:
        # forbid duplicated Role entries in the DB
        unique_together = ("base_role", "gas", "supplier", "delivery", "withdrawal", "order")
        
class GlobalPermission(models.Model):
    permission = models.ForeignKey(Permission)
    role = models.ForeignKey(BaseRole)
    content_type = models.ForeignKey(ContentType)
    class Meta:
        # forbid duplicated GlobalPermission entries in the DB
        unique_together = ("permission", "role", "content_type")

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

