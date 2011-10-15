
from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm

class GASRoleForm(BaseRoleForm):

    def __init__(self, request, *args, **kw):
        super(GASRoleForm, self).__init__(request, *args, **kw)
        self._gas = request.resource.gas
        self.fields['person'].queryset = \
            self._gas.persons.filter(gasmember_set__isnull=False)

#--------------------------------------------------------------------------------

