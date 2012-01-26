
from django.core.validators import RegexValidator
from django.utils.translation import ugettext, ugettext_lazy as _

import re

class PhoneValidator(RegexValidator):

    def __call__(self, value):
        return super(PhoneValidator,self).__call__(value)

phone_re = re.compile(
    r"(^[ ]*[+]?[\(\)0-9/\/\.\- ]+$)"
)
validate_phone = PhoneValidator(phone_re, _(u'Enter a valid phone number.'), 'invalid')

