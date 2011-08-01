from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db.models import signals
from django.contrib.auth.models import User, Group 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from permissions.models import Role

from gasistafelice.base.models import Resource
from gasistafelice.auth.managers import RolesManager

#from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
#from gasistafelice.supplier.models import Supplier

class PermissionBase(object):
    """
    Just a mix-in class for permission management.
    
    Permission-checking methods defined here all return `True`,
    so if a permission-enabled model class (one inheriting from
    `PermissionBase`) doesn't override some of them, every User 
    is automatically granted the corresponding permissions.
    """
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, **kwargs):
        return True

    # Row-level LIST permission
    def can_list(self, user, **kwargs):
        return True
    
    # Row-level VIEW permission
    def can_view(self, user, **kwargs):
        return True
    
    # Row-level EDIT permission
    def can_edit(self, user, **kwargs):
        return True
    
    # Row-level DELETE permission
    def can_delete(self, user, **kwargs):
        return True
    
    
class ParamByName(object):
    """Helper class used to setup a convenient access API for `ParamRole`'s parameters"""

    def _get_param(self, param_role, name):
        """
        If this role has a "%s" parameter, return it; else return None
        """
        # Retrieve the value of parameter named `name`; if it's not set, return None
        # Duck typing
        try: 
            rv = param_role.param_set.get(name=name).param
        except Param.DoesNotExist:
            rv = None

        return rv

#    def set_param(self, param_role, name, value):
#
#        param_names = map(lambda x : x[0], Param.PARAM_CHOICES)
#
#        #Sanity check
#        if name in param_names:
#            # TODO: check also content type
#            param_role.param_set.add(Param(name=name, param=value))
#        else:
#            raise NameError(ugettext("Wrong param name %s. Allowed param names are %s") % (value, param_names))

    def contribute_to_class(self, cls, name):
        """Create a property to retrieve role parameters by name"""

        p = property(
            lambda obj : self._get_param(obj, name), 
            None,
            None, 
            self._get_param.__doc__ % name
        )

        setattr(cls, name, p)

class Param(models.Model):
    """
    A trivial wrapper model class around a generic ForeignKey; 
    used to create (parametric) Roles with more than one parameter.  
    """
    #Choice are limited. May this be correct?
    # TODO: parameter choices should be a project-level setting
    PARAM_CHOICES = (
        ('gas', _('GAS')),
        ('supplier', _('Supplier')),
        ('order', _('Order')),
        ('delivery', _('Delivery')),
        ('withdrawal', _('Withdrawal')),
    )
    name = models.CharField(max_length=20, choices=PARAM_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    # TODO: refactoring: `value` should be a better name than `param`
    param = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")

    def __unicode__(self):
        return u"%s: %s" % (self.name, self.value)

    def __repr__(self):
        return "<%s %s: %s>" % (self.__class__.__name__, self.name, self.value)

    @property
    def value(self):
        #TODO placeholder seldon REFACTORY: change name of param attribute in value
        return self.param
    
    class Meta:
        # forbid duplicated `Param` entries in the DB
        unique_together = ('name', 'content_type', 'object_id')

class ParamRole(models.Model, Resource):
    """
    A custom role model class inspired by `django-permissions`'s `Role` model.
    
    The goal is to augment the base `Role` model (carrying only a `name` field attribute) 
    with additional information needed to describe those 'parametric' roles arising 
    in this application domain.
    
     A parametric role (`ParamRole`) can be tied to:
     
     1) a given GAS (e.g. GAS_REFERRER, GAS_MEMBER, GAS_REFERRER_CASH, GAS_REFERRER_TECH),
     2) a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER),
     3) a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
     4) a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
     5) a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
     6) a given "Retina" (TODO)
    
    """
    # link to the base model class (`Role`)
    role = models.ForeignKey(Role)
    # parameters for this Role
    param_set = models.ManyToManyField(Param)
    
    ## we define a few attributes providing easier access to allowed role parameters            
    # note that access is read-only; parameter assignment is managed by the 
    #`register_parametric_role()` factory function

    # Use `contribute_to_class` Django trickery
    # TODO: hard-coding allowed parameter's names in the model compromise reusability
    # they should be dynamically added based on project-level settings
    gas = ParamByName()
    supplier = ParamByName()
    order = ParamByName()
    delivery = ParamByName()
    withdrawal = ParamByName()

    objects = RolesManager()

    def __unicode__(self):
        param_str_list = ["%s" % s for s in self.param_set.all()]
        return u"%s on %s" % (self.role.name, ", ".join(param_str_list))

    @classmethod
    def get_role(cls, role_name, **params):
        qs = cls.objects.get_param_roles(role_name, **params)
        # TODO UNITTEST: write unit tests for this method
        if len(qs) > 1:
            raise MultipleObjectsReturned() 
        return qs[0]

    def add_principal(self, principal):
        """
        Add the given principal (User or Group) to this parametric role.
        
        Raise `TypeError` if the principal is neither a User nor a Group instance.
        """
        if isinstance(principal, User):
            PrincipalParamRoleRelation.objects.create(user=principal, role=self)
        elif isinstance(principal, Group):
            PrincipalParamRoleRelation.objects.create(group=principal, role=self)
        else:
            raise TypeError("The principal must be either a User instance or a Group instance.")   

            
    def get_groups(self):
        """Returns all Groups to which this parametric role is assigned."""    
        prrs = PrincipalParamRoleRelation.objects.filter(role=self).exclude(group=None)
        return [prr.group for prr in prrs]

    def get_users(self, content=None):
        """
        Returns all Users to which this parametric role was assigned. 
        """
        prrs = PrincipalParamRoleRelation.objects.filter(role=self).exclude(user=None)
        return [prr.user for prr in prrs]

    
class PrincipalParamRoleRelation(models.Model):
    """
    This model is a relation describing the fact that a parametric role (`ParamRole`) 
    is assigned to a principal (i.e. a User or Group). 

    user
        The User to which the parametric role should be assigned. 
        Either a User instance xor a Group instance needs to be given.

    group
        The Group to which the parametric role should be assigned. 
        Either a User instance xor a Group instance needs to be given.

    role
        The role (a `ParamRole` instance) to be assigned to the principal.
        
    CREDITS: this class is inspired by the `PrincipalRoleRelation` model in `django-permissions`.
    """
    user = models.ForeignKey(User, blank=True, null=True, related_name="principal_param_role_set")
    group = models.ForeignKey(Group, blank=True, null=True, related_name="principal_param_role_set")
    role = models.ForeignKey(ParamRole, related_name="principal_param_role_set")

    def get_principal(self):
        """Returns the principal."""
        return self.user or self.group

    def set_principal(self, principal):
        """Sets the principal."""
        if isinstance(principal, User):
            self.user = principal
        elif isinstance(principal, Group):
            self.group = principal
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")

    principal = property(get_principal, set_principal)    
    
def setup_roles(sender, instance, created, **kwargs):
    """
    Setup proper Roles after a model instance is saved to the DB for the first time.
    This function just calls the `setup_roles()` instance method of the sender model class (if defined);
    actual role-creation/setup logic is encapsulated there.
    """
    if created: # Automatic role-setup should happen only at instance-creation time 
        try:
            # `instance` is the model instance that has just been created
            instance.setup_roles()
                                                
        except AttributeError:
            # sender model doesn't specify any role-related setup operations, so just ignore the signal
            pass

# add `setup_roles` function as a listener to the `post_save` signal
signals.post_save.connect(setup_roles)
     