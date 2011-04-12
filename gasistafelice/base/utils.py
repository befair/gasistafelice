from django.contrib.contenttypes.models import ContentType

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
        ctype = ContentType.objects.get(app_label=app_label, model=model_name)
        return ctype        
    except:
        return None 
