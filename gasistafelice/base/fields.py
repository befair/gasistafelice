"""Custom model fields go here"""

from django.db import models

class CurrencyField(models.DecimalField):
    """Subclass of DecimalField.

    It must be positive
    """

    def __init__(self, *args, **kw):
        kw['max_digits'] = 10
        kw['decimal_places'] = 4
        super(CurrencyField, self).__init__(*args, **kw)

#THIS IS BETTER but does not work (in MySQL at least)
#refer to http://stackoverflow.com/questions/2013835/django-how-should-i-store-a-money-value
#FIXME: Caught ValueError while rendering: incomplete format TemplateSyntaxError
#I ran into an python locale issue with the DecimalField?. During MySQL INSERTs and UPDATEs invalid sql-statements are generated since a comma-seperator ',' is used for formating DecimalField? instead of the expected dot-seperator '.' 
#USE_L10N is set to true and LANGUAGE_CODE to it-IT

#from django.db import models
#from decimal import Decimal
#
#class CurrencyField(models.DecimalField):
#    __metaclass__ = models.SubfieldBase
#
#    def to_python(self, value):
#        try:
#           return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
#        except AttributeError:
#           return None
#

