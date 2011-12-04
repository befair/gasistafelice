
from django.contrib.admin.sites import AdminSite
from django.contrib import admin

from gasistafelice.base import models as base_models
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models
from simple_accounting import models as accounting_models

from gasistafelice.gas_admin.models.base import *
from gasistafelice.gas_admin.models.gas import *


class GasAdminSite(AdminSite):

    index_template = "gas_admin/index.html"

gas_admin = GasAdminSite("gas_admin")
gas_admin.register(base_models.Place, GASAdmin_Place)
#gas_admin.register(gas_models.base.GASConfig, GASAdmin_GAS)
gas_admin.register(gas_models.order.GASSupplierOrder, GASAdmin_GASSupplierOrder)
gas_admin.register(gas_models.order.GASMemberOrder)

#MODEL_LIST = [ 
#    base_models.Place,
#]
## Register models in GAS admin instance
#for m,admin_m in admin.site._registry.items():
#
#    if m in MODEL_LIST:
#        attrs = {
#            'change_list_template' : 'gas_admin/change_list.html'
#        }
#        new_admin_m = type(admin_m.__name__ + "GASAdmin", (admin_m, ), attrs)
#        gas_admin.register(m, new_admin_m)

#gas_admin.register(base_models.Person, admin_models.PersonAdmin)
#
#gas_admin.register(supplier_models.Supplier, admin_models.SupplierAdmin)
#gas_admin.register(supplier_models.Product, admin_models.ProductAdmin)
#gas_admin.register(supplier_models.ProductCategory)
#gas_admin.register(supplier_models.ProductMU)
#gas_admin.register(supplier_models.SupplierStock, admin_models.SupplierStockAdmin)
##gas_admin.register(gas_models.GASConfig, admin_models.GASConfigAdmin)
#gas_admin.register(gas_models.GASMember, admin_models.GASMemberAdmin)
#gas_admin.register(gas_models.order.GASSupplierStock)
#gas_admin.register(gas_models.order.GASSupplierOrderProduct, admin_models.GASSupplierOrderProductAdmin) 
#gas_admin.register(gas_models.order.Delivery, admin_models.DeliveryAdmin)
#gas_admin.register(gas_models.order.Withdrawal, admin_models.WithdrawalAdmin)

