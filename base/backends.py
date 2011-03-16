from django.contrib.auth.backends import ModelBackend

class MyAuthBackend(ModelBackend):

    supports_object_permissions = True
    supports_anonymous_user = True
    #supports_inactive_user = False

    def has_perm(self, user, perm, obj=None):

        if obj:
            rv = obj.permission_check(user, perm)
        else:
            rv = super(ModelBackend, self).has_perm(user, perm)

        return rv
