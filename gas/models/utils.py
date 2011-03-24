from django.utils.translation import ugettext as _

from workflows.models import Workflow, State, Transition
from base.models import WorkflowDefaultTransitionOrder
from permissions.utils import register_role
from permissions.utils import register_role

def init_workflow():

    # GASMemberOrder simplest workflow
    workflow = Workflow.objects.create(name="GASMemberOrderSimple")

    confirmed = State.objects.create(name=_("Confirmed"), workflow=workflow)
    finalized = State.objects.create(name=_("Finalized"), workflow=workflow)
    delivered = State.objects.create(name=_("Ready for withdraw"), workflow=workflow)
    withdrawn = State.objects.create(name=_("Withdrawn"), workflow=workflow)
    canceled = State.objects.create(name=_("Canceled"), workflow=workflow)
    #TODO? exception_raised = State.objects.create(name=_("Exception raised"), workflow=workflow)

    finalize = Transition.objects.create(name=_("Finalize"), workflow=workflow, destination=finalized)
    deliver = Transition.objects.create(name=_("Deliver"), workflow=workflow, destination=delivered)
    withdraw = Transition.objects.create(name=_("Withdraw"), workflow=workflow, destination=withdrawn)
    cancel = Transition.objects.create(name=_("Cancel"), workflow=workflow, destination=canceled)

    confirmed.transitions.add(finalize)
    confirmed.transitions.add(cancel)
    finalized.transitions.add(deliver)
    delivered.transitions.add(withdraw)

    workflow.initial_state = confirmed
    workflow.save()

    workflow.defaultworkflowtransitionorder_set.add(transition=finalize, order=1)
    workflow.defaultworkflowtransitionorder_set.add(transition=deliver, order=2)
    workflow.defaultworkflowtransitionorder_set.add(transition=withdraw, order=3)

    #GASMember Order full workflow
    workflow = Workflow.objects.create(name="GASMemberOrderFull")

    unconfirmed = State.objects.create(name=_("Unconfirmed"), workflow=workflow)
    confirmed = State.objects.create(name=_("Confirmed"), workflow=workflow)
    finalized = State.objects.create(name=_("Finalized"), workflow=workflow)
    sent = State.objects.create(name=_("Sent"), workflow=workflow)
    delivered = State.objects.create(name=_("Ready for withdraw"), workflow=workflow)
    withdrawn = State.objects.create(name=_("Withdrawn"), workflow=workflow)
    not_withdrawn = State.objects.create(name=_("NOT Withdrawn"), workflow=workflow) #COMMENT: is it useful to know what has been delivered but not withdrawn
    #charged COMMENT: is it useful to make an automatic state update when order is charged by economist?
    canceled = State.objects.create(name=_("Canceled"), workflow=workflow)
    #TODO exception_raised = State.objects.create(name=_("Exception raised"), workflow=workflow)

    confirm = Transition.objects.create(name=_("Confirm"), workflow=workflow, destination=confirmed)
    finalize = Transition.objects.create(name=_("Finalize"), workflow=workflow, destination=finalized)
    send = Transition.objects.create(name=_("Send"), workflow=workflow, destination=sent) #COMMENT: is it useful?
    deliver = Transition.objects.create(name=_("Deliver"), workflow=workflow, destination=delivered)
    withdraw = Transition.objects.create(name=_("Withdraw"), workflow=workflow, destination=withdrawn)
    left_there = Transition.objects.create(name=_("Make not Withdrawn"), workflow=workflow, destination=not_withdrawn)
    cancel = Transition.objects.create(name=_("Cancel"), workflow=workflow, destination=canceled)

    unconfirmed.transitions.add(confirm)
    confirmed.transitions.add(finalize)
    confirmed.transitions.add(cancel)
    finalized.transitions.add(send)
    sent.transitions.add(deliver)
    delivered.transitions.add(withdraw)
    delivered.transitions.add(left_there)

    workflow.initial_state = unconfirmed
    workflow.save()

    workflow.defaultworkflowtransitionorder_set.add(transition=confirm, order=1)
    workflow.defaultworkflowtransitionorder_set.add(transition=finalized, order=2)
    workflow.defaultworkflowtransitionorder_set.add(transition=sent, order=3)
    workflow.defaultworkflowtransitionorder_set.add(transition=deliver, order=4)
    workflow.defaultworkflowtransitionorder_set.add(transition=withdraw, order=4)

    # SupplierOrder Default Workflow
#TODO TODO TODO
#    workflow = Workflow.objects.create(name="SupplierOrderDefault")
#
#    open = State.objects.create(name=_("Open"), workflow=workflow)
#    closed = State.objects.create(name=_("Closed"), workflow=workflow)
#    finalizing = State.objects.create(name=_("Finalizing"), workflow=workflow)
#    finalized = State.objects.create(name=_("Finalized"), workflow=workflow)
#    sent = State.objects.create(name=_("Sent"), workflow=workflow)
#    delivered = State.objects.create(name=_("Delivered"), workflow=workflow)
#    exception_raised = State.objects.create(name=_("Exception raised"), workflow=workflow)
#    
#    
#
#    close = Transition.objects.create(name=_("Close"), workflow=workflow, destination=closed)
#    arrange = Transition.objects.create(name=_("Arrange"), workflow=workflow, destination=finalizing)
#    finalize = Transition.objects.create(name=_("Finalize"), workflow=workflow, destination=finalized)
#
#    open.transitions.add(close)
#    open.transitions.add(arrange)
#    open.transitions.add(finalize)
#
#    #TODO
#    workflow.initial_state = open
#    workflow.save()
