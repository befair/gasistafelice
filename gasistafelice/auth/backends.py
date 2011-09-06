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
    
    
        
class ParamRoleBackend(object):
    """A Django authorization backend for (parametric) role-based permission checking.
    
    It supports per-model (table-level) and per-instance (row-level) permissions.

    Use it together with Django's default `ModelBackend` adding this declaration 
    within the settings module:

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'gasistafelice.auth.backends.ParamRoleBackend',
        )

    Then, to check if a Django User has a permission on a given object (model class or instance), 
    just invoke the `has_perm()` method on the User model:

        user.has_perm(perm, obj)
        
        where `perm` is a permission codename - as a string - and `obj` is the object 
        with respect to which the permission checking is done: if `obj` is a model class, 
        the permission is intended as a table-level one (i.e. it applies to every instance 
        of that model), while if `obj` is a model instance the permission is meant to be row-level 
        (valid only for that specific instance).  
        
        In order for the backend to work, in a given Django application each model class 
        (for which permission checking is enabled) should define a method for every 
        checkable permission (w.r.t. that model), adhering to the following specifications:
        * if the permission is model-level, it should be a class-method; 
          on the other hand, if the permission is instance-level, it should be an instance-method;
        * the method should be named as `can_<perm>`, where <perm> is the lower-cased permission codename;
        * the method must take as argument an User instance and allow for arbitrarily keyword arguments;
          so the method signature should be `(user, **kwargs)`.  Keyword arguments are needed 
          - for example - when a given user is granted the permission to create a new model instance 
          depending on additional parameters defining the actual context;  
        * the method should return `True` if the given user is granted the given permission on the object 
          w.r.t. which the permission is checked (model class or instance), `False` otherwise.
          
          A bare-bones example could be:
          
          class Foo(models.Model):
              # ... field declarations
              
              ## authorization API
              # table-level CREATE permission
              @classmethod
              def can_create(cls, user, **kwargs):
                  ...
              # row-level VIEW permission
              def can_view (self, user, **kwargs):
                  ...
              # row-level DELETE permission
              def can_delete (self, user, **kwargs):
                  ...
                   
    """
    
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        """
        This is an authorization-only backend; delegate authentication to others backends. 
        """
        return None
    
    
    def has_perm(self, user_obj, perm, obj=None, **kwargs):
        """Checks whether a user has a table-level/row-level permission on a model class/instance.

        This should be the primary method to check wether a User has a certain permission.

        Parameters
        ==========

        perm
            The codename of the permission which should be checked.

        user_obj
            The User for which the permission should be checked.

        obj
            The object (either a model class or instance) for which the permission should be checked.
            If `obj` is a model class, the permission is a table-level one; 
            If `obj` is a model instance, the permission is a row-level one.
        """
        
        # delegate non-object permission check to Django's default backend (`ModelBackend`) - or whatever
        if obj is None:
            return False
                    

        # Superuser can do evrything
        if user_obj.is_superuser:
            return True

        # if User is not authenticated or inactive, (s)he has no permissions 
        elif user_obj.is_anonymous() or not user_obj.is_active:
            return False

        # retrieve the function implementing the permission check for the given model
        # if `obj` is a model instance, that function should be a (bound) instance method;
        # if `obj` is a model class, it should be a (bound) class method.          
        perm_check = getattr(obj, 'can_' + perm.lower())
        return perm_check(user_obj, **kwargs)
