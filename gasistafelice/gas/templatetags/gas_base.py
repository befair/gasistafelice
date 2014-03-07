
from django import template
from django.utils.translation import ugettext as _


register = template.Library()

@register.simple_tag
def render_gas(gas):
    return u"%s - %s (%s ordini = %s euro)" % (
        gas, gas.city,
        gas.orders.count(), gas.balance_suppliers
    )

@register.simple_tag
def render_gas_as_tr(gas):
    return u"<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (
        gas, gas.city,
        gas.orders.archived().count(), gas.balance_suppliers
    )
