from django.contrib.contenttypes.models import ContentType

from flexi_auth.models import ParamRole, Param

from gasistafelice.lib.formsets import BaseFormSetWithRequest
from gasistafelice.base.forms import BaseRoleForm
from gasistafelice.consts import GAS_MEMBER
from gasistafelice.gas.models import GASSupplierSolidalPact

import logging
log = logging.getLogger(__name__)

class GASRoleForm(BaseRoleForm):

    def __init__(self, request, *args, **kw):
        super(GASRoleForm, self).__init__(request, *args, **kw)
        self._gas = request.resource.gas
        self.fields['person'].queryset = \
            self._gas.persons.filter(gasmember__isnull=False)
        self.fields['role'].queryset = self.fields['role'].queryset.exclude(role__name=GAS_MEMBER)
        self.fields['role'].queryset |= self._get_additional_roles()

    def _get_additional_roles(self):
        """
        Return a QuerySet containing all parametric roles manageable by the GAS
        (i.e: by GAS_REFERRER_TECH)
        """

        # Roles MUST BE a property because roles are bound to a User 
        # with `add_principal()` and not directly to a GAS member
        # costruct the result set by joining partial QuerySets

        ctype = ContentType.objects.get_for_model(GASSupplierSolidalPact)
        params = Param.objects.filter(content_type=ctype, object_id__in=map(lambda x: x['pk'], self._gas.pacts.values('pk')))
        qs = ParamRole.objects.filter(param_set__in=params)
        log.debug("PACT selectable roles %s" % qs.values())
        return qs

#--------------------------------------------------------------------------------

