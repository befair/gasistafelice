from django.db import models
from django.contrib.auth.models import User

from gasistafelice.auth.models import ParamRole

class GASMembersManager(models.Manager):

    def have_role(self, parametric_role):
        referrer_as_users = User.objects.filter(principal_param_role_relation=parametric_role)
        return self.get_query_set().filter(person__user_in=referrer_as_users)

    def have_roles(self, parametric_roles):
        referrer_as_users = User.objects.filter(principal_param_role_relation__in=parametric_roles)
        return self.get_query_set().filter(person__user_in=referrer_as_users)

    def gas_referrers(self, **resource_kw):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'GAS Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_tech_referrers(**resource_kw)
        return self.have_roles(parametric_roles)


    def tech_referrers(self, **resource_kw):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Tech Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_tech_referrers(**resource_kw)
        return self.have_roles(parametric_roles)

    def cash_referrers(self):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Cash Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_cash_referrers()
        return self.have_roles(parametric_roles)

    def supplier_referrers(self):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Supplier Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_supplier_referrers()
        return self.have_roles(parametric_roles)

    def order_referrers(self):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Order Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_supplier_referrers()
        return self.have_roles(parametric_roles)

    def delivery_referrers(self):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Delivery Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_delivery_referrers()
        return self.have_roles(parametric_roles)

    def withdrawal_referrers(self):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Withdrawal Referrer'
        role for the GAS they belong to.    
        """
        parametric_roles = ParamRole.objects.gas_delivery_referrers()
        return self.have_roles(parametric_roles)

