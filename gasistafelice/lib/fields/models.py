"""Custom model fields go here"""

from django.db import models
from django.core import exceptions
import decimal

#-----------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------

class PyPrettyDecimal(decimal.Decimal):

    def __unicode__(self):
        # TODO: to improve with decimal properties ?!?
        mod = self - int(self)
        if not mod:
            rv = int(self)
        else:
            rv = self.quantize(mod.normalize())
        return unicode(rv)

class PrettyDecimalField(models.DecimalField):

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return value
        try:
            return PyPrettyDecimal(value)
        except decimal.InvalidOperation:
            raise exceptions.ValidationError(self.error_messages['invalid'])


