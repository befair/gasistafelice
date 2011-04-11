from django.db.models import Model
from django.contrib.contenttypes.models import ContentType

import permissions.utils
from permissions.models import ObjectPermission

from gasistafelice.auth.models import GlobalPermission

class DummyBackend(object):
    """A dummy authorization backend intended only for development purposes.
    
    Using this backend, permission checks always succeed ! ;-)
          
    """
    
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        return None
    
    def has_perm(self, user_obj, perm, obj=None):
        return True
    
    
        
class ObjectPermissionsBackend(object):
    """An authorization backend for Django for role-based permission checking.
    
    Support global (per-model) and local (per-instance) Permissions.

    Use it together with the default ModelBackend like this:

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'gasistafelice.base.backends.ObjectPermissionsBackend',
        )

    Then you can use it like:

        user.has_perm("view", your_object)
        
        where `your_object` can be a ContentType instance (if you want to check global permissions) 
        or a model instance (if you want to check local permissions).
    """
    
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        return None
    
    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns the set of Permissions (locals and globals) this User has been granted
        through his/her Groups (via the Roles assigned to them).
        
        If the `obj` argument is a model (actually, a ContentType instance), all (global) Permissions for that model are returned. 
        If the `obj` argument is a model instance all (local) Permissions for that instance are returned.           
        """
        
        # iterate on each Group the User belongs to
        roles = []
        groups = user_obj.groups.all()         
        for group in groups:
            roles.extend(permissions.utils.get_roles(group))
        if isinstance(obj, ContentType): # `obj` is a model class, so check for global Permissions for this model        
            perms = GlobalPermission.objects.filter(content_type=obj, role__in=roles)
        elif isinstance(obj, Model) : # `obj` is a model instance, so check for local Permissions for this instance
            ct = ContentType.objects.get_for_model(obj)
            perms = ObjectPermission.objects.filter(content_type=ct, content_id=obj.id, role__in=roles)            
        else: # `obj` is neither a model class nor a model instance (e.g. obj == None), so listing Permissions is meaningless 
            raise TypeError, "Can't get permissions for the provided object."
        return perms
        
            
    
    def get_all_permissions(self, user_obj, obj=None):
        
        """
        Returns the set of all Permissions (locals or globals) this User has been granted 
        (directly, via Roles assigned to him/her, or indirectly via those assigned to the Groups he/she belongs to).
        
        If the `obj` argument is a model (actually, a ContentType instance), all (global) Permissions for that model are returned.        
        If the `obj` argument is a model instance all (local) Permissions for that instance are returned.
        
        """
        # retrieve all the Roles assigned to the User (directly or indirectly)
        roles = permissions.utils.get_roles(user_obj)
        if isinstance(obj, ContentType): # `obj` is a model class, so check for global Permissions for this model        
            perms = GlobalPermission.objects.filter(content_type=obj, role__in=roles)
        elif isinstance(obj, Model) : # `obj` is a model instance, so check for local Permissions for this instance
            ct = ContentType.objects.get_for_model(obj)
            perms = ObjectPermission.objects.filter(content_type=ct, content_id=obj.id, role__in=roles)            
        else: # `obj` is neither a model class nor a model instance (e.g. obj == None), so listing Permissions is meaningless 
            raise TypeError, "Can't get permissions for the provided object."
        return perms

    def has_perm(self, user_obj, perm, obj=None):
        """Checks whether a User has a global (local) Permission on a model (model instance).

        This should be the primary method to check wether a User has a certain Permission.

        Parameters
        ==========

        perm
            The codename of the Permission which should be checked.

        user_obj
            The User for which the Permission should be checked.

        obj
            The Object (either a model or model instance) for which the Permission should be checked.
        """
        
        # if User is not authenticated or inactive, he has no Permissions 
        if user_obj.is_anonymous() or not user_obj.is_active():
            return False        
        if isinstance(obj, ContentType): # `obj` is a model class, so check for global Permissions for this model
            return perm in self.get_all_permissions(user_obj, obj)        
        elif isinstance(obj, Model) : # `obj` is a model instance, so check for local Permissions for this instance
            return permissions.utils.has_permission(obj, user_obj, perm)
        else: # `obj` is neither a model class nor a model instance (e.g. obj == None), so Permissions check is meaningless 
            raise TypeError, "Can't check permissions for the provided object."