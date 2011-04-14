from django import template
from django.conf import settings
from django.template import resolve_variable, loader
from django.template import TemplateSyntaxError
from django.template.loader import get_template, select_template

from django.utils.translation import ugettext as _
from django.core import urlresolvers
import datetime, os.path

register = template.Library()

@register.simple_tag
def des_admin_nav():
    # Inspired from django-pki

    menu = {
        'orders_open' : { 
            'label' : _("Open orders"), 
            'url' : urlresolvers.reverse('gas_admin:gas_gassupplierorder_changelist')
        },
        'products_ordered' : {
            'label' : _("Products ordered"),
            'url' : urlresolvers.reverse('gas_admin:gas_gasmemberorder_changelist')
        }
    }

    
    rv = """
    <div id="des-admin-nav">
        <ul>
    """

    for k,v in menu.items():

        rv += '<li><a href="%(url)s">%(label)s</a></li>' % v

    rv += """
        </ul>
    </div>""" 

    return rv
