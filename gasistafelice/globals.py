from gasistafelice.gas.models.proxy import *

type_model_d = {
	'site' : DES,
	'gas' : GAS,
	'gasmember' : GASMember,
	'person' : Person,
	'supplier' : Supplier,
	'product' : Product,
	'category' : ProductCategory,
	'order' : GASSupplierOrder,
	'pact' : GASSupplierSolidalPact,
	'delivery' : Delivery,
	'withdrawal' : Withdrawal,
	'account' : Account,
}

RESOURCE_LIST = type_model_d.keys()

#TODO fero TOCHECK
#from reports.models import PeriodicReport
#from users.models import UserContainer
#type_model_d.update( { 'periodicreport': PeriodicReport } )
#type_model_d.update( { 'usercontainer' : UserContainer } )


