from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from gasistafelice.rest.models.pages import HomePage
from gasistafelice.users.models import UserProfile

from gasistafelice.gas.models.base import GASMember
#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def index(request):

    if request.user.is_superuser:
	return redirect("rest.views.index")

    role = request.user.get_profile().default_role
    request.session["app_settings"]["active_role"] = role
    request.session.modified = True

    url = HomePage.get_user_home(request.user, role)
    return HttpResponseRedirect(url)
  
#LF: no role selection anymore. 
#WAS:    try: 
#WAS:        role = request.session["app_settings"]["active_role"]
#WAS:    except KeyError:
  

@login_required
def newria_index(request):

    person = request.user.person
    #url = reverse('api-v1-person', args=(person.pk,))
    #url += "?format=json"
    #return HttpResponseRedirect(url)

    #gasmember = GASMember.objects.get(person=person.pk)
    url = "http://localhost/newUI/#/%s/" % person.pk
  
#LF: no role selection anymore. 
#WAS:    try: 
#WAS:        role = request.session["app_settings"]["active_role"]
#WAS:    except KeyError:
  
    return HttpResponseRedirect(url)

@login_required
def simulate_user(request, user_pk):

    #Check permissions
    #TODO: open also to non superuser account (i.e: TECH_REFERRERS for users in their GAS)
    if request.logged_user.is_superuser:
        request.session['user_to_simulate'] = user_pk
    else:
        user_pk = _("yourself")
    return HttpResponse(_("OK, now you are %s") % user_pk)
