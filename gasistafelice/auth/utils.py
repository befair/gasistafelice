from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User, Group

from permissions.models import Role

from gasistafelice.base.utils import get_ctype_from_model_label 

from gasistafelice.auth import VALID_PARAMS_FOR_ROLES
from gasistafelice.auth.models import Param, ParamRole, PrincipalParamRoleRelation
from gasistafelice.auth.exceptions import RoleParameterNotAllowed, RoleNotAllowed, RoleParameterWrongSpecsProvided

# Roles ######################################################################
# CREDITS: inspired by `django-permissions`

def _validate_parametric_role(name, params, constraints=None):
    """
    Check if the parameters passed on registration of a new (parametric) role
    are allowed in the current application domain.
    
    If the validation succeeds, return True.  
    
    If `name` is not a valid role name, raises  `RoleNotAllowed`.
    
    If the name of a passed parameter is invalid (given the domain-specific constraints), 
    raises `RoleParameterNotAllowed`.
    
    If anything else goes wrong with respect to passed parameters, raises `RoleParameterWrongSpecsProvided`.
    
    **Parameters:**
    name
        a string identifying the kind of parametric role to register;
        must be an identifier of an allowed (non-parametric) Role
    params
        a dictionary containing names and values of the parameters to be associated
        with the parametric Role 
    constraints
        a data structure specifying what combinations of basic roles and parameters
        are valid in the context of the current application domain.
        This data structure must be a dictionary having as keys the string identifiers 
        of allowed (non-parametric) roles; values must be dictionaries where each key-value pair
        consists of the name (as as string) and content type (as a 'model label') of an
        allowed parameter (here, the 'model label' is  a string of the type 'app_name.model_name').  
    
    
        
    """
    
    if constraints: # if no constraints are specified, any parametric role is valid

        # First of all, check if a valid role_name is provided
        role_name = name
        if role_name not in constraints.keys():
            raise RoleNotAllowed(role_name)

        # construct a dictionary holding ContentTypes of passed parameters
        param_specs = {}
        for (k,v) in params.items():
            if k not in constraints[role_name].keys():
                raise RoleParameterNotAllowed(role_name, constraints[role_name].keys(), k)
            param_specs[k] = ContentType.objects.get_for_model(v)

        # construct a dictionary holding expected ContentTypes of expected parameters
        expected_param_specs = {}
        for (k,v) in constraints[role_name].items():
            expected_param_specs[k] = get_ctype_from_model_label(v)

        # compare computed and expected signatures for parameters
        if expected_param_specs != param_specs:

            # this kind of parametric role isn't allowed in the current application domain
            # COMMENT fero: in this way we cannot easily guess which parameter is wrong
            raise RoleParameterWrongSpecsProvided(role_name, param_specs=param_specs)

    return True


def register_parametric_role(name, **kwargs):
    """Registers a parametric role (`ParamRole`) with given parameters.
    
    Role parameters are passed as keyword arguments; this registration function 
    checks that name, type and number of provided parameters is suitable for 
    the application domain, and prevents duplication of parametric roles in the DB.     
    
    Returns the new parametric role if the registration was successfully. 
    
    If `name` is not a valid role name, raises  `RoleNotAllowed`.
    
    If the name of a passed parameter is invalid (given the domain-specific constraints), 
    raises `RoleParameterNotAllowed`.
    
    If anything else goes wrong with respect to passed parameters, raises `RoleParameterWrongSpecsProvided`.
       
    
    **Parameters:**

    name
        a (unique) string identifying the basic Role associated with the ParamRole 
    
    kwargs
         a dictionary of keyword arguments describing the parameters associated with the ParamRole
    
    This function is just a simple extension of the `register_role()` function found in `django-permissions`,
    taking into account the additional parameters needed by the constructor of our custom `ParamRole` model class.
    """
    # TODO: adapt implementation to the new version of `ParamRole`
    params = kwargs

    # raise an exception if params are invalid
    _validate_parametric_role(name, params, constraints=VALID_PARAMS_FOR_ROLES)   

    # check if a `Role` with the passed name already exists in the DB; if not, create it

    role, created = Role.objects.get_or_create(name=name)      
    ## TODO: enclose in a transaction
    # construct the dictionary representation of the parametric role to be registered,
    # as specified by the passed arguments
    p_role_dict = {}
    p_role_dict['role'] = role
    p_role_dict['params'] = params           
            
    # avoid storing duplicated parametric roles in the DB
    # if a parametric role of the same kind and with the same parameters 
    # of the one to be registered already exists in the DB, creation isn't actually needed
    candidates =  ParamRole.objects.filter(role=role)
    for c in candidates:
        if _compare_parametric_roles(p_role_dict, c):
            return c
    # the parametric role doesn't already exist in the DB, so create it
    # create a new blank `ParamRole` instance 
    p_role = ParamRole.objects.create(role=role)
    for (k,v) in params.items():
        ct = ContentType.objects.get_for_model(v)
        obj_pk = v.pk
        p, created = Param.objects.get_or_create(name=k, content_type=ct, object_id=obj_pk)
        p_role.param_set.add(p)
        p.save()
    return p_role           

def _parametric_role_as_dict(p_role):
    """
    Convert a parametric role (a `ParamRole` model instance) 
    to a dictionary representation of it.
    
    If the passed argument is not a `ParamRole` model instance, raise a `TypeError`.
    
    The dictionary representation of a parametric role is of the form:
    
    {'role':role, params:{'name1':value1, 'name2':value2,..}},
    
    where role is the `Role` model instance associated with the `ParamRole`.
    
    This kind of representation can be useful when comparing two parametric roles, 
    since it doesn't depend on details such as instance's database IDs and similar.    
    """    
    if isinstance(p_role, ParamRole):
        dict_repr = {}
        role = p_role.role
        dict_repr['role'] = role
        dict_repr['params'] = {}
        params = p_role.params
        for p in params:
            name = p.name
            value = p.value
            dict_repr['params'][name] = value
        return dict_repr        
    else:
        raise TypeError('Argument must be a ParamRole model instance.')
    
    

def _is_valid_parametric_role_dict_repr(dict_repr):
    """
    Tests if a given dictionary is a valid dictionary representation 
    of a parametric role (`ParamRole`) model instance 
    (as specified by the `_parametric_role_as_dict()` function).
    
    Return True if the passed dictionary has the right format, False otherwise.
    
    Note that this function only checks the general structure of the passed dictionary;
    it doesn't care for the 'semantic' aspects of the parametric role 
    (i.e. names and  values of parameters), since they depend on domain-specific constraints,
    if any.    
    """
    
    if isinstance(dict_repr, dict):        
        if set(dict_repr.keys()) == set(('role', 'params')):
            role = dict_repr['role']
            params = dict_repr['params']
            if isinstance(role, Role) and isinstance(params, dict):
                return True                                
    return False

         

def _compare_parametric_roles(p_role1, p_role2):
    """ 
    Compare two parametric roles for equality;
    retrun True if they are equal, False otherwise.
    
    Two parametric roles are considered equal iff both of the following conditions hold:
    1) they are associated to the same basic role (`ParamRole.role`) 
    2) they have the same set of parameters (`ParamRole.param_set`)
    
    In turn, two parameters are considered equal iff they have the same name (`Param.name`) 
    and value (`Param.value`).
    
    Function arguments can be either `ParamRole` instances or dictionary representations of a parametric
    role (as specified by the `_parametric_role_as_dict()` function).
    
    If an argument is neither a `ParamRole` instance nor a valid dictionary representation of it,
    raise a  `TypeError`.        
    """
    
    p_roles = [p_role1, p_role2]     
    for i in range(0,2):
        if isinstance(p_roles[i], ParamRole):
            # if argument is a ParamRole instance, convert it to a dictionary representation;
            # useful for comparison purposes
            p_roles[i] = _parametric_role_as_dict(p_roles[i])
        elif _is_valid_parametric_role_dict_repr(p_roles[i]):
            pass
        else:
            raise TypeError("%s is neither a ParamRole instance nor a valid dictionary representation of a parametric role." % p_roles[i])
        
    return p_roles[0] == p_roles[1]
         

def add_parametric_role(principal, role):
    """
    Adds a parametric role to a principal.  
    
    Return True if a new parametric role was added to the principal, 
    False if the given parametric role was already assigned to the principal;
    raise `AttributeError` if the principal is neither a `User` nor a `Group` instance.  

    **Parameters:**

    principal
        The principal (`User` or `Group`) which gets the parametric role added.

    role
        The (parametric) role which is assigned.
    """
    if isinstance(principal, User):
        try:
            PrincipalParamRoleRelation.objects.get(user=principal, role=role)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(user=principal, role=role)
            return True
    elif isinstance(principal, Group):
        try:
            PrincipalParamRoleRelation.objects.get(group=principal, role=role)
        except PrincipalParamRoleRelation.DoesNotExist:
            PrincipalParamRoleRelation.objects.create(group=principal, role=role)
            return True
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")

    return False

def remove_parametric_role(principal, role):
    """
    Remove a parametric role from a principal.
      
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a `User` nor a `Group` instance.  

    **Parameters:**

    principal
        The principal (`User` or `Group`) which gets the parametric role removed.

    role
        The (parametric) role which is removed from the principal.
    """
        
    try:
        if isinstance(principal, User):
            ppr = PrincipalParamRoleRelation.objects.get(user=principal, role=role)
        elif isinstance(principal, Group):
            ppr = PrincipalParamRoleRelation.objects.get(group=principal, role=role)
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")

    except PrincipalParamRoleRelation.DoesNotExist:
        return False
    else:
        ppr.delete()

    return True

def remove_parametric_roles(principal):
    """
    Removes all parametric roles assigned to a principal ('User` or `Group`).
    
    Return True if the removal was successful, False otherwise; 
    raise `AttributeError` if the principal is neither a `User` nor a `Group` instance.
      
    **Parameters:**

    principal
        The principal (a `User` or `Group` instance) from which all parametric roles are removed.
    """
    if isinstance(principal, User):
        pprs = PrincipalParamRoleRelation.objects.filter(user=principal)
    elif isinstance(principal, Group):
        pprs = PrincipalParamRoleRelation.objects.filter(group=principal)
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")   
    if len(pprs) == 0:
        return False
    else:
        pprs.delete.all()
        return True
        

def get_parametric_roles(principal):
    """
    Returns parametric roles assigned to a principal (`User` or `Group`).
        
    Raise `AttributeError` if the principal is neither a `User` nor a `Group` instance.
    """
    if isinstance(principal, User):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            user=principal)]
    elif isinstance(principal, Group):
        return [prr.role for prr in PrincipalParamRoleRelation.objects.filter(
            group=principal)]
    else:
        raise AttributeError("The principal must be either a User instance or a Group instance.")
    
    
def get_all_parametric_roles(principal):
    """
    Returns all parametric roles of a given principal (`User` or `Group`). 
    
    This takes into account roles assigned directly to the principal and, 
    if the principal is a `User`, also roles obtained via a `Group` the user belongs to. 

    """
    roles = get_parametric_roles(principal)

    if isinstance(principal, User):
        for group in principal.groups.all():
            roles.extend(get_parametric_roles(group))
    return roles
