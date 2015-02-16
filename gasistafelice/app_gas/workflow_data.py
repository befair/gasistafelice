"""
This module contains workflow-related data needed for GAS' order management.
"""

#FIXME: translation SHOULD happen at run-time!
from django.utils.translation import ugettext as _

from app_base.models import WorkflowDefinition

STATUS_PREPARED = "Prepared"
STATUS_OPEN = "Open"
STATUS_CLOSED = "Closed"
STATUS_UNPAID = "Unpaid"
STATUS_ARCHIVED = "Archived"
STATUS_CANCELED = "Canceled"

TRANSITION_OPEN = "Open"
TRANSITION_CLOSE = "Close"
TRANSITION_ARCHIVE = "Archive"
TRANSITION_UNPAID = "MAKE UNPAID"
TRANSITION_CLOSE_EMAIL = "Close and send"
TRANSITION_CANCEL = "Cancel"

# a dictionary containing all workflows declarations (as `WorkflowDefinition` objects)
# listed in this module, keyed by name 
workflow_dict = {}

#-----------------------------------------------------------------------------
## default Workflow for a GASMemberOrder
    
name = "GASMemberOrderDefault"   
       
## States in which a GASMemberOrder can be
state_list = (
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
          ('canceled', STATUS_CANCELED), # GASMemberOrder has been canceled
          #(exception_raised,"Exception raised")
          )
     
## Transitions allowed among States defined for a GASMemberOrder 
transition_list = ( 
                # (key, Transition name, destination State), 
                ('confirm', "Confirm", 'confirmed'), # GASMember has confirmed its GASMemberOrder
                ('unconfirm', "Unconfirm", 'unconfirmed'), # GASMember has un-confirmed its GASMemberOrder
                ('finalize', "Finalize", 'finalized'), # finalize the GASMemberOrder (usually is a side-effect of the associated SupplierOrder being finalized)
                ('send', "Send", 'sent'), # GASMemberOrder has been sent to the Supplier (as a side-effect of the SupplierOrder it belongs to being sent)
                ('make_ready', "Make ready", 'ready'), # flag a GASMemberOrder as 'available for withdrawal' 
                ('set_withdrawn', "Set withdrawn", 'withdrawn'), # flag a GASMemberOrder as 'withdrawn by the GASMember who issued it'
                ('set_not_withdrawn', "Set not withdrawn", 'not_withdrawn'), # flag a GASMemberOrder as 'not withdrawn by the GASMember who issued it'
                ('cancel', TRANSITION_CANCEL, 'canceled'), # cancel a GASMemberOrder
                   )
   
## Transitions-to-States map
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

initial_state_name = 'unconfirmed'    

## define default Transitions for States in a Workflow, 
## so we can suggest to end-users what the next "logical" State could be   
default_transitions = (
                       # (state name, transition name),
                        ('unconfirmed', 'confirm'),
                        ('confirmed', 'finalize'),
                        ('finalized', 'send'),
                        ('sent', 'make_ready'),
                        ('ready', 'set_withdrawn'),
                       )
  
workflow_dict[name] = WorkflowDefinition(name, state_list, transition_list, state_transition_map, initial_state_name, default_transitions)

#----------------------------------------------------------------------------- 
## default Workflow for a SupplierOrder 
name="SupplierOrderDefault"
 
## States in which a SupplierOrder can be
state_list = (
          # (key, state name),
           ('open', STATUS_OPEN), # SupplierOrder is open; Gas members are allowed to issue GASMemberOrders
           ('closed', STATUS_CLOSED), # SupplierOrder is closed; GasMemberOrders are disabled 
           ('on_completion', "On completion"), # SupplierOrder was closed, but some constraints were not satisfied, so a completion procedure was started 
           ('finalized', "Finalized"), # SupplierOrder was finalized (no more chances left for reopening)
           ('sent', "Sent"), # SupplierOrder was sent to the Supplier
           ('delivered', "Delivered"), # SupplierOrder was delivered to the GAS
           ('archived', STATUS_ARCHIVED), # SupplierOrder was delivered to and processed by the GAS
           ('canceled', STATUS_CANCELED),# SupplierOrder was canceled
           #(exception_raised,"Exception raised")
)

     
## Transitions allowed among States defined for a SupplierOrder
 
transition_list = ( 
                 # (key, transition name, destination state), 
                 ('close', TRANSITION_CLOSE, 'closed'), # close the SupplierOrder
                 ('reopen', "Reopen", 'open'), # re-open the SupplierOrder
                 ('start_completion', "Start completion", 'on_completion'), # start the completion procedure for the SupplierOrder
                 ('end_completion', "End completion", 'closed'), # end the completion procedure for the SupplierOrder
                 ('finalize', "Finalize", 'finalized'), # finalize the SupplierOrder
                 ('send', "Send", 'sent'), # send the SupplierOrder to the Supplier
                 ('set_delivered', "Set delivered", 'delivered'), # mark the SupplierOrder as "delivered"
                 ('archive', TRANSITION_ARCHIVE, 'archived'), # mark the SupplierOrder as "archived" (do not display anymore)
                 ('cancel', TRANSITION_CANCEL, 'canceled'), # cancel the SupplierOrder                                     
)
 
## Transitions-to-States map
# FIXME: should be a dictionary
state_transition_map = (
                           # (state name, transition name), 
                           ('open', 'close'),
                           ('closed', 'reopen'),
                           ('closed', 'finalize'),
                           ('closed', 'start_completion'),
                           ('on_completion', 'end_completion'),
                           ('finalized', 'send'),
                           ('sent', 'set_delivered'),
                           ('delivered', 'archive'),
                           # SupplierOrder may be canceled at any time before delivery happens
                           ('open', 'cancel'),
                           ('closed', 'cancel'),
                           ('on_completion', 'cancel'),
                           ('finalized', 'cancel'),
                           ('sent', 'cancel'),
                           )
       
initial_state_name = 'open'
 
## define default Transitions for States in a Workflow, 
## so we can suggest to end-users what the next "logical" State could be   
# FIXME: should be a dictionary
default_transitions = (
                        # (state name, transition name),                         
                        )
 
workflow_dict[name] = WorkflowDefinition(name, state_list, transition_list, state_transition_map, initial_state_name, default_transitions)

#----------------------------------------------------------------------------- 
## default Workflow for a SupplierOrder 
name="SimpleSupplierOrderDefault"

## States in which a SupplierOrder can be
state_list = (
          # (key, state name),
           ('prepared', STATUS_PREPARED), # SupplierOrder has been created
           ('open', STATUS_OPEN), # SupplierOrder is open; Gas members are allowed to issue GASMemberOrders
           ('closed', STATUS_CLOSED), # SupplierOrder is closed; GasMemberOrders are disabled 
           ('unpaid', STATUS_UNPAID), # SupplierOrder is unpaid (gas cash registered, but not paid to supplier)
           ('archived', STATUS_ARCHIVED), # SupplierOrder is archived 
           ('canceled', STATUS_CANCELED),# SupplierOrder was canceled
           #(exception_raised,"Exception raised")
)

     
## Transitions allowed among States defined for a SupplierOrder
 
transition_list = ( 
    # (key, transition name, destination state), 
    ('open', TRANSITION_OPEN, 'open'), # close the SupplierOrder
    ('close', TRANSITION_CLOSE, 'closed'), # close the SupplierOrder
    ('close_and_send', TRANSITION_CLOSE_EMAIL, 'closed'), # close the SupplierOrder
    ('archive', TRANSITION_ARCHIVE, 'archived'), # make the SupplierOrder disappear from ordinary operations
    ('make_unpaid', TRANSITION_UNPAID, 'unpaid'), # cancel the SupplierOrder 
    ('cancel', TRANSITION_CANCEL, 'canceled'), # cancel the SupplierOrder 
)
 
## Transitions-to-States map
# FIXME: should be a dictionary
state_transition_map = (
    # (state name, transition name), 
    ('prepared', 'open'),
    ('open', 'close'),
    ('open', 'close_and_send'),
    ('closed', 'archive'),
    ('closed', 'make_unpaid'),
    ('unpaid', 'archive'),
    # SupplierOrder may be canceled at any time before delivery happens
    ('open', 'cancel'),
    ('closed', 'cancel'),
    ('prepared', 'cancel'),
)
       
initial_state_name = 'prepared'
 
## define default Transitions for States in a Workflow, 
## so we can suggest to end-users what the next "logical" State could be   
# FIXME: should be a dictionary
default_transitions = (
                        # (state name, transition name),                         
                        )
 
workflow_dict[name] = WorkflowDefinition(name, state_list, transition_list, state_transition_map, initial_state_name, default_transitions)
