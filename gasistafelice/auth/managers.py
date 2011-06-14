from django.db import models

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, VALID_PARAMS_FOR_ROLES,\
SUPPLIER_REFERRER, GAS_REFERRER, GAS_REFERRER_ORDER, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL
from gasistafelice.auth.exceptions import RoleParameterNotAllowed

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
        allowed_param_names = VALID_PARAMS_FOR_ROLES[role_name].keys()
        for k in params.keys():
            if k not in allowed_param_names: 
                raise RoleParameterNotAllowed(role_name, allowed_param_names, k)

        return self.get_query_set().filter(role__name__exact=role_name, **params)

    def supplier_referrers(self, **resource_kw):
        return self.get_param_roles(SUPPLIER_REFERRER, **resource_kw)
    
    def gas_members(self, **resource_kw):
        return self.get_param_roles(GAS_MEMBER, **resource_kw)    
    
    def gas_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER, **resource_kw)    
    
    def gas_tech_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_TECH, **resource_kw)

    def gas_cash_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_CASH, **resource_kw)

    def gas_supplier_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_SUPPLIER, **resource_kw)
    
    def gas_order_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_ORDER, **resource_kw)


    def gas_delivery_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_DELIVERY, **resource_kw)

    def gas_withdrawal_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_WITHDRAWAL, **resource_kw)


