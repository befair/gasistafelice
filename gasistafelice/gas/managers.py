from django.db import models

from gasistafelice.base import const as role

class GASRolesManager(models.Manager):

    def tech_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_TECH)

    def cash_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_CASH)

    def supplier_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_SUPPLIER)

    def order_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_ORDER)

    def withdraw_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_WITHDRAWAL)

    def delivery_referrers(self):
        return self.get_query_set().filter(role_set__name__exact=role.GAS_REFERRER_DELIVERY)


