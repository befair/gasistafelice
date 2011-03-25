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
    
    ## States in which a SupplierOrder can be
    state_data = (
             # (key, state name),
              ('open', "Open"), # SupplierOrder is open; Gas members are allowed to issue GASMemberOrders
              ('closed', "Closed"), # SupplierOrder is closed; GasMemberOrders are disabled 
              ('on_completion', "On completion"), # SupplierOrder was closed, but some constraints were not satisfied, so a completion procedure was started 
              ('finalized', "Finalized"), # SupplierOrder was finalized (no more chances left for reopening)
              ('sent', "Sent"), # SupplierOrder was sent to the Supplier
              ('delivered', "Delivered"), # SupplierOrder was delivered to the GAS
              ('canceled', "Canceled"),# SupplierOrder was canceled
              #(exception_raised,"Exception raised")
              )
    
    # create States objects
    states = {} # dictionary containing State objects for the current Workflow 
    for (key, name) in state_data:
        states[key] = State.objects.create(name=_(name), workflow=workflow )
       
        
    ## Transitions allowed among States defined for a SupplierOrder
    
    transition_data = ( 
                    # (key, transition name, destination state), 
                    ('close', "Close", 'closed'), # close the SupplierOrder
                    ('reopen', "Reopen", 'open'), # re-open the SupplierOrder
                    ('start_completion', "Start completion", 'on_completion'), # start the completion procedure for the SupplierOrder
                    ('end_completion', "End completion", 'closed'), # end the completion procedure for the SupplierOrder
                    ('finalize', "Finalize", 'finalized'), # finalize the SupplierOrder
                    ('send', "Send", 'sent'), # send the SupplierOrder to the Supplier
                    ('set_delivered', "Set delivered", 'delivered'), # mark the SupplierOrder as "delivered"
                    ('cancel', "Cancel", 'canceled'), # cancel the SupplierOrder                                     
                       )
    # create Transition objects
    transitions = {} # dictionary containing Transition objects for the current Workflow
    for (key, transition_name, destination) in transition_data:
        transitions[key] = Transition.objects.create(name=_(transition_name), workflow=workflow, destination=states[destination])
    
    
    ## associate Transitions to States
    state_transition_map = (
                              # (state name, transition name), 
                              ('open', 'close'),
                              ('closed', 'reopen'),
                              ('closed', 'finalize'),
                              ('closed', 'start_completion'),
                              ('on_completion', 'end_completion'),
                              ('finalized', 'sent'),
                              # SupplierOrder may be canceled at every time before delivery
                              ('open', 'cancel'),
                              ('close', 'cancel'),
                              ('on_completion', 'cancel'),
                              ('finalized', 'cancel'),
                              ('sent', 'cancel'),
                              )

    for (state, transition) in state_transition_map:
        states[state].transitions.add(transitions[transition])
           
    workflow.initial_state = open
    workflow.save()
