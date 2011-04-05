from django.db.models import signals
# from django.contrib.auth.models import Permission as BasePermission
from permissions.utils import register_permission, grant_permission
from gasistafelice.base.const import PERMISSIONS_LIST

## setup proper Roles after a model instance is saved to the DB for the first time;

# this function just calls the `setup_roles` method of the the sender model class (if existing);
# actual role-creation/setup logic is encapsulated there. 
 
def setup_roles(sender, instance, created, **kwargs):
        if created: # Permissions have to be set only for newly created instances
            try:
                # `instance` is the model instance that has just been created
                instance.setup_roles()
                                                    
            except AttributeError:
                # sender model doesn't specify any role-setup operations to do, so just ignore the signal
                pass

# add `setup_roles` function as a listener to the `post_save` signal 
signals.post_save.connect(setup_roles)

## register project-level Permissions

# a dictionary holding Permission model instances, keyed by Permission's codename
perms_dict = {}
for (codename, name)  in  PERMISSIONS_LIST:
    perms_dict[codename] = register_permission(name, codename)

# setup proper Permissions after a model instance is saved to the DB for the first time,
# based on data contained on the `permission_grants` attribute (if any) of the given model class (`sender`)
def setup_perms(sender, instance, created, **kwargs):
        if created: # Permissions have to be set only for newly created instances
            try:
                # sender is the model class the saved instance belongs to
                grants = sender.permission_grants
                # `permission_grants` is a tuple of tuples of the form:
                # (permission codename, Role (query)set, is_local?)
                for (key, roles, is_local) in grants:
                    if is_local: # grant a local (instance-level) Permission
                        # retrieve the Permission object  
                        perm = perms_dict[key]
                        for role in roles:
                            grant_permission(instance, role, perm)
                    else: # grant a global (model-level) Permission
                        # TODO: global permissions' management
                        pass                    
            except AttributeError:
                # sender model has no permission-related data, so just ignore the signal
                pass

# add `setup_perms` function as a listener to the `post_save` signal 
signals.post_save.connect(setup_perms)


