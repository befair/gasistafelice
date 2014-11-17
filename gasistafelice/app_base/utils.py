from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

import os
import datetime

def get_ctype_from_model_label(label):
    """
    This helper function takes a model identifier (a string of the form
    'app_label.model_name', where `app_label` is as in Django docs and `model_name`
    is the model class' name, and return the ContentType instance associated with 
    the model class. If the label is malformed or there is no model with that label, 
    return `None`.     
    """
    try:
        (app_label, model_name) = label.split('.')
        # ContenType framework expects lowercased model names
        model_name = model_name.lower()               
        ctype = ContentType.objects.get(app_label=app_label, model=model_name)
        return ctype        
    except:
        return None 

#-------------------------------------------------------------------------------
# Icon and file path management for resources

def get_resource_icon_path(instance, filename):
    return get_attr_file_path(instance, filename, "icon", base_path="images")

def get_association_act_path(instance, filename):
    return get_attr_file_path(instance, filename, "association_act")

def get_intent_act_path(instance, filename):
    return get_attr_file_path(instance, filename, "intent_act")

def get_pact_path(instance, filename):
    return get_attr_file_path(instance, filename, "pact")

def get_attr_file_path(instance, filename, attr_name, base_path="docs"):

    if instance.pk:
        old_instance = instance.__class__.objects.get(pk=instance.pk)
        old_name = getattr(old_instance, attr_name).name
        if old_name:
            return old_name

    ext = filename.split('.')[-1]
    d = datetime.datetime.today()
    filename = "%s-%s-%s.%s" % (d.strftime("%Y-%m-%s"), slugify(instance.name), attr_name, ext)
    return '%s/%s/%s' % (base_path, instance.resource_type, filename)


