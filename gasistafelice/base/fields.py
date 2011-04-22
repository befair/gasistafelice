"""Custom model fields go here"""

from django.db import models

class CurrencyField(models.FloatField):
    """Subclass of FloatField.

    It must be positive
    """

    #TODO: init float field with positive validator
    pass
