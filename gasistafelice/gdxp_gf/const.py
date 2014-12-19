from base.const import PHONE,EMAIL,FAX

CONTACT_CHOICES_MAP = [
    (PHONE , 'phoneNumber'),
    (EMAIL, 'emailAddress'),
    (FAX, 'faxNumber'),
]
RETURN_CODE = {
    'contacts' : 10,
    'extraFields' : 11,
}


EXTRA = 'extra'
SINGLE = 'single'
TREE = 'tree'
MULTIPLE = 'multiple'

