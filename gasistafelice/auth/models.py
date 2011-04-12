from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from permissions.models import Permission, Role as BaseRole

from gasistafelice.base.models import Resource
#from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
#from gasistafelice.supplier.models import Supplier


class Role(Resource, BaseRole):
    """
    A custom `Role` model class inheriting from `django-permissions`'s`Role` model.
    This way, we are able to augment the base `Role` model
    (carrying only a `name` field attribute) with additional information
    needed to describe those 'parametric' roles arising in this application domain.
    
     A (parametric) Role can be tied to:
     
     1) a given GAS (e.g. GAS_REFERRER_CASH, GAS_REFERRER_TECH),
     2) a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER),
     3) a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
     4) a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
     5) a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
     6) a given "Retina" (TODO)
    
    """
    # link to the base model class (`BaseRole`)
    base_role = models.OneToOneField(BaseRole, parent_link=True)
    ## Generic ForeignKey for the first (optional) Role parameter
    content_type_1 = models.ForeignKey(ContentType)
    obj_id_1 = models.PositiveIntegerField()
    param1 = generic.GenericForeignKey(ct_field="content_type_1", fk_field="obj_id_1")
    ## Generic ForeignKey for the second (optional) Role parameter
    content_type_2 = models.ForeignKey(ContentType, null=True, blank=True)
    obj_id_2 = models.PositiveIntegerField(null=True, blank=True)
    param2 = generic.GenericForeignKey(ct_field="content_type_2", fk_field="obj_id_2")

        
class GlobalPermission(models.Model):
    permission = models.ForeignKey(Permission)
    role = models.ForeignKey(BaseRole)
    content_type = models.ForeignKey(ContentType)
    class Meta:
        # forbid duplicated GlobalPermission entries in the DB
        unique_together = ("permission", "role", "content_type")
