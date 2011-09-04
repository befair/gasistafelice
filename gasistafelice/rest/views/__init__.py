from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.conf import settings
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from gasistafelice.lib.shortcuts import render_to_xml_response

from gasistafelice.rest.utils import load_block_handler, load_symbols_from_dir

from gasistafelice.gas.models.proxy import Siteattr

from gasistafelice.comments.views import get_all_notes, get_notes_for
from gasistafelice.auth import ROLES_DICT
from gasistafelice.auth.models import ParamRole

import time, datetime

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

@login_required
def index(request):
    """ main entrance page """
    ctx = {
        'VERSION': settings.VERSION,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'LOGOUT_URL' : settings.LOGOUT_URL,
        'THEME' : settings.THEME,
    }
    return render_to_response("html/index.html", ctx)
    
#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

@login_required
def site_settings(request):
    """ main entrance page (following index ;))"""

    site = Siteattr.get_site()
    
    user = request.user
    base_usercontainer_id = None
    
#    if not user.is_anonymous():
#        base_usercontainer_id = UserContainer.objects.filter(creator=user, parent=None)    [0].id
    
    ctx = {
        'user'                 : request.user.username,
        'base_usercontainer_id': base_usercontainer_id,
        'url_prefix'           : settings.URL_PREFIX,
        'type'                 : 'site',
        'id'                   : site.pk,
        'site_id'              : site.pk,
        'site_name'            : unicode(site),
        'isdebug'              : settings.DEBUG,
    }
    return render_to_xml_response("settings.xml", ctx)

#---------------------------------------------------------------------#
# Roles management                                                    #
#---------------------------------------------------------------------#

@login_required
def user_roles(request):
    
    if request.user.is_superuser:
        rv = [{ 'role_name' : _("Master of the Universe"), 'role_resources' : [] }]
        return HttpResponse(simplejson.dumps(rv))

    rv = []
    for prr in request.user.principal_param_role_set.all():
        rv.append( {
            'role_name': ROLES_DICT[prr.role.role.name],
            'role_pk': prr.role.pk,
            'role_resources': [ r.value.as_dict() for r in prr.role.params ],
        })

    return HttpResponse(simplejson.dumps(rv))

@login_required
def switch_role(request):

    if request.method == 'POST':
        
        role = get_object_or_404(ParamRole, pk=int(request.POST["active_role"]))
        request.session["app_settings"]["active_role"] = role
        request.session.modified = True
        return redirect("base.views.index")
    else:
        raise ValueError("Only POST is allowed for this view")

#---------------------------------------------------------------------#
# Timestamps                                                          #
#---------------------------------------------------------------------#

def hh_mm(request):
    """Get current time hh:mm"""
    return HttpResponse(time.strftime("%H:%M"))

def now(request):
    """Get current datetime in format: dow dom mon year - hh:mm"""
    dt = datetime.datetime.now()

    return HttpResponse(dt.strftime("%c")[:-7])
    #return HttpResponse(dt.strftime("%A, %d %B %Y - %H:%M"))

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

@login_required
#@authorized_on_resource TODO placeholder seldon replace with has_perm
def view_factory(request, resource_type, resource_id, view_type, args=""):
    
    response = ""
    
    handler = load_block_handler(view_type)
    
    if (args != "options"):
        response = handler.get_response(request, resource_type, resource_id, args)
    else: 
        if (request.method == "GET"):
            response = handler.options_response(request, resource_type, resource_id)
        else:
            response = handler.options_response(request, resource_type, resource_id)

    return response


#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

@login_required
def resource_page(request, resource_type, resource_id):
        
    resource = request.resource
    
    parent = resource.ancestors
    page_config = get_resource_page_content_config(resource.resource_type)

    return create_page_settings_from_config(page_config, resource, parent)


#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def create_page_settings_from_config(page_config, resource, parent=None):

    for section in page_config:

        blocks = []
        for block_type in section['blocks']:
            a = create_block_signature(block_type, resource.resource_type, resource.pk)
            blocks.append(a)
            
        section['blocks_signature'] = blocks
    
    pt = ['page_config.xml']

    ctx = {
        
        'resource': resource,
        'parents': parent,
        'sections': page_config,
    }
    
    return render_to_xml_response(pt, ctx)


def get_resource_page_content_config(resource_type):
    
    page_config = settings.RESOURCE_PAGE_BLOCKS[resource_type]
    return page_config
    
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def create_block_signature(view_type, resource_type, resource_id):
    
    handler = load_block_handler(view_type)
    response = handler.create_block_signature(resource_type, resource_id)
    
    return response
    
#def create_block_signature_from_resource(view_type, resource, args):
def create_block_signature_from_resource(view_type, resource):
    
    handler = load_block_handler(view_type)
    
    response = handler.create_block_signature_from_resource(resource)
    
    return response    
    
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#
    
def related_notes(request, resource_type, resource_id):
    
    target = request.resource
    
    node = target.iface.node if target.iface != None else target.node
    
    context = {
        'target_notes': target.notes,
        'node_notes': node.notes
    }
    return render_to_response('related_notes.html', context)    

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#


def list(request, resource_type):
    
    user = request.user
    ids = []
    context = {
        'resource_type':resource_type,
        'ids':ids
    }
    return render_to_xml_response("resource_list.xml", context)
    
#    if resource_type == 'usercontainer':
#        
#        from users.models import UserContainer
#        
#        containers = UserContainer.objects.filter(creator=user).all()
#        #containers = UserContainer.objects.all()
#        #for uc in containers: print uc.id, uc.creator
#        
#        ids = [ {"id": uc.id, "name": str(uc) } for uc in containers ]
#    else:    
#        from state.models import type_model_d
#    
#        #resource_type_class = type_model_d[resource_type]
#        #results = resource_type_class.objects.all()
#        
#        
#        site = Siteattr.get_site()
#                if not user.is_superuser:
#                        site = site.filter(user)
#        
#        print resource_type
#        if   resource_type == 'site'      : results = [site]
#        elif resource_type == 'container' : results = site.containers.all()
#        elif resource_type == 'node'      : results = site.nodes.all()
#        elif resource_type == 'iface'     : results = site.ifaces.all()
#        elif resource_type == 'target'    : results = site.targets.all()
#        elif resource_type == 'measure'   : results = site.measure.all()
#
#        print results
#
#        column = {
#            'site'         :'name',
#            'iface'        :'name',
#            'target'       :'expanded_title',
#            'measure'      :'path',
#            'node'         :'name',
#            'container'    :'name',
#            'usercontainer':'name',
#        }
#                
#        ids = []
#        for obj in results:
#            name = getattr(obj, column[resource_type])
#            #print column[resource_type], name
#            ids.append({'id':obj.id, "name": unicode(obj) })
                   

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def parts(request, resource_type, resource_id):
    urls = []
    for m in load_symbols_from_dir("/rest/views/blocks/", "rest.views.blocks", "Block"):
        try:
            
            module = m[0]
            itm    = m[1]()
            
            if (itm.is_valid(resource_type)):
                if (itm.visible_in_page()):
                    urls.append({
                            "address": module,
                            "description":itm.get_description()
                            })
        except Exception, e:
            print(e)
            continue

    return render_to_xml_response("resource_urls.xml", {"resource_id":resource_id, "resource_type":resource_type, "urls":urls})
#

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def quick_search(request):

    site = Siteattr.get_site()
    #TODO: fero TOCHECK, no filter needed for "VIEW" permission
    #if not request.user.is_superuser:
    #   site = site.filter(request.user)
    q = request.GET['q']
    limits = request.REQUEST.getlist('l')
    if len(limits) == 0:
        search_result = site.quick_search(q = q)
    else:
        search_result = site.quick_search(q = q, limits = limits)
    context = {
        'search_result': search_result 
    }
    return render_to_response("html/quick_search_result.html", context)
    
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

@login_required()
def list_comments(request):
    #
    # FIX: GESTIRE LA VISIBILITA' DELLE NOTE DEGLI ALTRI UTENTI
    #
    user = request.user
    res = Siteattr.get_site()
    
    if not user.is_superuser:
        res = res.filter(user)

    rnotes = []
    if not request.user.is_superuser:
        #TODO fero: check if required
        rnotes.extend(get_notes_for([res]))
        rnotes.extend(get_notes_for(res.containers))
        rnotes.extend(get_notes_for(res.nodes))
        rnotes.extend(get_notes_for(res.ifaces))
        rnotes.extend(get_notes_for(res.targets))
        rnotes.extend(get_notes_for(res.measures))
    else:
        rnotes = get_all_notes()

    context = {
        'notes': rnotes
    }
    return render_to_xml_response("comments_result.xml", context)




#import sys
#import traceback
#import pprint
#import types 
#import pwd
#import os.path
#
#import settings
#
#from django.core.servers.basehttp import FileWrapper
#from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
#from django.template import Context, loader, RequestContext
#
#from django.contrib.comments.models import Comment
#from django.contrib.auth.models import User
#
#from state.models import Site, Container, Node, Iface, Target, Measure, TargetStateLog
#
#from state.models.manager import VisibleMeasureManager
#from state.models.manager import VisibleTargetManager
#Target.add_to_class('objects', VisibleTargetManager())
#Target.add_to_class('_default_manager', VisibleTargetManager())
#Measure.add_to_class('objects', VisibleMeasureManager())
#Measure.add_to_class('_default_manager', VisibleMeasureManager())
#
#from djlabs.shortcuts import render_to_response
#from lib import load_symbol
#
#from users.decorators import sanet_login_required
#from users.decorators import authorized_on_resource
#
#from users.models import UserContainer
#
#from rest.utils import *
##---------------------------------------------------------------------#
##                                                                     #
##---------------------------------------------------------------------#
#
#@login_required()
#def maps_menus(request):
#    
#    FAKE_RESOURCE_ID = '000'
#    
#    from contextmenu import get_default_menu_entries, get_external_menu_entries
#    
#    resource_types = [
#        'container',
#        'node',
#        'iface',
#        #'target',
#        #'measure',
#    ]
#    
#    menus = []
#    
#    for rtype in resource_types:
#        m_entries = []
#        
#        m_entries += [ {
#            'id'   : 'quickinfo',
#            'icon' : 'info.png', 
#            'descr': 'Quick info', 
#            'type' : 'script',
#            'data' : [ 'showQuickInfo', rtype+'/'+FAKE_RESOURCE_ID ], 
#        } ]
#        
#        m_entries += get_default_menu_entries(rtype, FAKE_RESOURCE_ID)
#        m_entries += get_external_menu_entries(rtype, FAKE_RESOURCE_ID)
#
#        menus.append({
#            'rtype': rtype,
#            'entries' : m_entries
#        })
#    
#        
#    context = {
#          'media_url'   : settings.MEDIA_URL
#        , 'menus': menus
#    }
#    
#    #pt = ['maps_menus.xml']
#    #return render_to_response(pt, context)        
#
#    from django.utils import simplejson
#    retdata = simplejson.dumps(context)
#    return HttpResponse(retdata);
#    
#    
#
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#def advanced_search_page(request):
#
#    resource = Siteattr.get_site()
#    resource_type = 'site'
#    resource_id   = '1'
#
#    request.resource = resource
#
#    parent = []
#        try:
#                if resource.node:
#                        parent.append(resource.node)
#                if resource.iface:
#                        parent.append(resource.iface.node)
#                        parent.append(resource.iface)
#        except:
#                pass
#        
#        
#    page_config = get_resource_page_content_config('advanced-search-page')
#    
#    return create_page_settings_from_config(page_config, resource, resource_type, resource_id)
#
#
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#def list_nodes(request):
#
#    result = Node.objects.all()
#    
#
#    context = {
#        'nodes'        : result
#    }
#    
#    t = loader.get_template( "nodes_list.xml" )
#    text = t.render(Context(context))
#    response = HttpResponse(text, content_type='text/xml')
#    return response
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#
#def target_changes(request, resource_type, resource_id):
#    import time
#    import datetime
#    target = request.resource
#    
#    end = int(time.time())
#    start = end - (24 * 60 * 60 * 7)
#    
#    states_sequence = extract_target_changes( target, start, end)
#    
#    events = []
#    for e in states_sequence:
#        e2 = ( 
#             datetime.datetime.fromtimestamp(e[0]).ctime()
#            ,datetime.datetime.fromtimestamp(e[1]).ctime()
#            ,convert_time(e[2])
#            ,e[3] 
#        ) 
#        events.append(e2)
#    
#    context = {
#        'target': target,
#        'events': events
#    }
#    return render_to_response("target_changes.json", context)
#    
#    
#
#def convert_time(duration):
#
#    DAY    = 24 * 60 * 60
#    HOUR   = 60 * 60
#    MINUTE = 60
#
#    text = ''
#    days = duration / DAY
#    if days: text += '%sd' % (days)
#    duration = duration % DAY
#    
#    hours = duration / HOUR
#    if hours: text += ' %sh' % (hours)
#    duration = duration % HOUR
#    
#    minutes = duration / MINUTE
#    if minutes: text += ' %sm' % (minutes)
#    duration = duration % MINUTE
#    
#    if duration: text += ' %ss' % (duration)
#    
#    return text
#    
#def extract_target_changes(target, start, end):
#    
#    return target.logchanges_sequence(start, end)
#
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#def last_status_change(request):
#
#
#    resource = Siteattr.get_site()
#    user = request.user
#    
#    if isinstance(resource, Site) and not user.is_superuser:
#        resource = resource.filter(user)
#
#    ret = [ resource.target_states_log().latest('timestamp'),  ]
#
#    context = {
#        'q_limit':None,
#        'q_start':None,
#        'limited_target_states_log': ret
#    }
#    return render_to_response('blocks/states_log.xml', context)    
#    
#
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#def resource_by_log(request, log_id, resource_type):
#    
#    from state.models import TargetStateLog
#    from djlabs.http import HttpResponseRedirect
#    
#    try:
#        log = TargetStateLog.objects.get(id=log_id)
#        
#        if resource_type == 'target':
#            
#            resource = Target.objects.get(path=log.target_name)
#            
#        elif resource_type == 'node':
#            
#            resource = Target.objects.get(name=log.node_name)
#            
#        elif resource_type == 'iface':
#            
#            resource = Iface.objects.get(name=log.iface_name, node__name=log.node_name)
#            
#        else:
#            raise Exception("Invalid resource type '%s'" % (resource_type))
#    
#        url = get_rest_page(resource.resource_type, resource.id)
#    
#        return HttpResponseRedirect(url)
#        
#    except TargetStateLog.DoesNotExist, e:
#        return HttpResponse("Target with path '%s' not found! It doesn't exits or it has changed path." % (path,))
#
#def get_rest_page(resource_type, resource_id):
#    url =  '/%srest/#rest/%s/%s' % (settings.URL_PREFIX, resource_type, resource_id)
#    return url        
#
#
#
#def create_label(request):
#    
#    from rest.imaging import create_transparent_label
#    
#    LABELS_DIR = 'statecharts'
#    
#    text = request.REQUEST['text']
#    
#    text = text.encode('ascii','replace')
#    
#    fontsize = 14
#    
#    filename = '%s_%s_%s.png' % (text, 'arial', fontsize)
#    file_path = os.sep.join([settings.MEDIA_ROOT, LABELS_DIR, filename])
#    
#    #
#    # Create label file
#    #
#    if not os.path.exists(file_path):
#        
#        create_transparent_label(file_path, text, font_size=12)
#        
#        try:
#            user = settings.WEBSERVER_USER
#            userinfo = pwd.getpwnam(user)
#            uid = userinfo[2]
#            gid = userinfo[3]
#            os.chown( file_path, uid, gid )
#        except Exception, e:
#            pass
#        
#    #
#    # Send file
#    #        
#    f = open(file_path, "r+")
#    wrapper = FileWrapper(f)    
#    response = HttpResponse(wrapper, content_type='image/png')
#    response['Content-Length'] = os.path.getsize(file_path)            
#    #response['Cache-Control'] = 'no-cache'
#    #response['Pragma']        = 'no-cache'
#    #response['Expire']        = '-1'
#
#    return response        
#
#    
#    
#    
#    
#
##------------------------------------------------------------------------------#
##                                                                              #
##------------------------------------------------------------------------------#
#
#def handler500(request, *args, **kwargs):
#    t, i, tb = sys.exc_info()
#    sys.stderr.write("Sanet got a 500. Traceback and request details follow.\n")
#    try:
#        traceback.print_tb(tb, None, sys.stderr)
#        sys.stderr.write(str(i) + '\n')
#    except:
#        sys.stderr.write("Sanet got a 500 trying to write the traceback.\n")
#    try:
#        sys.stderr.write(pprint.pformat(request.__dict__) + '\n')
#    except:
#        sys.stderr.write("Sanet got a 500 trying to dump the request.\n")
#    sys.stderr.flush()
#
#    return HttpResponseServerError('Sorry, there was an internal error. There shoud really be details in the webserver log.')
#
#def handler404(request, *args, **kwargs):
#    sys.stderr.write("Sanet got a 404. Request details follow.\n")
#    try:
#        sys.stderr.write(pprint.pformat(request.__dict__) + '\n')
#    except:
#        sys.stderr.write("Sanet got a 500 trying to dump the request.\n")
#    sys.stderr.flush()
#
#    return HttpResponseServerError('Sorry, there was an 404 error. There shoud be details in the webserver log.')
#
#
