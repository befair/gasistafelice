from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product
from gasistafelice.gas.models import GAS, GASMember, GASSupplierOrder, GASSupplierSolidalPact, Delivery, Withdrawal
from gasistafelice.des.models import DES

type_model_d = {
	'site' : DES,
	'gas' : GAS,
	'gasmember' : GASMember,
	'person' : Person,
	'supplier' : Supplier,
	'product' : Product,
	'order' : GASSupplierOrder,
	'pact' : GASSupplierSolidalPact,
    'delivery' : Delivery,
    'withdrawal' : Withdrawal,
	
}

RESOURCE_LIST = type_model_d.keys()

#TODO fero TOCHECK
#from reports.models import PeriodicReport
#from users.models import UserContainer
#type_model_d.update( { 'periodicreport': PeriodicReport } )
#type_model_d.update( { 'usercontainer' : UserContainer } )


