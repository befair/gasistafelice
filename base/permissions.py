from django.db.models import signals
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import cache

from permissions.utils import register_role, register_permission

from gasistafelice.base.const import ROLES_LIST, PERMISSIONS_LIST
from gasistafelice.base.models import Role, GlobalPermission



## register project-level Roles

# a dictionary holding Roles model instances, keyed by name
roles_dict = {}
for (name, description)  in  ROLES_LIST:
    roles_dict[name] = register_role(name)


## register project-level Permissions

# a dictionary holding Permission model instances, keyed by Permission's codename
perms_dict = {}
for (codename, name)  in  PERMISSIONS_LIST:
    perms_dict[codename] = register_permission(name, codename)


def get_models_with_global_permissions():
    """
    This is a simple helper function that retrieves the list of installed models
    for which global permission management is active. 
    """
    
    # we are only interested in installed model classes for which the `global_grants` attribute exists
    rv = [m for m in cache.get_models() if m._meta.installed and hasattr(m, global_grants)]
    return rv


def get_models_with_local_permissions():
    """
    This is a simple helper function that retrieves the list of installed models
    for which local permission management is active. 
    """

    # we are only interested in installed model classes for which the `local_grants` property is defined
    rv = [m for m in cache.get_models() if m._meta.installed and hasattr(m, local_grants)]
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


def setup_perms(sender, instance, created, **kwargs):
        """
        Setup proper Permissions after a model instance is saved to the DB for the first time,
        based on data contained on the `*_grants` attributes (if any) of the given model class (`sender`).
        
        Global (model-wide) permission grants are specified within the `global_grants` attribute of the given model class;
        it's a tuple of 2-tuples of the form:
        
        (codename of the Permission to be granted, (non-parametric) Roles (as a tuple of strings) to which the Permission is granted for the given model).
        
        Local (per-instance) permission grants are specified within the `local_grants` property of the given model class;
        this property should return a tuple of 2-tuples of the form:
        
        (codename of the Permission to be granted, (query)set of Roles to which that Permission is granted for the given model instance). 
        
        """
        if created: # Permissions have to be set only for newly created instances
            if sender == Role: # a new Role has just been created, so grant to it the right Permissions on existing model instances
                role = instance
                ## setup global permission
                # iterate on all installed models (excluding Role) for which global Permission management is a concern
                model_list = [m for m in get_models_with_global_permissions() if m is not Role]  
                for m in model_list:
                    grants = m.global_grants
                    for (perm_code, roles) in grants:
                        # get a list of actual Role objects 
                        roles = [roles_dict[r] for r in roles]
                        if role in roles:                        
                            # retrieve the Permission object  
                            perm = perms_dict[perm_code]
                            ct = ContentType.objects.get_for_model(m)
                            try:
                                GlobalPermission.objects.create(permission=perm, role=role, content_type=ct)
                            except IntegrityError: # this global permission already exists in the DB
                                pass
                ## setup local permission
                # iterate on all installed models (excluding Role) for which local Permission management is a concern
                model_list = [m for m in get_models_with_local_permissions() if m is not Role]  
                for m in model_list:
                    for obj in m.objects.all():
                        grants = obj.local_grants
                        for (perm_code, roles) in grants:
                                if role in roles:                        
                                    # retrieve the Permission object  
                                    perm = perms_dict[perm_code]
                                    obj.grant_permission(role, perm)                        
            else: # a non-Role model instance has just been created, so grant the right Permissions on it to proper Roles
                if hasattr(sender, 'global_grants'): # model has global permissions data 
                    ## grant global Permissions
                    grants = sender.global_grants
                    for (perm_code, roles) in grants: 
                        # get a list of actual Role objects 
                        roles = [roles_dict[r] for r in roles]                   
                        # retrieve the Permission object  
                        perm = perms_dict[perm_code]
                        # get the Contentype associated with the model class
                        ct = ContentType.objects.get_for_model(sender)
                        for role in roles:
                            try:
                                GlobalPermission.objects.create(permission=perm, role=role, content_type=ct)
                            except IntegrityError: # this global permission already exists in the DB
                                pass
                elif hasattr(instance, 'local_grants'): # model instance has local permissions data
                    ## grant local Permissions
                    # `instance` is the model instance just created
                    grants = instance.local_grants
                    for (perm_code, roles) in grants:                        
                        # retrieve the Permission object  
                        perm = perms_dict[perm_code]
                        for role in roles:
                            instance.grant_permission(role, perm)                                 
                else: # sender model has no permission-related data, so just ignore the signal
                    pass
                                        
# add `setup_perms` function as a listener to the `post_save` signal 
signals.post_save.connect(setup_perms)


