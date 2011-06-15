"""These models include everything necessary to manage GAS activity.

They rely on base models and Supplier-related ones to get Product and Stock infos.

Definition: `Vocabolario - GAS <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#GAS>`__ (ITA only)
"""
 
from django.db.models.signals import post_save
from django.dispatch import receiver


from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact, GASConfig
from gasistafelice.gas.models.order import GASSupplierOrder, GASSupplierOrderProduct, GASMemberOrder, Delivery, Withdrawal

@receiver(post_save, sender=GASSupplierSolidalPact)
def auto_select_all_products_if_configured(sender, instance, created, **kwargs):
    try:
        if created and instance.gas.config.auto_select_all_products:
            for p in instance.supplier.supplierstock_set.all():
                p.gassupplierstock_set.add(gas=instance.gas)
    except GASConfig.DoesNotExist: # if GAS configuration is not defined, do nothing
        pass
    