from django.db import models


from django.contrib.contenttypes.models import ContentType

from permissions.models import Permission, Role as BaseRole

from gasistafelice.base.models import Resource
from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
from gasistafelice.supplier.models import Supplier


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
    gas = models.ForeignKey(GAS, null=True, blank=True)
    # a Role can be tied to a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    # a Role can be tied to a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
    delivery = models.ForeignKey(Delivery, null=True, blank=True)
    # a Role can be tied to a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
    withdrawal = models.ForeignKey(Withdrawal, null=True, blank=True)
    # a Role can be tied to a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
    order = models.ForeignKey(GASSupplierOrder, null=True, blank=True)
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
