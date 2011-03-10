from django.db import models

from gasistafelice.base import const as role

class GASRolesManager(models.Manager):

    def tech_referrers(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_TECH)

    def cash_referrers(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_CASH)

    def supplier_referrers(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_TECH)

    def order_referrers(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_TECH)

    def withdraw_referrers(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_TECH)

    def delivery_referrerss(self):
        return self.get_query_set().filter(roles__name__exact=role.GAS_REFERRER_TECH)


