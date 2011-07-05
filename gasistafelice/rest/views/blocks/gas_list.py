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

#TODO fero CHECK this is not needed anymore because DES model is bound to DjangoSite
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

class Block(AbstractBlock):

    def __init__(self):
        super(Block, self).__init__()

        self.name        = "gas_list" 
        self.description = _("GAS")
        
        self.auto_refresh = False
        self.refresh_rate = (60 * 2)
        
        self.start_open  = True
    
        
    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def is_valid(self, resource_type):
        # This block is only valid for DES, Supplier and User
        # When related to DES it shows GAS available in DES
        # When related to Supplier it show GAS bound to the Supplier through a pact
        # When related to User it show GAS for which the User is a GASMember
        # Note in gas_response that there is a common API: just invoke resource.gas_list
        return resource_type in ["site", "supplier", "user"]

    def visible_in_page(self):
        return True
        
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#

    #TODO fero
    #def options_response(self, request, resource_type, resource_id):

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        resource = request.resource

        if args == "":
            gas_list = resource.gas_list

            context = {
                'block_type' : self.name,
                'resource'   : resource,
                'resource_list' : gas_list
            }
            return render_to_xml_response('blocks/resource_list.xml', context)

        else:
            raise NotImplementedError

# TODO fero CHECK
# THIS IS USEFUL FOR USER ACTIONS: add/update/delete
#        # Calculate allowed user actions
#        #    
#        user_actions = []
#        
#        if settings.CAN_CHANGE_CONFIGURATION_VIA_WEB == True:
#            user = request.user
#            if can_write_to_resource(user,res):
#                if resource_type in ['container', 'node', 'target', 'measure']:
#                    
#                    if (resource_type in ['target', 'measure']):
#                        if res.suspended:
#                            user_actions.append('resume')
#                        else:
#                            user_actions.append('suspend')
#                    else:
#                        user_actions.append('resume')
#                        user_actions.append('suspend')

# TODO fero CHECK
# THIS IS USEFUL FOR ADD/REMOVE NEW GAS
#        elif args == "new_note":
#            return self.add_new_note(request, resource_type, resource_id)
#        elif args == "remove_note":
#            return self.remove_note(request, resource_type, resource_id)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
        
# TODO fero CHECK
# THIS IS USEFUL FOR ADD/REMOVE NEW GAS
#    def add_new_note(self,request, resource_type, resource_id):
#        resource = request.resource
#        
#        if request.POST:
#            
#            #title = request.REQUEST.get('title');
#            body  = request.REQUEST.get('body');
#            
#            new_comment = Comment(content_object = resource
#                             ,site = DjangoSite.objects.all()[0]
#                             ,user = request.user
#                             ,user_name = request.user.username
#                             ,user_email = request.user.email
#                             ,user_url = ''
#                             ,comment = body
#                             ,ip_address = None
#                             ,is_public = True
#                             ,is_removed = False                       
#                             )
#                        
#            new_comment.save()
#
#            return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (resource.resource_type, resource.id))
#            
#        return HttpResponse('')
#            
#    #------------------------------------------------------------------------------#    
#    #                                                                              #     
#    #------------------------------------------------------------------------------#
#            
#    def remove_note(self, request, resource_type, resource_id):
#        
#        resource = request.resource
#        
#        note_id = request.REQUEST.get('note_id')
#        
#        note = Comment.objects.get(id=note_id)
#        note.delete()
#
#        return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (resource.resource_type, resource.id))
        
