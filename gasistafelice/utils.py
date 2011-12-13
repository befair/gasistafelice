from django.conf import settings

def queryset_from_iterable(model, iterable):
    """
    Take a model class and an iterable containing instances of that model; 
    return a ``QuerySet`` containing exactly those instances (barring duplicates, if any).
    
    If ``iterable`` contains an object that isn't an instance of ``model``, raise ``TypeError``.
    """
    # collect the set of IDs (i.e. primary keys) of model instances
    # contained in the given iterable (using a ``set`` object as accumulator, 
    # in order to avoid duplicates)
    id_set = set()
    for obj in iterable:
        if obj.__class__ == model:
            id_set.add(obj.pk)
        else:
            raise TypeError(_(u"Can't create a %(model)s QuerySet: %(obj)s is not an instance of model %(model)s"))
    qs = model._default_manager.filter(pk__in=id_set)
    return qs

#-----------------------------------------------------------------------------------

def long_date(d):
    return d.strftime(settings.LONG_DATE_FMT).decode('utf-8')

def medium_date(d):
    return d.strftime(settings.MEDIUM_DATETIME_FMT).decode('utf-8')

