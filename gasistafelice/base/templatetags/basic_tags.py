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

@register.simple_tag
def bool_img_not(value):
    return bool_img(not value)


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
        pt_list = ["values/"+data_type+".xml", "values/str.xml"]
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

#----------------------------------------------------------------------------------

class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""

def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)

#----------------------------------------------------------------------------------

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

register.tag('assign', do_assign)
