from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from gasistafelice.base.utils import get_ctype_from_model_label
from permissions.models import Permission, Role

from gasistafelice.base.models import Resource
#from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
#from gasistafelice.supplier.models import Supplier

class Param(models.Model):
    """
    A trivial wrapper model class around a generic ForeignKey; 
    used to create (parametric) Roles with more than one parameter.  
    """
    # TODO: validate parameter names (they should belongs to a predefined list,
    # e.g. 'gas', 'supplier', 'order', ..)
    name = models.CharField(max_lenght=20)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    param = generic.GenericForeignKey(ct_field="content_type", fk_field="obj_id")

class ParamRole(Resource, Role):
    """
    A custom role model class inheriting from `django-permissions`'s`Role` model.
    This way, we are able to augment the base `Role` model
    (carrying only a `name` field attribute) with additional information
    needed to describe those 'parametric' roles arising in this application domain.
    
     A parametric role (`ParamRole`) can be tied to:
     
     1) a given GAS (e.g. GAS_REFERRER_CASH, GAS_REFERRER_TECH),
     2) a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER),
     3) a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
     4) a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
     5) a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
     6) a given "Retina" (TODO)
    
    """
    # link to the base model class (`BaseRole`)
    role = models.OneToOneField(Role, parent_link=True)
    # parameters for this Role
    param_set = models.ManyToManyField(Param)
    
    ## we define a few properties providing easier access to allowed role parameters            
    # note that access is read-only; parameter assignment is managed by the 
    #`register_parametric_role()` factory function
    
    @property 
    def gas(self):
        """
        If this role has a 'gas' parameter, return it; else return None. 
        """
        # examine all the parameters attached to this role 
        # and see if there is one named 'gas'
        for p in self.param_set.all():
            if p.name == 'gas':
                gas = p.param
                return gas
        return None
                
    @property 
    def supplier(self):
        """
        If this role has a 'supplier' parameter, return it; else return None. 
        """
        # examine all the parameters attached to this role 
        # and see if there is one named 'supplier'
        for p in self.param_set.all():
            if p.name == 'supplier':
                supplier = p.param
                return supplier
        return None
    
    
    @property 
    def order(self):
        """
        If this role has an 'order' parameter, return it; else return None. 
        """
        # examine all the parameters attached to this role 
        # and see if there is one named 'order'
        for p in self.param_set.all():
            if p.name == 'order':
                order = p.param
                return order
        return None
    
    @property 
    def delivery(self):
        """
        If this role has a 'delivery' parameter, return it; else return None. 
        """
        # examine all the parameters attached to this role 
        # and see if there is one named 'delivery'
        for p in self.param_set.all():
            if p.name == 'delivery':
                delivery = p.param
                return delivery
        return None
    
    @property 
    def withdrawal(self):
        """
        If this role has an 'withdrawal' parameter, return it; else return None. 
        """
        # examine all the parameters attached to this role 
        # and see if there is one named 'withdrawal'
        for p in self.param_set.all():
            if p.name == 'withdrawal':
                withdrawal = p.param
                return withdrawal
        return None
        
     
class GlobalPermission(models.Model):
    permission = models.ForeignKey(Permission)
    role = models.ForeignKey(Role)
    content_type = models.ForeignKey(ContentType)
    class Meta:
        # forbid duplicated GlobalPermission entries in the DB
        unique_together = ("permission", "role", "content_type")
