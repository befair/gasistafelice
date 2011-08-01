from django.utils.translation import ugettext as _, ugettext_lazy 

## role-related constants
NOBODY = 'NOBODY'
GAS_MEMBER = 'GAS_MEMBER'
GAS_REFERRER = 'GAS_REFERRER'
GAS_REFERRER_SUPPLIER = 'GAS_REFERRER_SUPPLIER'
GAS_REFERRER_ORDER = 'GAS_REFERRER_ORDER'
GAS_REFERRER_WITHDRAWAL = 'GAS_REFERRER_WITHDRAWAL'
GAS_REFERRER_DELIVERY = 'GAS_REFERRER_DELIVERY'
GAS_REFERRER_CASH = 'GAS_REFERRER_CASH'
GAS_REFERRER_TECH = 'GAS_REFERRER_TECH'
SUPPLIER_REFERRER = 'SUPPLIER_REFERRER'
DES_ADMIN = 'DES_ADMIN'

ROLES_LIST = [
    (NOBODY, _('Nobody')),
    (SUPPLIER_REFERRER, _('Supplier referrer')),
    (GAS_MEMBER, _('GAS member')),
    (GAS_REFERRER, _('GAS referrer')),
    (GAS_REFERRER_SUPPLIER, _('GAS supplier referrer')),
    (GAS_REFERRER_ORDER, _('GAS order referrer')),
    (GAS_REFERRER_WITHDRAWAL, _('GAS withdrawal referrer')),
    (GAS_REFERRER_DELIVERY, _('GAS delivery referrer')),
    (GAS_REFERRER_CASH, _('GAS cash referrer')),
    (GAS_REFERRER_TECH, _('GAS technical referrer')),
    (DES_ADMIN, _('DES administrator')),
]

VALID_PARAMS_FOR_ROLES = {
    ## format
    # {Role' codename: {parameter name: parameter type, ..}}
    # where the parameter type is expressed as a string of the format 'app_label.model_name'
    SUPPLIER_REFERRER : {'supplier':'supplier.Supplier'},
    GAS_MEMBER : {'gas':'gas.GAS'},
    GAS_REFERRER : {'gas':'gas.GAS'},
    GAS_REFERRER_CASH : {'gas':'gas.GAS'},
    GAS_REFERRER_TECH : {'gas':'gas.GAS'},
    GAS_REFERRER_SUPPLIER : {'gas':'gas.GAS', 'supplier':'supplier.Supplier'},
    GAS_REFERRER_ORDER : {'order':'gas.GASSupplierOrder'},
    GAS_REFERRER_WITHDRAWAL: {'withdrawal':'gas.Withdrawal'},
    GAS_REFERRER_DELIVERY: {'delivery':'gas.Delivery'},
    DES_ADMIN: {'des':'des.DES'},                         
}



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





    
