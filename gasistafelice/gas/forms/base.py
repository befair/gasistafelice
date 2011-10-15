
from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import GAS_MEMBER

class GASRoleForm(BaseRoleForm):

    def __init__(self, request, *args, **kw):
        super(GASRoleForm, self).__init__(request, *args, **kw)
        self._gas = request.resource.gas
        self.fields['person'].queryset = \
            self._gas.persons.filter(gasmember__isnull=False)
        self.fields['role'].queryset = self.fields['role'].queryset.exclude(role__name=GAS_MEMBER)

#--------------------------------------------------------------------------------

