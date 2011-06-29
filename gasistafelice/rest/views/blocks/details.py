import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models #fields types

# Notes (Comment)
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from django.contrib.sites.models import Site as DjangoSite
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from gasistafelice.lib.fields import ResourceList
from gasistafelice.lib.shortcuts import render_to_xml_response
from gasistafelice.base.models import Resource
from gasistafelice.des.models import Site
from gasistafelice.rest.views.blocks import AbstractBlock

#from users.models import can_write_to_resource

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

DETAILS_DEFAULT_OPTIONS = {
    'show_problems'    : 'False',
    'show_uncheckables': 'False',
}

class Block(AbstractBlock):

    def __init__(self):
        super(Block, self).__init__()

        self.name        = "details"            
        self.description = _("Details")
        
        self.auto_refresh = False
        self.refresh_rate = (60 * 2)
        
        self.start_open  = True
    
        
    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def is_valid(self, resource_type):
        return True

    def visible_in_page(self):
        return True
        
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#

    def options_response(self, request, resource_type, resource_id):
        
        user = request.user

        options = self.load_user_configuration(user, resource_type, resource_id)
        
        if not options:
            options = DETAILS_DEFAULT_OPTIONS
                    
        #paranoic programming
        if not isinstance(options, types.DictType): options = DETAILS_DEFAULT_OPTIONS
        options['show_problems']     = options.get('show_problems'    , 'True')
        options['show_uncheckables'] = options.get('show_uncheckables', 'True')
        
        ctx = {
            'block_name': 'Dettagli',
            'fields': [
                {'field_type':'checkbox', 'field_label':_('Show problems')    , 'field_name':'show_problems'    , 'field_values':[ options['show_problems']     ]},
                {'field_type':'checkbox', 'field_label':_('Show unchechables'), 'field_name':'show_uncheckables', 'field_values':[ options['show_uncheckables'] ]},
            ]
        }
        return render_to_xml_response('options.xml', ctx)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        if args == "":
            return self.render_details_block(request, resource_type, resource_id)
        elif args == "new_note":
            return self.add_new_note(request, resource_type, resource_id)
        elif args == "remove_note":
            return self.remove_note(request, resource_type, resource_id)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def render_details_block(self, request, resource_type, resource_id):

        user = request.user
        res = request.resource
        
        if isinstance(res, Site) and not user.is_superuser:
            res = res.filter(user)

        info = ''

        #
        # LOAD USER OPTIONS. Remember that values are strings!
        #
        options = self.load_user_configuration (user, resource_type, resource_id)
        if not options:    options = DETAILS_DEFAULT_OPTIONS 
        show_problems     = True if options.get('show_problems'    , 'False') == 'True' else False
        show_uncheckables = True if options.get('show_uncheckables', 'False') == 'True' else False


        # Retrieve resource's cached informations
        res.load_checkdata_from_cache()
        
        #
        # Calculate visible informations
        #
        df = []
        for display_field in res.display_fields:
            
            element_value = ''
            element_type  = ''
            element_warning = ''    # 'on' will make the value look red
            
            #print "DETTAGLIO PRE: ", type(c)
            
            if isinstance(display_field, types.StringTypes) or isinstance(display_field, types.UnicodeType):
                element_type  = 'str'
                display_field= res._meta.get_field(display_field)
                
            element_value = getattr(res, display_field.name)
            if element_value != None:

                if isinstance(display_field, ResourceList):
                    element_type  = 'resourcelist'
                elif isinstance(element_value, Resource):
                    element_type = str(element_value.resource_type)
                elif isinstance(display_field, models.EmailField):
                    element_type  = 'email'
                else:    
                    element_type  = 'str'
            else:
                element_type = 'none'
                element_value = ''
            
            info_element = {
                "name"  : display_field.name,
                "text"  : display_field.verbose_name,
                "type"  : element_type,
                "value" : element_value,
                "warning": element_warning
            }
                
            df.append(info_element)

        #
        # Calculate resource notes
        #
        notes = self.get_notes(res, request.user)
        
        #
        # Calculate allowed user actions
        #    
        user_actions = []
        
        if settings.CAN_CHANGE_CONFIGURATION_VIA_WEB == True:
            user = request.user
            if can_write_to_resource(user,res):
                if resource_type in ['container', 'node', 'target', 'measure']:
                    
                    if (resource_type in ['target', 'measure']):
                        if res.suspended:
                            user_actions.append('resume')
                        else:
                            user_actions.append('suspend')
                    else:
                        user_actions.append('resume')
                        user_actions.append('suspend')
            
        #
        # Prepere data for the templage
        #
        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'rimage'        : self.get_image(res, '128x128', "png"),
            'display_fields': df,
            'more_details'  : res.details if hasattr(res, 'details') else None,
            'notes'         : notes,
            'user_actions'  : user_actions,
            'config'        : options,
        }
        
        #
        # Addidional link to the BIRT report page
        #
        if settings.ENABLE_OLAP_REPORTS:

            if resource_type in ['node','container']:

            
                """
                url = settings.OLAP_URL_STRING % { 'resource_type' : resource_type , 'resource_id':resource_id}
                
                olap_data = {
                     'olap_url' : '%s://%s:%s/%s' % (settings.OLAP_PROTOCOL, settings.OLAP_SERVER_ADDRESS, settings.OLAP_SERVER_PORT, url) 
                    ,'olap_user_id': request.user.id
                    ,'olap_session_id': request.COOKIES['sessionid'] 
                    ,'olap_report_type': 'sanet_olap_no_cube/%s' % res.resource_type
                    ,'olap_resource_type': res.resource_type
                    ,'olap_resource_name': res.name
                }
                olap_data['olap_url'] = "%(olap_url)s?%(olap_resource_type)s=%(olap_resource_name)s&__report=%(olap_report_type)s.rptdesign&user_id=%(olap_user_id)s&session_id=%(olap_session_id)s" % olap_data
                """
            
                olap_data = {}
                
                vname = "rest.views.actions.olap_reports_redirect"
                kwargs = {'resource_type': resource_type, 'resource_id': resource_id }
                url = reverse(vname, args=[], kwargs=kwargs)            
            
                olap_data['olap_url'] = url
            
                ctx.update(olap_data)
        
        
        #
        # RENDER 
        #
        return render_to_xml_response('blocks/details.xml', ctx)
        


    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
        
    def get_notes(self, resource, user):

        visible_notes = resource.allnotes
        
        #
        # TODO: do not show notes belonging to users of other groups?
        #
        
        return visible_notes


    def get_image(self, resource, type, ext):
        
        basedir = os.path.join(settings.MEDIA_URL, "theme", "img", "resources")
        if hasattr(resource,'icon'):
            value = os.path.join(basedir, "%s%s.%s" % (resource.icon.fname, type, ext))
        else:
            value = os.path.join(basedir, "%s%s.%s" % (resource.resource_type, type, ext))
        
        return value        
        
        """
        #filename_end = type + "." + ext
        #base_path = os.path.join('theme', 'img', 'resources')

        name = resource.name.lower()
        try:
            cat_name = resource.category.name.lower()
        except AttributeError:
            cat_name = None
            
        try:
            #controlla le performance di questa operazione, se e' lenta prova a farla
            #nel caso falliscano le prime due ricerche
            catbranch_name = resource.category.site_branch.lower()
        except AttributeError:
            #Abbiamo a che fare con il site
            catbranch_name = resource.__class__.__name__.lower()

        parent_paths = []
        try:
            x = resource.category
            while (x.parent):
                parent_paths.append(os.path.join(base_path, x.parent.name) + filename_end)
                x = x.parent
        except AttributeError:
            #No problem if this list is empty
            pass

        icon_possible_paths = []
        if cat_name:
            icon_possible_paths += [
                os.path.join(base_path, cat_name, name) + filename_end,
                os.path.join(base_path, cat_name) + filename_end
            ]

        icon_possible_paths += parent_paths

        if catbranch_name:
            icon_possible_paths.append(os.path.join(base_path, catbranch_name) + filename_end)

        icon_possible_paths += [
            os.path.join(base_path, "default_icon" + filename_end),
            os.path.join(base_path, "default_icon." + ext)
        ]

        i = 0
        icon_path = False
        while (not icon_path) and (i < len(icon_possible_paths)):
            possible_path = icon_possible_paths[i]
            icon_path = os.path.exists(os.path.join(settings.MEDIA_ROOT, possible_path))
            i += 1

        if not icon_path:
            raise ValueError, "No icon found for %s object, please create at least the default icon %s" % (resource.name, icon_possible_paths[-1])

        icon_url = os.path.join(settings.MEDIA_URL, possible_path)
        return icon_url
            """
            
    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
        
    def add_new_note(self,request, resource_type, resource_id):
        resource = request.resource
        
        if request.POST:
            
            #title = request.REQUEST.get('title');
            body  = request.REQUEST.get('body');
            
            new_comment = Comment(content_object = resource
                             ,site = DjangoSite.objects.all()[0]
                             ,user = request.user
                             ,user_name = request.user.username
                             ,user_email = request.user.email
                             ,user_url = ''
                             ,comment = body
                             ,ip_address = None
                             ,is_public = True
                             ,is_removed = False                       
                             )
                        
            new_comment.save()

            return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (resource.resource_type, resource.id))
            
        return HttpResponse('')
            
    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
            
    def remove_note(self, request, resource_type, resource_id):
        
        resource = request.resource
        
        note_id = request.REQUEST.get('note_id')
        
        note = Comment.objects.get(id=note_id)
        note.delete()

        return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (resource.resource_type, resource.id))
        
