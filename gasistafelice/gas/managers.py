from django.db import models

from gasistafelice.consts import *
from flexi_auth.models import ParamRole
from gasistafelice.gas.query import OrderQuerySet, AppointmentQuerySet

class GASMemberManager(models.Manager):
    """
    A custom manager class for the `GASMember` model.
    """

    def gas_referrers(self, gas=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'GAS Referrer'
        role for the GAS they belong to.
        
        If a `gas` argument is provided, the result set is filtered accordingly.      
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER, gas)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in=pr.get_users(), gas=pr.gas)

        return qs


    def tech_referrers(self, gas=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Tech Referrer'
        role for the GAS they belong to.    
        
        If a `gas` argument is provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_TECH, gas)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas=pr.gas)

        return qs
        

    def cash_referrers(self, gas=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Cash Referrer'
        role for the GAS they belong to.    
        
        If a `gas` argument is provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_CASH, gas)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas=pr.gas)

        return qs

    def supplier_referrers(self, gas=None, supplier=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Supplier Referrer'
        role for the GAS they belong to.    
        
        If a `gas` and/or a 'supplier' arguments are provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_SUPPLIER, gas, supplier)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas=pr.gas)

        return qs


    def order_referrers(self, order=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Order Referrer'
        role for the GAS they belong to.    
        
        If a `order` argument is provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_ORDER, order)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas=pr.order.pact.gas)

        return qs

    def delivery_referrers(self, delivery=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Delivery Referrer'
        role for the GAS they belong to.    
        
        If a `delivery` argument is provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_DELIVERY, delivery)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas__in=pr.delivery.gas_set)

        return qs

    def withdrawal_referrers(self, withdrawal=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Withdrawal Referrer'
        role for the GAS they belong to.
        
        If a `withdrawal` argument is provided, the result set is filtered accordingly.    
        """
        # TODO: UNITTEST needed !
        p_roles = ParamRole.objects.get_param_roles(GAS_REFERRER_WITHDRAWAL, withdrawal)
        # initialize the return QuerySet to an EmptyQuerySet
        qs = self.model.objects.none()
        # costruct the result set by joining partial QuerySets
        # (one for each parametric role of interest)
        for pr in p_roles:
            # filter out spurious GAS members arising when a Person belongs to multiple GAS
            qs = qs | self.model.objects.filter(person__user__in= pr.get_users(), gas__in=pr.withdrawal.gas_set)

        return qs

#-------------------------------------------------------------------------------

class AppointmentManager(models.Manager):
    # TODO UNITTEST
    """Extends default manager with methods useful for appointments.

    * future()
    * past()
    
    """
    
    def get_query_set(self):
        return AppointmentQuerySet(self.model)

    def future(self):
        """
        Return a QuerySet containing all appointments scheduled for today or for a future date.
        """
        return self.get_query_set().future()

    def past(self):
        """
        Return a QuerySet containing all past appointments.
        """
        return self.get_query_set().past()

#-------------------------------------------------------------------------------

class OrderManager(models.Manager):
    # TODO UNITTEST DOC

    def get_query_set(self):
        return OrderQuerySet(self.model)

    def open(self):
        return self.get_query_set().open()

    def closed(self):
        return self.get_query_set().closed()
    
    def on_completion(self):
        return self.get_query_set().on_completion()
    
    def finalized(self):
        return self.get_query_set().finalized()
    
    def sent(self):
        return self.get_query_set().sent()
    
    def delivered(self):
        return self.get_query_set().delivered()
    
    def archived(self):
        return self.get_query_set().archived()
    
    def canceled(self):
        return self.get_query_set().canceled()
  
    

