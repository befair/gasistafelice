from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.conf import settings

from django.core.urlresolvers import reverse

import copy, time
from socket import gethostname

from gasistafelice.lib.shortcuts import render_to_response

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

DEFAULT_CONTEXTMENU_ENTRIES = [
    # This entry points to the resource page
    {
    	'id'   : 'page',
    	'icon' : 'info.png', 
    	'descr': _('Resource page'), 
    	'type' : 'url',
    	'data'  : '#rest/%(resource_type)s/%(resource_id)s/',
    },
]

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

def timestamp_to_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def get_default_menu_entries(resource, user=None):
    
    entries = copy.deepcopy(DEFAULT_CONTEXTMENU_ENTRIES)

    for entry in entries:
    	entry['data'] = entry['data'] % {
                                'resource_type': resource.resource_type, 
                                'resource_id'  : resource.pk
        }
    

    #
    # Mail  TO
    #
    
    to = resource.preferred_contact_email

    cc   = ''
    bcc  = ''
    subj = '[%s]' % (resource.site.name)
    body_lines = []

    #FUTURE TODO: mail template management
    body = 'body=%s' % ('%0A'.join(body_lines))
    
    #
    # Return entry
    #
    mailto_entry = {
        'id'   : 'mailto',
        'icon' : 'info.png', 
        'descr': 'Mail', 
        'type' : 'url',
        'data' : 'mailto:%s?cc=%s&bcc=%s&subject=%s&%s' % (to, cc, bcc, subj, body) ,
    }

    entries.append(mailto_entry)

    return entries
    
    
def __calculate_node_url(node):
    try:
    	vname = "state.views.node_by_path"
    	kwargs = { 'path': node.name }
    	url = reverse(vname, args=[], kwargs=kwargs)
    	return url			
    except Exception, e:
    	return ''
    		
#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

def get_external_menu_entries(resource, user=None):

    #FUTURE TODO: provide hooks for external scripts
    entries = []
    return entries

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

def get_context_menu(request):

    resource = request.resource
    user = request.user

    entries = []
    entries += get_default_menu_entries(resource, user)
    entries += get_external_menu_entries(resource, user)
    
    context = {
    	  'media_url': settings.MEDIA_URL
    	, 'resource': request.resource
    	, 'menu_entries': entries
    }

    pt = ['blocks/menu.xml']

    return render_to_response(pt, context)
    
