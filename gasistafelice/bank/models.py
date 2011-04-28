from django.db import models

from django.utils.translation import ugettext_lazy as _

from permissions.models import Role
from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import Resource, Person

from django.db import models
from decimal import Decimal

class Account(models.Model):
    """An current account. Dispose of the current state and a list of financial opertion say as movements 
    A GAS have two accounts
    A GASMember have one account 
    A supplier have one account for each GAS. So the Account is linked to the solidal pact act
    A supplier has as many accounts as he has solidal pact act
    """

    #TODO: This is the basis of the economic part. To discuss and extend
    balance = CurrencyField(default=Decimal("0"))
    #COMMENT: DecimalField --> 84 table on MySQL FloatField --> 84 table
    #COMMENT fero: what does this mean?

    def __unicode__(self):
        #FIXME: Caught TypeError while rendering: coercing to Unicode: need string or buffer, Decimal found
        #return self.balance
        return _("%(balance)s") % {'balance' : self.balance}

class Movement(models.Model):
    """Economic movement

    """
    #TODO: This is the basis of the economic part. To discuss and extend
    account = models.ForeignKey(Account)
    amount = CurrencyField()
    causal = models.CharField(max_length=512, help_text=_("causal of economic movement"))	

    def __unicode__(self):
        return _("%(amount)s (causal: %(causal)s)") % {'amount' : self.amount, 'causal' : self.causal}

