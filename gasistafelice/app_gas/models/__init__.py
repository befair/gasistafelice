"""These models include everything necessary to manage GAS activity.

They rely on base models and Supplier-related ones to get Product and Stock infos.

Definition: `Vocabolario - GAS <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#GAS>`__ (ITA only)
"""
 
from app_gas.models.base import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact, GASConfig, GASActivist
from app_gas.models.order import GASSupplierOrder, GASSupplierOrderProduct, GASMemberOrder, Delivery, Withdrawal

# Signals catching
from django.db.models.signals import post_save
from django.conf import settings

from workflows.utils import get_allowed_transitions, do_transition, get_workflow, set_workflow
from workflows.models import Transition

from app_gas.models.order import GASSupplierOrder

import datetime, logging

log = logging.getLogger(__name__)


def setup_order_workflow(sender, instance, created, **kwargs):

    if created:

        if not instance.workflow:
            # Set default workflow
            log.debug("Setting default workflow for %s" % instance)
            w = instance.gas.config.default_workflow_gassupplier_order
            set_workflow(instance, w)

        instance.open_if_needed()

post_save.connect(setup_order_workflow, sender=GASSupplierOrder)

## Signals
# setup accounting-related things for *every* model
# implementing a ``.setup_accounting()`` method.
def setup_non_subject_accounting(sender, instance, created, **kwargs):
    if created:
        # call the ``.setup_accounting()`` method on the sender model, if defined
        if getattr(instance, 'setup_accounting', None):     
            instance.setup_accounting()
        
post_save.connect(setup_non_subject_accounting, sender=GASMember)
post_save.connect(setup_non_subject_accounting, sender=GASSupplierSolidalPact)
