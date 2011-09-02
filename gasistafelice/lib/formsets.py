
from django.forms.formsets import BaseFormSet
from django.utils.functional import curry

class BaseFormSetWithRequest(BaseFormSet):

    def __init__(self, request, *args, **kw):
        # This trick is needed to pass request in form constructor. Superb python!
        self.form = curry(self.form, request)
        super(BaseFormSetWithRequest, self).__init__(*args, **kw)


