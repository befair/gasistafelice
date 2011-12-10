from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.views import login as django_auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from gasistafelice.des.forms import DESRegistrationForm

@never_cache
def login(request, *args, **kw):

    kw['extra_context'] = {
        'VERSION': settings.VERSION,
        'THEME' : settings.THEME,
        'MEDIA_URL' : settings.MEDIA_URL,
        'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX
    }
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
        'MEDIA_URL' : settings.MEDIA_URL,
        'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX
    }

    return render_to_response("registration/register.html", context,
                              context_instance=RequestContext(request)
    )
