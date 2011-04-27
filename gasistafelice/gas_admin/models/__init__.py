
from django.contrib.admin.sites import AdminSite

from gasistafelice.base import models as base_models
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models

from gasistafelice.gas_admin.models import base as admin_models

from gasistafelice.bank import models as bank_models

class GasAdminSite(AdminSite):

    index_template = "gas_admin/index.html"

gas_admin = GasAdminSite("gas_admin")

# Register models in GAS admin instance

gas_admin.register(base_models.Person, admin_models.PersonAdmin)
#gas_admin.register(base_models.Place, admin_models.PlaceAdmin)
gas_admin.register(base_models.Place)

gas_admin.register(supplier_models.Supplier, admin_models.SupplierAdmin)
gas_admin.register(supplier_models.Product, admin_models.ProductAdmin)
gas_admin.register(supplier_models.ProductCategory)
gas_admin.register(supplier_models.ProductMU)
gas_admin.register(supplier_models.SupplierStock, admin_models.SupplierStockAdmin)
gas_admin.register(gas_models.GAS, admin_models.GASAdmin)
gas_admin.register(gas_models.GASMember, admin_models.GASMemberAdmin)
gas_admin.register(gas_models.order.GASSupplierStock)
gas_admin.register(gas_models.order.GASSupplierOrder, admin_models.GASSupplierOrderAdmin)
gas_admin.register(gas_models.order.GASSupplierOrderProduct, admin_models.GASSupplierOrderProductAdmin) 
gas_admin.register(gas_models.order.GASMemberOrder)
gas_admin.register(gas_models.order.Delivery, admin_models.DeliveryAdmin)
gas_admin.register(gas_models.order.Withdrawal, admin_models.WithdrawalAdmin)
gas_admin.register(bank_models.Account)

