from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from gasistafelice.rest.models.pages import HomePage

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def index(request):

    try: 
        role = request.session["app_settings"]["active_role"]
    except KeyError:
        role = request.user.get_profile().default_role
        request.session["app_settings"]["active_role"] = role
        request.session.modified = True

    print "AAAA RUOLO ATTIVO: %s" % role
    url = HomePage.get_user_home(request.user, role)
    return HttpResponseRedirect(url)

