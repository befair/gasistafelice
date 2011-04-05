from django.db.models import signals
# from django.contrib.auth.models import Permission as BasePermission
from permissions.utils import register_permission
from gasistafelice.base.const import PERMISSIONS_LIST
from gasistafelice.base.models import Role

def get_models_with_permissions():
    """
    This is a simple helper function that retrieves the list of installed models
    for which permission management is active. 
    """
    from django.db.models.loading import cache
    # we are only interested in installed model classes for which the `permission_grants` property is defined
    rv = [m for m in cache.get_models() if m._meta.installed and hasattr(m, permission_grants)]
    return rv

 
def setup_roles(sender, instance, created, **kwargs):
    """
    Setup proper Roles after a model instance is saved to the DB for the first time.
    
    This function just calls the `setup_roles` method of the the sender model class (if existing);
    actual role-creation/setup logic is encapsulated there.
    """
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

def setup_perms(sender, instance, created, **kwargs):
        """
        Setup proper Permissions after a model instance is saved to the DB for the first time,
        based on data contained on the `permission_grants` attribute (if any) of the given model class (`sender`).
        """
        # TODO: global permissions' management
        if created: # Permissions have to be set only for newly created instances
            if sender == Role: # a new Role has just been created, so grant to it the right Permissions on existing model instances
                role = instance
                # iterate on all installed models (excluding Role) for which Permission management is a concern
                model_list = [m for m in get_models_with_permissions() if m is not Role]  
                for m in model_list:
                    for obj in m.objects.all():
                        grants = obj.permission_grants
                        for (perm_code, roles) in grants:
                                if role in roles:                        
                                    # retrieve the Permission object  
                                    perm = perms_dict[perm_code]
                                    instance.grant_permission(role, perm)                        
            else: # a not-Role model instance has just been created, so grant the right Permissions on it to proper Roles
                try:
                    # `instance` is the model instance just created
                    grants = instance.permission_grants
                    # `permission_grants` is a tuple of 2-tuples of the form:
                    # (codename of the permission to be granted, (query)set of Roles to which that Permission is granted for the give model instance)                    
                    for (perm_code, roles) in grants:                        
                            # retrieve the Permission object  
                            perm = perms_dict[perm_code]
                            for role in roles:
                                instance.grant_permission(role, perm)                   
                except AttributeError:
                    # sender model has no permission-related data, so just ignore the signal
                    pass

# add `setup_perms` function as a listener to the `post_save` signal 
signals.post_save.connect(setup_perms)


