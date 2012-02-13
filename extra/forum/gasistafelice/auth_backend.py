from django.contrib.auth.models import User, check_password

class GasistaFeliceBackend(object):
    """
    Authenticate against User database in Gasista Felice

    it uses database alias 'gasistafelice'
    """

    supports_inactive_user = False
    supports_anonymous_user = False
    supports_object_permissions = False

    def authenticate(self, username=None, password=None, **kw):

        try:
            #FERO: bisogna fare in questo modo perche' i campi del db non corrispondono
            #FERO: (askbot e' stato syncato su una versione piu' vecchia di Django?!?)
            gf_user_d = User.objects.using('gasistafelice').values('username','is_active','password','is_superuser').get(username=username)
        except User.DoesNotExist:
            gf_auth = None
        else:
            gf_auth = check_password(password, gf_user_d['password'])

        if gf_auth:

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password='capperoniemeloni')
                user.is_staff = False
                user.is_superuser = gf_user_d['is_superuser']
                user.is_active = gf_user_d['is_active']
                user.save()

            if user.is_active:
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

