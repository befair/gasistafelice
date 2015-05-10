from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.views import login as django_auth_login
from django.contrib.contenttypes.models import ContentType
from django_comments.models import Comment
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from des.forms import DESRegistrationForm, DESStaffRegistrationForm
from des.models import Siteattr
from gf.gas.models import GASMember, GAS

from registration.models import RegistrationProfile
import re, logging

log = logging.getLogger("gasistafelice")

def cmp_orders(gas_a, gas_b):
    if gas_a.orders.archived().count() < gas_b.orders.archived().count():
        return 1
    else:
        return -1

@never_cache
def login(request, *args, **kw):

    gas_list = list(GAS.objects.all())
    gas_list.sort(cmp_orders)

    kw['extra_context'] = {
        'VERSION': settings.VERSION,
        'THEME' : settings.THEME,
        'MAINTENANCE_MODE' : settings.MAINTENANCE_MODE,
        'gas_list' : gas_list,
    }
    if settings.MAINTENANCE_MODE:
        if request.method == "POST" and \
            request.POST.get('username') != settings.INIT_OPTIONS['su_username']:
            return HttpResponse(_("Maintenance in progress, please retry later..."))

    return django_auth_login(request, *args, **kw)

@csrf_protect
@never_cache
def registration(request, *args, **kw):

    form_class = DESRegistrationForm
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Ti sei registrato con successo, \
                attendi l'abilitazione del GAS e poi potrai accedere al sistema"
            )
            return HttpResponseRedirect(settings.LOGIN_URL)
    else:
        form = form_class()

    context = {
        'registration_form' : form,
        'VERSION': settings.VERSION,
        'THEME' : settings.THEME,
    }

    return render_to_response("registration/register.html", context,
                              context_instance=RequestContext(request)
    )

@csrf_protect
@never_cache
def staff_registration(request, *args, **kw):
    """This view is used by staff that wants to register new users
    without using the email confirmation procedure.

    """
    des = Siteattr.get_site()

    if request.user in des.admins | des.gas_tech_referrers:

        form_class = DESStaffRegistrationForm
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Complimenti o tecnico! Hai registrato un nuovo utente :)")
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            form = form_class()

        context = {
            'registration_form' : form,
            'VERSION': settings.VERSION,
            'THEME' : settings.THEME,
        }

        return render_to_response("registration/staff_register.html", context,
                                  context_instance=RequestContext(request)
        )

    else:
        return django_auth_login(request, *args, **kw)

# Activate user function which update RegistrationProfile activation key,
# but doesn't activate the user

SHA1_RE = re.compile('^[a-f0-9]{40}$')

@transaction.atomic
def activate_user(activation_key):
    """Make the user ready to be activated by GAS referrer tech, OR
    already active if he is a GASMember, his GAS specified a registration token,
    he has specified the registration token in the registration form
    """

    model = RegistrationProfile

    if SHA1_RE.search(activation_key):
        try:
            profile = model.objects.get(activation_key=activation_key)
        except model.DoesNotExist:
            return False
        if not profile.activation_key_expired():
            profile.activation_key = model.ACTIVATED
            profile.save()

            # Activate user if:
            # * he is a GASMember
            # * his GAS has defined a registration_token
            # * he has specified the registration token in the registration form
            # (find it in a special note to be deleted)
            try:
                # At this time the user belongs at most to one GAS
                # IMPORTANT: you must use the GASMember.all_objects manager
                # because GASMember user is not active now
                gm = GASMember.all_objects.get(person=profile.user.person)
            except ObjectDoesNotExist as e:
                # Do not worry if user is not a GASMember
                pass
            else:
                if check_registration_token_for_gasmember(gm):
                    profile.user.is_active = True
                    profile.user.save()
            return profile.user
    return False

def check_registration_token_for_gasmember(gm):
    """Check if registration token matches (case insensitive match)"""

    rv = False

    # Check if GAS has specified a registration_token
    gas_config_token = gm.gas.config.registration_token
    if gas_config_token:
        try:
            # Get token_comment
            ctype = ContentType.objects.get_for_model(gm.__class__)
            token_comment = Comment.objects.get(content_type=ctype, object_pk=gm.pk)
        except ObjectDoesNotExist as e:
            # Do not worry if there is no note that begin with "registration-token:"
            pass
        except MultipleObjectsReturned as e:
            log.warning("Multiple notes with registration-token: on GASMember %s. Suspected attack" % gm)
            pass
        else:

            if token_comment.comment.startswith('registration-token:'):
                token = token_comment.comment[len('registration-token:'):]

                # Compare token case insensitive
                if token.lower() == gas_config_token.lower():
                    rv = True

                # Finally delete the comment
                token_comment.delete()
    return rv

# Function copied from registration.views app
# Use custom function to update activation key for a user
# but does not activate it

def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):

    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = activate_user(activation_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
        { 'account': account,
          'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
        context_instance=context
    )
