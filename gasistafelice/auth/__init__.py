from django.utils.translation import ugettext as _, ugettext_lazy 
from django.db.models.signals import post_syncdb

import permissions
from permissions.utils import register_role, register_permission

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
(GAS_REFERRER_ORDER, 'gas.GASSupplierOrder', ''),
(GAS_REFERRER_WITHDRAWAL, 'gas.Withdrawal', ''),
(GAS_REFERRER_DELIVERY, 'gas.Delivery', ''),

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

class PermissionsRegister(object):
    """Support global register to hold Role and Permissions dicts"""

    # a dictionary holding Roles model instances, keyed by name
    roles_dict = {}

    # a dictionary holding Permission model instances, keyed by Permission's codename
    perms_dict = {}

    @property
    def roles(cls):
        return cls.roles_dict.values()

    @property
    def perms(cls):
        return cls.perms_dict.values()

    @property
    def role_names(cls):
        return cls.roles_dict.keys()

    @property
    def perm_names(cls):
        return cls.perms_dict.keys()

    def get_role(cls, code):
        return cls.roles_dict[code]

    def get_perm(cls, code):
        return cls.perms_dict[code]


def init_permissions(sender, **kwargs):

    ## register project-level Roles
    for (name, description) in ROLES_LIST:
        PermissionsRegister.roles_dict[name] = register_role(name)

    ## register project-level Permissions
    for (codename, name) in PERMISSIONS_LIST:    
        PermissionsRegister.perms_dict[codename] = register_permission(name, codename)

    return

post_syncdb.connect(init_permissions, sender=permissions.models)

    
