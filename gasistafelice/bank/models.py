from django.db import models

from django.utils.translation import ugettext_lazy as _

from permissions.models import Role
from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import Resource, Person

class Account(models.Model):
    """An current account. Dispose of the current state and a list of financial opertion say as movements 
    A GAS have two accounts
    A GASMember have one account 
    A supplier have one account for one GAS. So the Account is link to the solidal pact act
    A supplier have as many accounts as he have solidal pact act

    """
    #TODO: This is the basis of the economic part. To discuss and extend
    balance = models.DecimalField(max_digits=10, decimal_places=4)

    def __unicode__(self):
        return _("balance: %") % {'balance' : self.balance}

class Movement(models.Model):
    """Economic movement

    """
    #TODO: This is the basis of the economic part. To discuss and extend
    account = models.ForeignKey(Account)
    balance = CurrencyField(max_digits=10, decimal_places=4)
    causal = models.CharField(max_length=200, help_text=_("causal of economic movement"))	

    def __unicode__(self):
        return _("causal: %") % {'causal' : self.causal}

