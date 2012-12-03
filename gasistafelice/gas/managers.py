from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Max

from gasistafelice.consts import *
from flexi_auth.models import ParamRole
from gasistafelice.gas.query import AppointmentQuerySet, OrderQuerySet, GASMemberQuerySet

import logging

log = logging.getLogger(__name__)

class GASMemberManager(models.Manager):
    """
    A custom manager class for the `GASMember` model.
    """ 
    def get_query_set(self):
        """Specific queryset object for GASMember management.

        Default behaviour is to hide 
        - suspended GASMembers 
        - inactive Users
        """
        queryset_object = GASMemberQuerySet(self.model)
        queryset_object = queryset_object.exclude(is_suspended=True)
        queryset_object = queryset_object.exclude(person__user__is_active=False)
        return queryset_object

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
        if order is None:
            people = Person.objects.filter(order_set__isnull=False)
        else:
            people = [order.referrer_person]
        return self.model.objects.filter(person__in=people)

    def delivery_referrers(self, order=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Delivery Referrer'
        role for the GAS they belong to.    
        
        If a `order` argument is provided, the result set is filtered accordingly.
        """
        # TODO: UNITTEST needed !
        if order is None:
            people = Person.objects.filter(delivery_for_order_set__isnull=False)
        else:
            people = [order.referrer_person]
        return self.model.objects.filter(person__in=people)

    def withdrawal_referrers(self, order=None):
        """
        Return a QuerySet containing all GAS members who have been assigned the 'Withdrawal Referrer'
        role for the GAS they belong to.
        
        If an `order` argument is provided, the result set is filtered accordingly.    
        """
        # TODO: UNITTEST needed !
        if order is None:
            people = Person.objects.filter(withdrawal_for_order_set__isnull=False)
        else:
            people = [order.referrer_person]
        return self.model.objects.filter(person__in=people)

class IncludeSuspendedGASMemberManager(models.Manager):
    """Manager to retrieve ordinary behaviour"""

    def get_query_set(self):
        return QuerySet(self.model)

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

    def prepared(self):
        return self.get_query_set().prepared()

    def open(self):
        return self.get_query_set().open()

    def closed(self):
        return self.get_query_set().closed()
    
    def on_completion(self):
        return self.get_query_set().on_completion()
    
    def finalized(self):
        return self.get_query_set().finalized()
    
    def unpaid(self):
        return self.get_query_set().unpaid()

    def delivered(self):
        return self.get_query_set().delivered()
    
    def archived(self):
        return self.get_query_set().archived()
    
    def canceled(self):
        return self.get_query_set().canceled()
  

    def get_new_intergas_group_id(self):
        """Retrieve next available intergas group id."""

        #WARNING LF: this is not safe for concurrent requests
        #TODO Matteo: group_id should be implemented like SEQUENCE type in PostgreSQL
        # (see PostgreSQL doc) or similar behaviour emulation function. 
        # Max value should be obtained from an integer external to table rows.
        # Then perform atomic operation on get and increment an integer used as reference.

        _maxs = self.all().aggregate(Max('group_id'))
        log.warning("TODO Matteo: DANGER for concurrent requests!")
        log.debug("get_group_id %s " % _maxs)

        # get the maximum attribute from the first record and add 1 to it
        _group_id = _maxs.get('group_id__max') or 0 
        return _group_id + 1

