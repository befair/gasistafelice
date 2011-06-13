from django.utils.translation import ugettext as _

class RoleNotAllowed(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return _("Role %s is not allowed in current application domain") % self.value

class RoleParameterNotAllowed(Exception):

    def __init__(self, role_name, allowed_params, wrong_param):
        self.role_name = role_name
        self.allowed_params = allowed_params
        self.wrong_param = wrong_param

    def __str__(self):
        return _("Wrong param '%(wp)s' provided for role %(r)s. Only %(pl)s are relatable to this role") % \
                  { 'wp' : self.wrong_param, 'r' : self.role_name, 'pl' : ", ".join(self.allowed_params) }


class RoleParameterWrongSpecsProvided(Exception):
    def __init__(self, role_name, param_specs):

        self.role_name = role_name
        self.param_specs = param_specs

    def __str__(self):
        return _("Wrong specs %(s)s for role %(r)s") % \
                    { 's' : self.param_specs, 'r' : self.role_name }
