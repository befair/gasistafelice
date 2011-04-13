from django.db import IntegrityError
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import cache

from permissions.models import Role

from gasistafelice.base.utils import get_ctype_from_model_label 

from gasistafelice.auth import PermissionsRegister, valid_params_for_roles
from gasistafelice.auth.models import ParamRole, GlobalPermission



def validate_parametric_role(name, param1, param2, constraints=None):
    """
    Check if the parameters passed on creation of a new (parametric) role
    are allowed in the application domain.  
    """
    for (role_name, model_name_1, model_name_2) in constraints:
        ct_1 = get_ctype_from_model_label(model_name_1)
        ct_2 = get_ctype_from_model_label(model_name_2)
        param1_ct = ContentType.objects.get_for_model(param1)
        param2_ct = ContentType.objects.get_for_model(param2)
        if name == role_name and ct_1 == param1_ct and ct_2 == param2_ct:
            # parameters are of the right type for the role
            return True
    return False


def register_parametric_role(name, param1, param2=None):
    """Registers a parametric role (`ParamRole`) with passed parameters.
    Check if parameters' type is suitable for the application domain, and
    prevent registering duplicated roles in the DB.     
    Returns the new parametric role if the registration was successfully, otherwise False.    
    
    **Parameters:**

    name
        a (unique) string identifying the basic Role associated with the ParamRole 
    param1
        the primary (mandatory) parameter describing the parametric role 
    param2
        a secondary (optional) parameter describing the parametric role
    
    It's just a trivial extension of the `register_role` function found in `django-permissions`,
    taking into account the additional parameters for the constructor of our custom `ParamRole` model class.
    """
    if validate_parametric_role(name, param1, param2, constraints=valid_params_for_roles):   
        # check if a Role with the passed name already exists in the DB; if not, create it
        role = Role.objects.get_or_create(name=name) 
        # create the new Role, if not already existing in the DB 
        param_role = ParamRole.objects.get_or_create(role=role, param1=param1, param2=param2)                        
        return param_role
    else:
        return False

def get_models_with_global_permissions():
    """
    This is a simple helper function that retrieves the list of installed models
    for which global permission management is active.
    """
    
    # we are only interested in installed model classes for which the `global_grants` attribute exists
    rv = [m for m in cache.get_models() if m._meta.installed and hasattr(m, 'global_grants')]
    return rv


def get_models_with_local_permissions():
    """
    This is a simple helper function that retrieves the list of installed models
    for which local permission management is active.
    """

    # we are only interested in installed model classes for which the `local_grants` property is defined
    rv = [m for m in cache.get_models() if m._meta.installed and hasattr(m, 'local_grants')]
    return rv

def register_global_permission(perm, role, ctype):
    """
    This trivial helper function just creates a new GlobalPermission object,
    taking care of avoiding duplicated entries in the DB.
    """
    
    try:
        GlobalPermission.objects.create(permission=perm, role=role, content_type=ctype)
    except IntegrityError: # this global permission already exists in the DB
        pass
   
 
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
                        if role in PermissionsRegister.roles:
                            # retrieve the Permission object
                            perm = PermissionsRegister.get_perm(perm_code)
                            ct = ContentType.objects.get_for_model(m)
                            register_global_permission(perm, role, ct)
                ## setup local permission
                # iterate on all installed models (excluding Role) for which local Permission management is a concern
                model_list = [m for m in get_models_with_local_permissions() if m is not Role]
                for m in model_list:
                    for obj in m.objects.all():
                        grants = obj.local_grants
                        for (perm_code, roles) in grants:
                                if role in roles:
                                    # retrieve the Permission object
                                    perm = PermissionsRegister.get_perm(perm_code)
                                    obj.grant_permission(role, perm)
            else: # a non-Role model instance has just been created, so grant the right Permissions on it to proper Roles
                if hasattr(sender, 'global_grants'): # model has global permissions data
                    ## grant global Permissions
                    grants = sender.global_grants
                    for (perm_code, roles) in grants:
                        # get a list of actual Role objects
                        roles = PermissionsRegister.roles
                        # retrieve the Permission object
                        perm = PermissionsRegister.get_perm(perm_code)
                        # get the Contentype associated with the model class
                        ct = ContentType.objects.get_for_model(sender)
                        for role in roles:
                            register_global_permission(perm, role, ct)
                elif hasattr(instance, 'local_grants'): # model instance has local permissions data
                    ## grant local Permissions
                    # `instance` is the model instance just created
                    grants = instance.local_grants
                    for (perm_code, roles) in grants:
                        # retrieve the Permission object
                        perm = PermissionsRegister.get_perm(perm_code)
                        for role in roles:
                            instance.grant_permission(role, perm)
                else: # sender model has no permission-related data, so just ignore the signal
                    pass
                                        
# add `setup_perms` function as a listener to the `post_save` signal
signals.post_save.connect(setup_perms)
