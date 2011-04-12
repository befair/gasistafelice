from django.utils.translation import ugettext, ugettext_lazy as _

## role-related constants
NOBODY = 'NOBODY'
GAS_MEMBER = 'GAS_MEMBER'
GAS_REFERRER_SUPPLIER = 'GAS_REFERRER_SUPPLIER'
GAS_REFERRER_ORDER = 'GAS_REFERRER_ORDER'
GAS_REFERRER_WITHDRAWAL = 'GAS_REFERRER_WITHDRAWAL'
GAS_REFERRER_DELIVERY = 'GAS_REFERRER_DELIVERY'
GAS_REFERRER_CASH = 'GAS_REFERRER_CASH'
GAS_REFERRER_TECH = 'GAS_REFERRER_TECH'
SUPPLIER_REFERRER = 'SUPPLIER_REFERRER'

ROLES_LIST = [
(NOBODY, _('Nobody')),
(SUPPLIER_REFERRER, _('Supplier referrer')),
(GAS_MEMBER, _('GAS member')),
(GAS_REFERRER_SUPPLIER, _('GAS supplier referrer')),
(GAS_REFERRER_ORDER, _('GAS order referrer')),
(GAS_REFERRER_WITHDRAWAL, _('GAS withdrawal referrer')),
(GAS_REFERRER_DELIVERY, _('GAS delivery referrer')),
(GAS_REFERRER_CASH, _('GAS cash referrer')),
(GAS_REFERRER_TECH, _('GAS technical referrer')),
]

valid_params_for_roles = (
## format
# (Role' codename, allowed model for 1st param, allowed model for 2nd param)
(SUPPLIER_REFERRER, 'supplier.Supplier', ''),
(GAS_MEMBER, 'gas.GAS', ''),
(GAS_REFERRER_CASH, 'gas.GAS', '' ),
(GAS_REFERRER_TECH, 'gas.GAS', ''),
(GAS_REFERRER_SUPPLIER, 'gas.GAS', 'supplier.Supplier'),
(GAS_REFERRER_ORDER, 'gas.GAS',  'gas.GASSupplierOrder'),
(GAS_REFERRER_WITHDRAWAL, 'gas.GAS',  'gas.Withdrawal'),
(GAS_REFERRER_DELIVERY, 'gas.GAS', 'gas.Delivery'),
)


## permission-related constants
VIEW = 'view'
LIST = 'list'
CREATE = 'create'
EDIT = 'edit'
DELETE = 'delete'
ALL = 'all' # catchall

PERMISSIONS_LIST = [
(VIEW, _('View')),
(LIST, _('List')),
(CREATE, _('Create')),
(EDIT, _('Edit')),
(DELETE, _('Delete')),
(ALL, _('All')), # catchall
]
