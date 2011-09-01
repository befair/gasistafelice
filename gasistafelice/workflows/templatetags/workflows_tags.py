# django imports
from django import template

# workflows imports
import gasistafelice.workflows.utils

register = template.Library()

@register.inclusion_tag('workflows/transitions.html', takes_context=True)
def transitions(context, obj):
    """
    """
    request = context.get("request")
    
    return {
        "transitions" : gasistafelice.workflows.utils.get_allowed_transitions(obj, request.user),
        "state" : gasistafelice.workflows.utils.get_state(obj),
    }
