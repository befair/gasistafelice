from gasistafelice.gas.models.proxy import *

type_model_d = {
	'site' : DES,
	'gas' : GAS,
	'gasmember' : GASMember,
	'person' : Person,
	'supplier' : Supplier,
	'product' : Product,
	'product2' : SupplierStock,
	'product3' : GASSupplierStock,
	'product4' : GASSupplierOrderProduct,
	'category' : ProductCategory,
	'unit' : ProductMU,
	'order' : GASSupplierOrder,
	'pact' : GASSupplierSolidalPact,
	'delivery' : Delivery,
	'withdrawal' : Withdrawal,
	'account' : Account,
	'transact' : Movement,
	'referrer' : SupplierReferrer,
	'bio' : Certification,
	'order' : GASSupplierOrder,
	'basket' : GASMemberOrder,
}

#FIXME: find better name for catalogs of products: product, product2 , product3 and product4
#TODO domthu TOCHECK
# catalogs filtered by available & unavailable for view (blocks) product availability. how to? wich catalogs? 
#FIXME: list of orders filtered by worflow state: How to? Filter in views or each workflow_state = one resource?
#FIXME: Account: when viewing GAS we would like to show 3 blocks of Accounts (GAS, GASMember, Supplier). How can be done (filter in views/block or independant resources)?

RESOURCE_LIST = type_model_d.keys()

#TODO fero TOCHECK
#from reports.models import PeriodicReport
#from users.models import UserContainer
#type_model_d.update( { 'periodicreport': PeriodicReport } )
#type_model_d.update( { 'usercontainer' : UserContainer } )


