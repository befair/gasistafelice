from gasistafelice.des.models import DES
from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product, ProductCategory, ProductMU, SupplierStock
from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.models.order import GASSupplierOrder

type_model_d = {
	'site' : DES,
	'gas' : GAS,
	'gasmember' : GASMember,
	'person' : Person,
	'supplier' : Supplier,
	'product' : Product,
	'order' : GASSupplierOrder,
	'stock' : SupplierStock,
	'gasstock' : GASSupplierStock,
	'category' : ProductCategory,
	'unit' : ProductMU,
	'pact' : GASSupplierSolidalPact,
}

RESOURCE_LIST = type_model_d.keys()

#TODO fero TOCHECK
#from reports.models import PeriodicReport
#from users.models import UserContainer
#type_model_d.update( { 'periodicreport': PeriodicReport } )
#type_model_d.update( { 'usercontainer' : UserContainer } )


