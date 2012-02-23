
def get_qs_filter_dict_from_str(flt_string):
    """Given a string which represent a querySet filter, return a filter.

    Useful to be passed as **dict in filter() methods.
    """

    flt = {}

    # build filter
    if "," not in flt_string: 
        try:
            k,v = flt_string.split('=')
        except ValueError:
            raise
        flt[k] = v

    else:
        for couple in flt_string.split(','):
            try:
                k,v = couple.split('=')
            except ValueError:
                raise

            flt[k] = v
    return flt



def get_instance_dict_from_attrs(obj, attr_names):
    """Given a model instance and a list of attributes, returns a dict"""

    d = {}
    
    for attr_name in attr_names:
        # retrieve attributes and build dict for template
        
        # Support for nested attributes
        nested_attrs = attr_name.split('.')
        attr = obj
        for nested_attr in nested_attrs:
            attr = getattr(attr, nested_attr)

        if callable(attr):
            v = attr()
        else:
            v = attr
        d[attr_name] = v

    return d
    
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
