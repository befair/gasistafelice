from django.db import models
from django.contrib.auth.models import User

from gasistafelice.auth.models import ParamRole
from gasistafelice.gas.models.base import GASMember

class GASMembersManager(models.Manager):

    def gas_referrers(self, gas=None):
        """
        Return a list containing all GAS members who have been assigned the 'GAS Referrer'
        role for the GAS they belong to.
        
        If a `gas` argument is provided, the result set is filtered accordingly.      
        """
        p_roles = ParamRole.objects.gas_referrers(gas)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas == pr.gas]
        # FIXME: should be a QuesySet ?
        return members


    def tech_referrers(self, gas=None):
        """
        Return a list containing all GAS members who have been assigned the 'Tech Referrer'
        role for the GAS they belong to.    
        
        If a `gas` argument is provided, the result set is filtered accordingly.
        """
        
        p_roles = ParamRole.objects.gas_tech_referrers(gas)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas == pr.gas]
        # FIXME: should be a QuesySet ?
        return members
      

    def cash_referrers(self, gas=None):
        """
        Return a list containing all GAS members who have been assigned the 'Cash Referrer'
        role for the GAS they belong to.    
        
        If a `gas` argument is provided, the result set is filtered accordingly.
        """
        
        p_roles = ParamRole.objects.gas_cash_referrers(gas)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas == pr.gas]
        # FIXME: should be a QuesySet ?
        return members

    def supplier_referrers(self, gas=None, supplier=None):
        """
        Return a list containing all GAS members who have been assigned the 'Supplier Referrer'
        role for the GAS they belong to.    
        
        If a `gas` and/or a 'supplier' arguments are provided, the result set is filtered accordingly.
        """
        
        p_roles = ParamRole.objects.gas_supplier_referrers(gas, supplier)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas == pr.gas]
        # FIXME: should be a QuesySet ?
        return members


    def order_referrers(self, order=None):
        """
        Return a list containing all GAS members who have been assigned the 'Order Referrer'
        role for the GAS they belong to.    
        
        If a `order` argument is provided, the result set is filtered accordingly.
        """
        
        p_roles = ParamRole.objects.gas_order_referrers(order)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas == pr.order.pact.gas]
        # FIXME: should be a QuesySet ?
        return members

    def delivery_referrers(self, delivery=None):
        """
        Return a list containing all GAS members who have been assigned the 'Delivery Referrer'
        role for the GAS they belong to.    
        
        If a `delivery` argument is provided, the result set is filtered accordingly.
        """
        
        p_roles = ParamRole.objects.gas_order_referrers(delivery)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas in pr.delivery.gas_set()]
        # FIXME: should be a QuesySet ?
        return members

    def withdrawal_referrers(self, withdrawal=None):
        """
        Return a list containing all GAS members who have been assigned the 'Withdrawal Referrer'
        role for the GAS they belong to.
        
        If a `withdrawal` argument is provided, the result set is filtered accordingly.    
        """
        
        p_roles = ParamRole.objects.gas_order_referrers(withdrawal)
        members = []
        for pr in p_roles:
            for user in pr.get_users():
                # filter out spurious GAS members
                # arising when a Person belongs to multiple GAS
                members += [m for m in GASMember.objects.filter(person__user=user) if m.gas in pr.withdrawal.gas_set()]
        # FIXME: should be a QuesySet ?
        return members

