"""
This module contains workflow-related data needed for GAS' order management.
"""

from django.utils.translation import ugettext as _
from django.db.models.signals import post_syncdb

from gasistafelice.base.models import WorkflowDefinition
import workflows

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
          ('canceled', "Canceled"), # GASMemberOrder has been canceled
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
                ('cancel', "Cancel", 'canceled'), # cancel a GASMemberOrder
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

w1 = WorkflowDefinition(name, state_list, transition_list, state_transition_map, initial_state_name, default_transitions)  

#----------------------------------------------------------------------------- 
## default Workflow for a SupplierOrder 
name="SupplierOrderDefault"
 
## States in which a SupplierOrder can be
state_list = (
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
  
     
## Transitions allowed among States defined for a SupplierOrder
 
transition_list = ( 
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
 
## Transitions-to-States map
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
       
initial_state = 'open'
 
## define default Transitions for States in a Workflow, 
## so we can suggest to end-users what the next "logical" State could be   
default_transitions = (
                        # (state name, transition name),                         
                        )
 
w2= WorkflowDefinition(name, state_list, transition_list, state_transition_map, initial_state_name, default_transitions)  

def init_workflows(sender, **kwargs):

    w1.register_workflow()
    w2.register_workflow()
    return

post_syncdb.connect(init_workflows, sender=workflows.models)

