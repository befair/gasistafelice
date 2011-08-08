from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from gasistafelice.rest.models.pages import HomePage
#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def index(request):

    role = None
    url = HomePage.get_user_url(request.user, role)
    return HttpResponseRedirect(url)
