
from django.contrib.admin.sites import AdminSite

from gasistafelice.base import models as base_models
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models

from gasistafelice.gas_admin.models import base as admin_models

class GasAdminSite(AdminSite):

    index_template = "gas_admin/index.html"

gas_admin = GasAdminSite("gas_admin")

# Register models in GAS admin instance

gas_admin.register(base_models.Person)

gas_admin.register(supplier_models.Supplier)
gas_admin.register(supplier_models.Product)
gas_admin.register(supplier_models.ProductCategory)
gas_admin.register(supplier_models.SupplierStock)
gas_admin.register(gas_models.GASMember, admin_models.GASMemberAdmin)
#gas_admin.register(gas_models.GAS, GASAdmin)
gas_admin.register(gas_models.order.GASSupplierStock)
gas_admin.register(gas_models.order.GASSupplierOrder) #, admin_models.GASSupplierOrderAdmin)
gas_admin.register(gas_models.order.GASMemberOrder)


