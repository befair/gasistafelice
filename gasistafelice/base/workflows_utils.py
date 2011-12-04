
import workflows

# With this import we can use this utils file as the original workflows.utils
from workflows.utils import *

def get_allowed_transitions(obj, user):
    """Returns all allowed transitions for passed object and user. Takes the
    current state of the object into account.

    **Parameters:**

    obj
        The object for which the transitions should be returned.

    user
        The user for which the transitions are allowed.
    """
    from gasistafelice.gas.models import GASSupplierOrder, GASMemberOrder
    from flexi_auth.models import ParamRole
    from gasistafelice.consts import GAS_MEMBER, GAS_REFERRER_SUPPLIER, GAS_REFERRER_TECH, DES_ADMIN
        
    if isinstance(obj, GASSupplierOrder):
        param_roles =  [
             ParamRole.get_role(GAS_REFERRER_SUPPLIER, pact=obj.pact),
             ParamRole.get_role(GAS_REFERRER_TECH, gas=obj.gas),
             ParamRole.get_role(DES_ADMIN, des=obj.des),
        ]
    elif isinstance(obj, GASMemberOrder):
        param_roles = [
             ParamRole.get_role(GAS_MEMBER, obj.gas)
        ]

    else:
        return workflows.utils.get_allowed_transitions(obj, user)

    for pr in param_roles:
        if user in pr.get_users():
            rv = workflows.utils.get_allowed_transitions(obj, user)
        else:
            rv = []

    return rv 

#-------------------------------------------------------------------------------------
# Just moved do_transition here to let it use the new get_allowed_transitions function
#-------------------------------------------------------------------------------------

def do_transition(obj, transition, user):
    """Processes the passed transition to the passed object (if allowed).
    """
    if not isinstance(transition, Transition):
        try:
            transition = Transition.objects.get(name=transition)
        except Transition.DoesNotExist:
            return False

    transitions = get_allowed_transitions(obj, user)
    if transition in transitions:
        set_state(obj, transition.destination)
        return True
    else:
        return False

