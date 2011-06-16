from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

def index(request):
		
	vname = "rest.views.index"
	kwargs = {}
	url = reverse(vname, args=[], kwargs=kwargs)

	return HttpResponseRedirect(url)

