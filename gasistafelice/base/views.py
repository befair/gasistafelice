from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from gasistafelice.rest.models.pages import HomePage
#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def index(request):

    role = request.user.get_profile().default_role
    url = HomePage.get_user_home(request.user, role)
    return HttpResponseRedirect(url)

