from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext, ugettext_lazy as _

import re, logging
log = logging.getLogger(__name__)

def attr_user_is_set(obj):
    """Validator to check if the user attr of an object is set"""

    if obj.user:
        log.debug("This person is a user")
    else:
        log.debug("This person is not a user")
        raise ValidationError("This person is not a user of the site")


class PhoneValidator(RegexValidator):

    def __call__(self, value):
        return super(PhoneValidator,self).__call__(value)

phone_re = re.compile(
    r"(^[ ]*[+]?[\(\)0-9/\/\.\- ]+$)"
)
validate_phone = PhoneValidator(phone_re, _(u'Enter a valid phone number.'), 'invalid')

