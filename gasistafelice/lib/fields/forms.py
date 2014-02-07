
from django.forms import DecimalField
from lib.fields.models import PyPrettyDecimal

from decimal import Decimal, DecimalException
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils import formats
from django.utils.encoding import smart_str

class PrettyDecimalField(DecimalField):

    def to_python(self, value):
        """
        Validates that the input is a decimal number. Returns a Decimal
        instance. Returns None for empty values. Ensures that there are no more
        than max_digits in the number, and no more than decimal_places digits
        after the decimal point.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        value = smart_str(value).strip()
        try:
            value = PyPrettyDecimal(value)
        except DecimalException:
            raise ValidationError(self.error_messages['invalid'])
        return value

class TolerantDecimalField(DecimalField):

    def clean(self, value):

        if value is not None:
            dot_pos = value.rfind('.')
            comma_pos = value.rfind(',')

            if comma_pos > dot_pos:
                value = value[:comma_pos] + '.' + value[comma_pos+1:]

        return super(TolerantDecimalField, self).clean(value)

class CurrencyField(TolerantDecimalField):
    """CurrencyField that accept ',' and '.' as decimal separator"""

    def __init__(self, *args, **kw):
        kw['min_value'] = 0
        kw['decimal_places'] = 4
        super(CurrencyField, self).__init__(*args, **kw)

