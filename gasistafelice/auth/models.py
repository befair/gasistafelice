from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from gasistafelice.base.utils import get_ctype_from_model_label
from permissions.models import Permission, Role

from gasistafelice.base.models import Resource
#from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
#from gasistafelice.supplier.models import Supplier


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
    ## Generic ForeignKey for the first (optional) Role parameter
    content_type_1 = models.ForeignKey(ContentType, related_name="param_role_primary_set")
    obj_id_1 = models.PositiveIntegerField()
    param1 = generic.GenericForeignKey(ct_field="content_type_1", fk_field="obj_id_1")
    ## Generic ForeignKey for the second (optional) Role parameter
    content_type_2 = models.ForeignKey(ContentType, null=True, blank=True, related_name="param_role_secondary_set")
    obj_id_2 = models.PositiveIntegerField(null=True, blank=True)
    param2 = generic.GenericForeignKey(ct_field="content_type_2", fk_field="obj_id_2")
    class Meta:
        # forbid duplicated ParamRole entries in the DB
        unique_together = ("role", "content_type_1", "obj_id_1", "content_type_2", "obj_id_2")
        
    @property
    def gas(self):
        gas_ct = get_ctype_from_model_label('gas.GAS')
        GAS = gas_ct.model_class()
        if  self.content_type_1 == gas_ct:
            try:
                gas = GAS.objects.get(pk=self.obj_id_2)
                return gas
            except GAS.DoesNotExist:
                return None    
        elif self.content_type_2 == gas_ct:
            try:
                gas = GAS.objects.get(pk=self.obj_id_2)
                return gas
            except GAS.DoesNotExist:
                return None
        else:
            return None
    
    @property
    def supplier(self):
        supplier_ct = get_ctype_from_model_label('supplier.Supplier')
        Supplier = supplier_ct.model_class()
        if  self.content_type_1 == supplier_ct:
            try:
                supplier = Supplier.objects.get(pk=self.obj_id_1)
                return supplier
            except Supplier.DoesNotExist:
                return None    
        elif self.content_type_2 == supplier_ct:
            try:
                supplier = Supplier.objects.get(pk=self.obj_id_2)
                return supplier
            except Supplier.DoesNotExist:
                return None
        else:
            return None

    @property
    def order(self):
        order_ct = get_ctype_from_model_label('gas.GASSupplierOrder')
        GASSupplierOrder = order_ct.model_class()
        if  self.content_type_1 == order_ct:
            try:
                order = GASSupplierOrder.objects.get(pk=self.obj_id_1)
                return order
            except GASSupplierOrder.DoesNotExist:
                return None    
        elif self.content_type_2 == order_ct:
            try:
                order = GASSupplierOrder.objects.get(pk=self.obj_id_2)
                return order
            except GASSupplierOrder.DoesNotExist:
                return None
        else:
            return None

#    @property
#    def delivery(self):
#        ...

#    @property
#    def withdrawal(self):
#        ...

     
class GlobalPermission(models.Model):
    permission = models.ForeignKey(Permission)
    role = models.ForeignKey(Role)
    content_type = models.ForeignKey(ContentType)
    class Meta:
        # forbid duplicated GlobalPermission entries in the DB
        unique_together = ("permission", "role", "content_type")
