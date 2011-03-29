from permissions.utils import register_permission
from gasistafelice.base.const import PERMISSIONS_LIST

## register project-level Permissions
# a dictionary holding Permission model instances, keyed by Permission's codename
def init_permissions():
    permissions = {}
    for (codename, name)  in  PERMISSIONS_LIST:
        permissions[codename] = register_permission(name, codename)
    return permissions
