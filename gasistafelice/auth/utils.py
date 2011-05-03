from django.db import IntegrityError
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import cache

from django.contrib.auth.models import User, Group

from permissions.models import Role

from gasistafelice.base.utils import get_ctype_from_model_label 

from gasistafelice.auth import PermissionsRegister, valid_params_for_roles
from gasistafelice.auth.models import Param, ParamRole, PrincipalParamRoleRelation, GlobalPermission

# Roles ######################################################################
# CREDITS: inspired by `django-permissions`

def validate_parametric_role(name, params, constraints=None):
    """
    Check if the parameters passed on registration of a new (parametric) role
    are allowed in current the application domain.  
    
    **Parameters:**
    name
        a string identifying the kind of parametric role to register;
        must be an identifier of an existing (non-parametric) Role
    params
        a dictionary containing names and values of the parameters to be associated
        with the parametric Role 
    constraints
        a data structure specifiyng what combinations of basic roles and parameters
        are valid in the context of the current application domain. 
    """
    # construct a dictionary holding ContentTypes of passed parameters
    param_specs = {}
    for (k,v) in params.items():
        param_specs[k] = ContentType.objects.get_for_model(v)
    # construct a dictionary holding expected ContentTypes of expected parameters
    role_name = name
    expected_param_specs = {}
    for (k,v) in constraints[role_name].items():
        expected_param_specs[k] = get_ctype_from_model_label(v)
    # compare computed and expected signatures for parameters
    if expected_param_specs == param_specs:
        return True
    else:
        return False


def register_parametric_role(name, **kwargs):
    """Registers a parametric role (`ParamRole`) with given parameters.
    
    Role parameters are passed as keyword arguments; this registration function 
    checks that name, type and number of provided parameters is suitable for 
    the application domain, and prevents duplication of parametric roles in the DB.     
    
    Returns the new parametric role if the registration was successfully, otherwise False.    
    
    **Parameters:**

    name
        a (unique) string identifying the basic Role associated with the ParamRole 
    
    **kwargs
         a dictionary of keyword arguments describing the parameters associated with the ParamRole
    
    This function is just a simple extension of the `register_role()` function found in `django-permissions`,
    taking into account the additional parameters needed by the constructor of our custom `ParamRole` model class.
    """
    # TODO: adapt implementation to the new version of ParamRole
    params = kwargs
    if validate_parametric_role(name, params, constraints=valid_params_for_roles):   
        # check if a Role with the passed name already exists in the DB; if not, create it
        role = Role.objects.get_or_create(name=name)
        #if not isinstance(role, Role):
        #if not isinstance(name, role):
        #    raise AttributeError("The role must be a Role instance.")   
        ## TODO: enclose in a transaction 
        # create a new blank ParamRole 
        #p_role = ParamRole.objects.create(null, role=role)
        #p_role = ParamRole.objects.create(role)
        #p_role = ParamRole.objects.create(role=role)
        p_role = ParamRole(role=role)
        for (k,v) in params:
            p = Param.objects.get_or_create(name=k, param=v)
            p_role.param_set.add(p)
            # avoid storing duplicated parametric roles in the DB
            # if a parametric role with the same parameters of the one just constructed
            # already exists in the DB, registration isn't actually needed
            existing_p_roles = ParamRole.objects.all()
            if p_role in existing_p_roles:
                return True 
            else:
                # this parametric role doesn't exists yet, so save it to the DB 
                p.save()
                return p_role
    else: # this kind of parametric role isn't allowed in the current application domain
        return False
    

def add_parametric_role(principal, role):
    """Adds a global parametric role to a principal.  
    
    Return True if a new parametric role was added to the principal, 
    False the given parametric role was already assigned to the principal;
    raise `AttributeError` if the principal is neither a User nor a Group instance.  

    **Parameters:**

    principal
        The principal (User or Group) which gets the parametric role added.

    role
        The (parametric) role which is assigned.
    """
    if isinstance(principal, User):
        try:
            PrincipalParamRoleRelation.objects.get(user=principal, role=role, content_id=None, content_type=None)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(user=principal, role=role)
            return True
    elif isinstance(principal, Group):
        try:
            PrincipalParamRoleRelation.objects.get(group=principal, role=role, content_id=None, content_type=None)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(group=principal, role=role)
            return True
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")

    return False

def add_local_parametric_role(obj, principal, role):
    """Adds a local parametric role to a principal for a given content object.
      
    Return True if a new parametric role was added to the principal, 
    False the given parametric role was already assigned to the principal;
    raise `AttributeError` if the principal is neither a User nor a Group instance.  

    **Parameters:**

    principal
        The principal (User or Group) which gets the parametric role added.

    role
        The (parametric) role which is assigned.
        
    obj
        The content object for which the local role is assigned.
    """
        
    ctype = ContentType.objects.get_for_model(obj)
    if isinstance(principal, User):
        try:
            PrincipalParamRoleRelation.objects.get(user=principal, role=role, content_id=obj.id, content_type=ctype)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(user=principal, role=role, content=obj)
            return True
    elif isinstance(principal, Group):
        try:
            PrincipalParamRoleRelation.objects.get(group=principal, role=role, content_id=obj.id, content_type=ctype)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(group=principal, role=role, content=obj)
            return True
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")

    return False

def remove_parametric_role(principal, role):
    """Remove a parametric role from a principal.
      
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a User nor a Group instance.  

    **Parameters:**

    principal
        The principal (User or Group) which gets the parametric role removed.

    role
        The (parametric) role which is removed from the principal.
    """
        
    try:
        if isinstance(principal, User):
            ppr = PrincipalParamRoleRelation.objects.get(
                    user=principal, role=role, content_id=None, content_type=None)
        elif isinstance(principal, Group):
            ppr = PrincipalParamRoleRelation.objects.get(
                    group=principal, role=role, content_id=None, content_type=None)
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")

    except PrincipalParamRoleRelation.DoesNotExist:
        return False
    else:
        ppr.delete()

    return True

def remove_local_parametric_role(obj, principal, role):
    """Remove a local parametric role from a principal with respect to a content object.
      
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a User nor a Group instance.  

    **Parameters:**

    principal
        The principal (User or Group) which gets the parametric role removed.

    role
        The (parametric) role which is removed from the principal.
    obj
        The content object for which the local role is removed.
    """

    try:
        ctype = ContentType.objects.get_for_model(obj)

        if isinstance(principal, User):
            ppr = PrincipalParamRoleRelation.objects.get(
                user=principal, role=role, content_id=obj.id, content_type=ctype)
        elif isinstance(principal, Group):
            ppr = PrincipalParamRoleRelation.objects.get(
                group=principal, role=role, content_id=obj.id, content_type=ctype)
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")
    except PrincipalParamRoleRelation.DoesNotExist:
        return False
    else:
        ppr.delete()

    return True

def remove_parametric_roles(principal):
    """Removes all parametric roles assigned to a principal (User or Group).
    
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a User nor a Group instance.
      
    **Parameters:**

    principal
        The principal (a User or group instance) from which all parametric roles are removed.
    """
    if isinstance(principal, User):
        ppr = PrincipalParamRoleRelation.objects.filter(
            user=principal, content_id=None, content_type=None)
    elif isinstance(principal, Group):
        ppr = PrincipalParamRoleRelation.objects.filter(
            group=principal, content_id=None, content_type=None)
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")   
    if ppr:
        ppr.delete()
        return True
    else:
        return False

def remove_local_parametric_roles(obj, principal):
    """Removes all local parametric roles from a principal (User or Group) with respect to a content object.
   
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a User nor a Group instance.
   
    **Parameters:**

    obj
        content object with respect to the local parametric roles are removed from the principal     
    principal
        The principal (user or group) from which the roles are removed.
    """
    ctype = ContentType.objects.get_for_model(obj)

    if isinstance(principal, User):
        ppr = PrincipalParamRoleRelation.objects.filter(
            user=principal, content_id=obj.id, content_type=ctype)
    elif isinstance(principal, Group):
        ppr = PrincipalParamRoleRelation.objects.filter(
            group=principal, content_id=obj.id, content_type=ctype)
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")      
    if ppr:
        ppr.delete()
        return True
    else:
        return False

def get_parametric_roles(principal, obj=None):
    """Returns all parametric roles of a given principal  (User or Group). 
    
    This takes into account roles assigned directly to the principal and, 
    if the principal is a User, also roles obtained via a group the user belongs to. 
    
    If an object is passed also local parametric roles will be added to the result.

    **Parameters:**

    principal
        The principal (User or Group) for which the roles are retrieved.
    obj [optional]
        A content object with respect to retreiving local parametric roles. 

    
    """
    roles = get_global_parametric_roles(principal)

    if obj is not None:
        roles.extend(get_local_parametric_roles(obj, principal))

    if isinstance(principal, User):
        for group in principal.groups.all():
            if obj is not None:
                roles.extend(get_local_parametric_roles(obj, group))
            roles.extend(get_parametric_roles(group))

    return roles

def get_global_parametric_roles(principal):
    """Returns global parametric roles assigned to a principal (User or Group).
        
       Raise `AttributeError` if the principal is neither a User nor a Group instance.
    """
    if isinstance(principal, User):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            user=principal, content_id=None, content_type=None)]
    elif isinstance(principal, Group):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            group=principal, content_id=None, content_type=None)]
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")      

def get_local_parametric_roles(obj, principal):
    """Returns local parametric roles assigned to a principal (User or Group),
     with respect to a given content object.
     
     Raise `AttributeError` if the principal is neither a User nor a Group instance.
    """
    ctype = ContentType.objects.get_for_model(obj)

    if isinstance(principal, User):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            user=principal, content_id=obj.id, content_type=ctype)]
    elif isinstance(principal, Group):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            group=principal, content_id=obj.id, content_type=ctype)]
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")   


# Permissions ################################################################
def register_global_permission(perm, role, ctype):
    """
    This trivial helper function just creates a new GlobalPermission object,
    taking care of avoiding duplicated entries in the DB.
    """
    
    try:
        GlobalPermission.objects.create(permission=perm, role=role, content_type=ctype)
    except IntegrityError: # this global permission already exists in the DB
        pass
 
# Role and Permission setup utilities ################################################################
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
