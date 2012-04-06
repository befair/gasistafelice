from django.core.exceptions import ValidationError

import logging
log = logging.getLogger(__name__)

def attr_user_is_set(obj):
    """Validator to check if the user attr of an object is set"""

    if obj.user:
        log.debug("This person is a user")
    else:
        log.debug("This person is not a user")
        raise ValidationError("This person is not a user of the site")
