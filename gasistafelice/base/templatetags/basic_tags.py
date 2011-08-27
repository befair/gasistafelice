from django import template
from django.conf import settings
from django.template import resolve_variable, loader
from django.template import TemplateSyntaxError
from django.template.loader import get_template, select_template

from django.db import models
import datetime, os.path

register = template.Library()

@register.simple_tag
def des_media_url():
    return settings.MEDIA_URL

@register.simple_tag
def des_debug():
    return settings.DEBUG

@register.simple_tag
def des_version():
    return settings.VERSION

@register.simple_tag
def bool_img(value):
    if bool(value):
        rv = '<img alt="True" src="/media/img/admin/icon-yes.gif">'
    else:
        rv = '<img alt="False" src="/media/img/admin/icon-no.gif">'
    return rv

#--------------------------------------------------------------------------------

class RenderXmlDetail(template.Node):

    def __init__(self, field):
        self.field = field
    
    def render(self, context):

        try:
            field = resolve_variable(self.field, context)
        except template.VariableDoesNotExist:
            raise template.VariableDoesNotExist, "Variable %s has not been found in the context" % self.field

        data_type = field['type']
        pt_list = ["values/"+data_type+".xml", "data/str.xml"]
        context['value'] = field['value']

        t = select_template(pt_list)
        rendered_data = t.render(context)

        return rendered_data

@register.tag
def render_xml_detail(parser, token):
    # Split arguments 
    try:
        arguments = token.split_contents()
        field = arguments[1]
    except:
        raise template.TemplateSyntaxError, "%r tag requires field as argument" % arguments[0]

    return RenderXmlDetail(field)
