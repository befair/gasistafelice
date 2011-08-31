"""Custom model fields go here"""

from django.db import models

class CurrencyField(models.DecimalField):
    """Subclass of DecimalField.
    It must be positive.

    We do not want to round up to second decimal here.
    We will do it in a place suitable for views.
    """

    def __init__(self, *args, **kw):
        kw['max_digits'] = 10
        kw['decimal_places'] = 4
        super(CurrencyField, self).__init__(*args, **kw)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], [
    "^gasistafelice\.base\.fields\.CurrencyField",
    "^current_user\.models\.CurrentUserField",
])

