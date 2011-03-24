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

   # default Workflow for a SupplierOrder 
    workflow = Workflow.objects.create(name="SupplierOrderDefault")
    
    ## in which States a SupplierOrder can be
    # SupplierOrder is open; Gas members are allowed to issue GASMemberOrders
    open = State.objects.create(name=_("Open"), workflow=workflow)
    # SupplierOrder is closed; GasMemberOrders are disabled 
    closed = State.objects.create(name=_("Closed"), workflow=workflow)
    # SupplierOrder was closed, but some constraints were not satisfied,
    # so a completion procedure was started 
    on_completion = State.objects.create(name=_("On completion"), workflow=workflow)
    # SupplierOrder was finalized (no more chances left for reopening)
    finalized = State.objects.create(name=_("Finalized"), workflow=workflow)
    # SupplierOrder was sent to the Supplier
    sent = State.objects.create(name=_("Sent"), workflow=workflow)
    # SupplierOrder was delivered to the GAS
    delivered = State.objects.create(name=_("Delivered"), workflow=workflow)
    # SupplierOrder was canceled
    canceled = State.objects.create(name=_("Canceled"), workflow=workflow)
    # exception_raised = State.objects.create(name=_("Exception raised"), workflow=workflow)
        
    ## Transitions allowed among States defined for a SupplierOrder
    # close the SupplierOrder
    close = Transition.objects.create(name=_("Close"), workflow=workflow, destination=closed)
    # re-open the SupplierOrder
    reopen = Transition.objects.create(name=_("Reopen"), workflow=workflow, destination=open)
    # start the completion procedure for the SupplierOrder
    start_completion = Transition.objects.create(name=_("Star completion"), workflow=workflow, destination=on_completion)
    # end the completion procedure for the SupplierOrder
    end_completion = Transition.objects.create(name=_("Star completion"), workflow=workflow, destination=closed)
    # finalize the SupplierOrder
    finalize = Transition.objects.create(name=_("Finalize"), workflow=workflow, destination=finalized)
    # send the SupplierOrder to the Supplier
    send = Transition.objects.create(name=_("Send"), workflow=workflow, destination=sent)
    # mark the SupplierOrder as "delivered"
    set_delivered = Transition.objects.create(name=_("Set delivered"), workflow=workflow, destination=delivered)
    # cancel the SupplierOrder
    cancel = Transition.objects.create(name=_("Canceled"), workflow=workflow, destination=canceled)
    
    ## associate Transitions to States
    open.transitions.add(close)
    closed.transitions.add(reopen)
    closed.transitions.add(finalize)
    closed.transitions.add(start_completion)
    on_completion.transitions.add(end_completion)
    finalized.transitions.add(sent)
    sent.transitions.add(set_delivered)
    # SupplierOrder may be canceled at every time before delivery
    # FIXME: remove boilerplate (for loop ?)
    open.transitions.add(cancel)
    close.transitions.add(cancel)
    on_completion.transitions.add(cancel)
    finalized.transitions.add(cancel)
    sent.transitions.add(cancel)
       
    workflow.initial_state = open
    workflow.save()
