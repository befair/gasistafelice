
from django import template
from django.utils.translation import ugettext as _


register = template.Library()

@register.simple_tag
def render_gas(gas):
    return u"%s - %s (%s ordini = %s euro)" % (
        gas, gas.city, 
        gas.orders.count(), gas.balance_suppliers
    )
