
from django.forms import DecimalField

class CurrencyField(DecimalField):
    """CurrencyField that accept ',' and '.' as decimal separator"""

    def __init__(self, *args, **kw):
        kw['min_value'] = 0
        kw['decimal_places'] = 4
        super(CurrencyField, self).__init__(*args, **kw)

    def clean(self, value):
        dot_pos = value.rfind('.')
        comma_pos = value.rfind(',')

        if comma_pos > dot_pos:
            new_value = value[:comma_pos] + '.' + value[comma_pos+1:]
        else:
            new_value = value

        return super(CurrencyField, self).clean(new_value)


