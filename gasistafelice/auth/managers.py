from django.db import models
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from gasistafelice.base.utils import get_ctype_from_model_label

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, VALID_PARAMS_FOR_ROLES,\
SUPPLIER_REFERRER, GAS_REFERRER, GAS_REFERRER_ORDER, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL
from gasistafelice.auth.exceptions import RoleNotAllowed, RoleParameterNotAllowed, RoleParameterWrongSpecsProvided

class RolesManager(models.Manager):
    """ 
    A custom Manager class for the `ParamRole` model.
    
    Useful for retrieving parametric roles based on role name and parameters
    (via the `get_param_roles` method).
    
    For convenience, a specific method for each role type allowed in the application domain 
    is also provided.        
    
    """
    def get_param_roles(self, role_name, **params):
        """
        This method retrieves the parametric roles satisfying the criteria provided as input.
        
        **Arguments**
        
        role_name
            An identifier string matching one of the (non-parametric) roles allowed by 
            the application domain. 
        params
            A dictionary of keyword arguments representing a pattern of parameters with respect to which 
            restricting the query.
            
        **Return Values**
        
        If input values are fine (with respect to the given application domain), `get_param_roles`  returns
        the QuerySet of all ParamRoles whose type is `role_name` and whose parameter set is a superset of `params`.
        
        If `role_name` is not a valid identifier for a role, raises `RoleNotAllowed`.
        
        If `params` contains an invalid parameter name, raises `RoleParameterNotAllowed`.
        
        If provided parameter names are valid, but one of them is assigned to a wrong type,
        (based on domain constraints) raises  `RoleParameterWrongSpecsProvided`.  
          
        """
        # sanity checks
        try: 
            allowed_param_names = VALID_PARAMS_FOR_ROLES[role_name].keys()
        except KeyError:
            raise RoleNotAllowed(role_name)
        for k in params.keys():
            if k not in allowed_param_names: 
                raise RoleParameterNotAllowed(role_name, allowed_param_names, k)
            expected_ctype = get_ctype_from_model_label(VALID_PARAMS_FOR_ROLES[role_name][k])
            actual_ctype = ContentType.objects.get_for_model(params[k])
            if expected_ctype != actual_ctype:
                raise RoleParameterWrongSpecsProvided(role_name, params)                 
        
        # FIXME should be a QuesrySet, not a list
        rv = []
        # filter out parametric roles of the right type
        p_roles = self.get_query_set().filter(role__name__exact=role_name)
        # select only parametric roles whose parameters are compatible with those specified as input
        for pr in p_roles:
            # a flag used to exclude roles with a mis-matching parameter set 
            match = True
            for (k, v) in params.items():
                try:
                    #parameter name match, but value don't 
                    if not pr.param_set.get(name=k).value == v:
                        match = False
                # in case a parameter has a globally valid name, but not in this role's context
                except ObjectDoesNotExist:  
                    raise RoleParameterWrongSpecsProvided(role_name, params)
            # all tests were passed, so this parametric role matches with the query
            if match:
                rv.append(pr)
                
        return rv
         
        

    def supplier_referrers(self, **params):
        return self.get_param_roles(SUPPLIER_REFERRER, **params)
    
    def gas_members(self, **params):
        return self.get_param_roles(GAS_MEMBER, **params)    
    
    def gas_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER, **params)    
    
    def gas_tech_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_TECH, **params)

    def gas_cash_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_CASH, **params)

    def gas_supplier_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_SUPPLIER, **params)
    
    def gas_order_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_ORDER, **params)


    def gas_delivery_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_DELIVERY, **params)

    def gas_withdrawal_referrers(self, **params):
        return self.get_param_roles(GAS_REFERRER_WITHDRAWAL, **params)


