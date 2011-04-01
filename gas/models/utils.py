from django.utils.translation import ugettext as _

from workflows.models import Workflow, State, Transition
from base.models import WorkflowDefaultTransitionOrder
from permissions.utils import register_role

def init_workflow():

#-----------------------------------------------------------------------------
    # default Workflow for a GASMemberOrder 
    workflow = Workflow.objects.create(name="GASMemberOrderDefault")
        
    ## States in which a GASMemberOrder can be
    state_data = (
             # (key, State name),
              ('unconfirmed', "Unconfirmed"), # GASMemberOrder has not been confirmed by the GASMember yet 
              ('confirmed', "Confirmed"), # GASMemberOrder has been confirmed by GASMember
              ('finalized', "Finalized"), # SupplierOrder has been closed, so GASMemberOrders can't be changed anymore
              # TODO: is really necessary ?
              ('sent', "Sent"), # GASMemberOrder has been sent to the Supplier
              ('ready', "Ready for withdraw"), # GASMemberOrder is ready for withdrawal
              ('withdrawn', "Withdrawn"), # GASMemberOrder has been withdrawn by the GASMember who issued it
              ('not_withdrawn', "Not withdrawn"), # GASMemberOrder hasn't been withdrawn in due time by the GASMember who issued it
              #COMMENT: is it useful to know what has been delivered but not withdrawn
              #charged COMMENT: is it useful to make an automatic state update when order is charged by economist?
              ('canceled', "Canceled"), # GASMemberOrder has been canceled
              #(exception_raised,"Exception raised")
              )
    
    # create States objects
    states = {} # dictionary containing State objects for the current Workflow 
    for (key, name) in state_data:
        states[key] = State.objects.create(name=_(name), workflow=workflow )
     
    ## Transitions allowed among States defined for a GASMemberOrder 
    transition_data = ( 
                    # (key, Transition name, destination State), 
                    ('confirm', "Confirm", 'confirmed'), # GASMember has confirmed its GASMemberOrder
                    ('unconfirm', "Unconfirm", 'unconfirmed'), # GASMember has un-confirmed its GASMemberOrder
                    ('finalize', "Finalize", 'finalized'), # finalize the GASMemberOrder (usually is a side-effect of the associated SupplierOrder being finalized)
                    ('send', "Send", 'sent'), # GASMemberOrder has been sent to the Supplier (as a side-effect of the SupplierOrder it belongs to being sent)
                    ('make_ready', "Make ready", 'ready'), # flag a GASMemberOrder as 'available for withdrawal' 
                    ('set_withdrawn', "Set withdrawn", 'withdrawn'), # flag a GASMemberOrder as 'withdrawn by the GASMember who issued it'
                    ('set_not_withdrawn', "Set not withdrawn", 'not_withdrawn'), # flag a GASMemberOrder as 'not withdrawn by the GASMember who issued it'
                    ('cancel', "Cancel", 'canceled'), # cancel a GASMemberOrder
                       )
    # create Transition objects
    transitions = {} # dictionary containing Transition objects for the current Workflow
    for (key, transition_name, destination) in transition_data:
        transitions[key] = Transition.objects.create(name=_(transition_name), workflow=workflow, destination=states[destination])         
    
    ## associate Transitions to States
    state_transition_map = (
                              # (state name, transition name), 
                              ('unconfirmed', 'confirm'),
                              ('confirmed', 'unconfirm'),
                              ('confirmed', 'finalize'), 
                              ('finalized', 'send'),
                              ('sent', 'make_ready'),
                              ('ready', 'set_withdrawn'), 
                              ('ready', 'set_not_withdrawn'),
                              # GASMemberOrder may be canceled at any time before delivery happens
                              ('confirmed', 'cancel'),
                              ('finalized', 'cancel'),
                              ('sent', 'cancel'),
                              )

    for (state, transition) in state_transition_map:
        states[state].transitions.add(transitions[transition])
           
    workflow.initial_state = states['unconfirmed']    
    workflow.save()

    workflow.defaultworkflowtransitionorder_set.add(transition=confirm, order=1)
    workflow.defaultworkflowtransitionorder_set.add(transition=finalized, order=2)
    workflow.defaultworkflowtransitionorder_set.add(transition=sent, order=3)
    workflow.defaultworkflowtransitionorder_set.add(transition=deliver, order=4)
    workflow.defaultworkflowtransitionorder_set.add(transition=withdraw, order=4)
#----------------------------------------------------------------------------- 
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
                              # SupplierOrder may be canceled at any time before delivery happens
                              ('open', 'cancel'),
                              ('closed', 'cancel'),
                              ('on_completion', 'cancel'),
                              ('finalized', 'cancel'),
                              ('sent', 'cancel'),
                              )

    for (state, transition) in state_transition_map:
        states[state].transitions.add(transitions[transition])
           
    workflow.initial_state = states['open']
    workflow.save()
