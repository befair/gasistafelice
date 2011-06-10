from django.db import models

from gasistafelice.auth import GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, GAS_REFERRER_CASH, GAS_MEMBER, VALID_PARAMS_FOR_ROLES
from gasistafelice.auth.exceptions import RoleParameterNotAllowed

class RolesManager(models.Manager):

    def get_param_roles(self, role_name, **resource_kw):
        relatable_resources = VALID_PARAMS_FOR_ROLES[role_name].keys()
        for k in resource_kw.keys():
            if k not in relatable_resources: 
                raise RoleParameterNotAllowed(role_name, relatable_resources, k)

        return self.get_query_set().filter(role__name__exact=role_name, **resource_kw)
        
    def gas_tech_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_TECH, **resource_kw)

    def gas_cash_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_CASH, **resource_kw)

    def gas_supplier_referrers(self, **resource_kw):
        return self.get_param_roles(GAS_REFERRER_SUPPLIER, **resource_kw)

    def supplier_referrers(self, **resource_kw):
        return self.get_param_roles(SUPPLIER_REFERRER, **resource_kw)

    #TODO placeholder for other roles: seldon
