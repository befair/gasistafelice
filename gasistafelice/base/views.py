from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from gasistafelice.rest.models.pages import HomePage
from gasistafelice.users.models import UserProfile

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def index(request):

    if request.user.is_superuser:
        return redirect("rest.views.index")

    try: 
        role = request.session["app_settings"]["active_role"]
    except KeyError:
        role = request.user.get_profile().default_role
        request.session["app_settings"]["active_role"] = role
        request.session.modified = True

    url = HomePage.get_user_home(request.user, role)
    return HttpResponseRedirect(url)

