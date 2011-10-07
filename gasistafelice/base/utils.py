from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

import os, datetime

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


def get_resource_icon_path(instance, filename):

    if instance.pk:
        return instance.icon.name

    ext = filename.split('.')[-1]
    d = datetime.datetime.today()
    filename = "%s-%s.%s" % (d.strftime("%Y-%m-%s"), slugify(instance.name), ext)
    return os.path.join('images/%s' % instance.resource_type, filename)

