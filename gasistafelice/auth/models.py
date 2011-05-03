from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User, Group 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from permissions.models import Permission, Role

from gasistafelice.base.models import Resource
#from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal 
#from gasistafelice.supplier.models import Supplier

class ParamByName(object):
    """Helper class used to set param role properties by name """

    def get_param(self, param_role, name):
        """
        If this role has a "%s" parameter, return it; else return None
        """
        # Retrieve param which has name 'name'. If it does not exist return None
        # Duck typing
        try: 
            rv = param_role.param_set.get(name=name)
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
        """Create a property to retrieve param by name"""

        p = property(
            lambda obj : self.get_param(obj, name), 
            None,
            None, 
            self.get_param.__doc__ % name
        )

        setattr(cls, name, p)

class Param(models.Model):
    """
    A trivial wrapper model class around a generic ForeignKey; 
    used to create (parametric) Roles with more than one parameter.  
    """
    #Choice are limited. May this be correct?
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
    param = generic.GenericForeignKey(ct_field="content_type", fk_field="obj_id")

class ParamRole(Resource, Role):
#class ParamRole(Role):
    """
    A custom role model class inheriting from `django-permissions`'s`Role` model.
    This way, we are able to augment the base `Role` model
    (carrying only a `name` field attribute) with additional information
    needed to describe those 'parametric' roles arising in this application domain.
    
     A parametric role (`ParamRole`) can be tied to:
     
     1) a given GAS (e.g. GAS_REFERRER, GAS_MEMBER, GAS_REFERRER_CASH, GAS_REFERRER_TECH),
     2) a given Supplier (e.g. SUPPLIER_REFERRER, GAS_REFERRER_SUPPLIER),
     3) a given Delivery appointment (e.g. GAS_REFERRER_DELIVERY)
     4) a given Withdrawal appointment (e.g. GAS_REFERRER_WITHDRAWAL)
     5) a given GASSupplierOrder (e.g. GAS_REFERRER_ORDER)
     6) a given "Retina" (TODO)
    
    """
    # link to the base model class (`BaseRole`)
    role = models.OneToOneField(Role, parent_link=True)
    # parameters for this Role
    param_set = models.ManyToManyField(Param)
    
    def add_principal(self, principal, content=None):
        """
        Add the given principal (User or Group) to this parametric role.
        
        Raise `AttributeError` if the principal is neither a User nor a Group instance.
        """
        if isinstance(principal, User):
            PrincipalParamRoleRelation.objects.create(user=principal, role=self)
        elif isinstance(principal, Group):
            PrincipalParamRoleRelation.objects.create(group=principal, role=self)
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")   

            
    def get_groups(self, content=None):
        """
        Returns all Groups to which this parametric role is assigned. 
        
        If a content object is given, parametric roles local to this object are returned, too.
        """
        if content:
            ctype = ContentType.objects.get_for_model(content)
            prrs = PrincipalParamRoleRelation.objects.filter(role=self,
                content_id__in = (None, content.id),
                content_type__in = (None, ctype)).exclude(group=None)
        else:
            prrs = PrincipalParamRoleRelation.objects.filter(role=self,
            content_id=None, content_type=None).exclude(group=None)

        return [prr.group for prr in prrs]

    def get_users(self, content=None):
        """
        Returns all Users to which this parametric role was assigned. 
        
        If a content object is given, parametric roles local to this object are returned, too.
        """
        if content:
            ctype = ContentType.objects.get_for_model(content)
            prrs = PrincipalParamRoleRelation.objects.filter(role=self,
                content_id__in = (None, content.id),
                content_type__in = (None, ctype)).exclude(user=None)
        else:
            prrs = PrincipalParamRoleRelation.objects.filter(role=self,
                content_id=None, content_type=None).exclude(user=None)

        return [prr.user for prr in prrs]

    
    ## we define a few properties providing easier access to allowed role parameters            
    # note that access is read-only; parameter assignment is managed by the 
    #`register_parametric_role()` factory function

    # Use contribute_to_class django trickery
    gas = ParamByName()
    supplier = ParamByName()
    order = ParamByName()
    delivery = ParamByName()
    withdrawal = ParamByName()

class PrincipalParamRoleRelation(models.Model):
    """This model is a relation describing the fact that a parametric role (`ParamRole`) 
    is assigned to a principal (i.e. a User or Group). If a content object is
    given this is a local role, i.e. the principal has this role only for this
    content object. Otherwise it is a global role, i.e. the principal has
    this role for all content objects.

    user
        The User to which the parametric role should be assigned. 
        Either a User instance xor a Group instance needs to be given.

    group
        The Group to which the parametric role should be assigned. 
        Either a User instance xor a Group instance needs to be given.

    role
        The role (a `ParamRole` instance) to be assigned to the principal.

    content [optional]
        If given, the role assigned to the principal is local to that content object.
        
    CREDITS: this class is inspired by the `PrincipalRoleRelation` model in `django-permissions`.
    """
    user = models.ForeignKey(User, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    role = models.ForeignKey(ParamRole)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    content_id = models.PositiveIntegerField(blank=True, null=True)
    content = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    def get_principal(self):
        """Returns the principal.
        """
        return self.user or self.group

    def set_principal(self, principal):
        """Sets the principal.
        """
        if isinstance(principal, User):
            self.user = principal
        elif isinstance(principal, Group):
            self.group = principal
        else:
            raise AttributeError("The principal must be either a User instance or a Group instance.")

    principal = property(get_principal, set_principal)
        
     
class GlobalPermission(models.Model):
    permission = models.ForeignKey(Permission)
    role = models.ForeignKey(Role)
    content_type = models.ForeignKey(ContentType)
    class Meta:
        # forbid duplicated GlobalPermission entries in the DB
        unique_together = ("permission", "role", "content_type")
        

