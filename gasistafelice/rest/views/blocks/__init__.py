import types

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson

from django.contrib.auth.models import User

from globals import type_model_d
from rest.models import BlockConfiguration

import logging

log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class AbstractBlock(object):
    
    BLOCK_NAME = "default name"
    BLOCK_DESCRIPTION = _("default description")
    BLOCK_VALID_RESOURCE_TYPES = None
    
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def __init__(self):
        
        self.app          = 'rest'
        
        self.loc          = 'body'

        self.name         = self.BLOCK_NAME
        self.description  = self.BLOCK_DESCRIPTION
        
        self.auto_refresh = False
        self.refresh_rate = 0

        self.start_open   = True
        self._resource    = None
    
    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#

    @property
    def block_name(self):
        return self.name

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def _get_user_actions(self, request):
        return []

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def is_valid(self, resource_type):
        """
        Returns true if the block is valid for the given resource_type.

        If class attribute BLOCK_VALID_RESOURCE_TYPES is None
        it means that it is valid for ALL KIND OF RESOURCES
        """

        if self.BLOCK_VALID_RESOURCE_TYPES is None:
            rv = True
        else:
            rv = resource_type in self.BLOCK_VALID_RESOURCE_TYPES
        return rv
        
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def visible_in_page(self):
        """
        Return true if the block can be added in user page.
        """
        return True

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def get_description(self):
        return self.description

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def options_response(self, request, resource_type, resource_id):
        # Return options for each block (like filtering contents...)
        #
        # No options by default
        #
        ctx={
            #'block_name' : 'Details',
            'fields': []
        }
        return render_to_response('options.xml', ctx)

    def validate_options(self, options_dict):
        # return no errors for user options
        return None

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#        
    
    def response_success(self):
        return HttpResponse(simplejson.dumps(self.response_dict))
        #WAS HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (self.resource.resource_type, self.resource.pk))

    def response_error(self, error_msg):
        response_dict = self.response_dict
        if not isinstance(error_msg, types.ListType):
            error_msg = [error_msg]
        response_dict['error_msg'] = error_msg
        return HttpResponse(simplejson.dumps(response_dict))
        
    def get_response(self, request, resource_type, resource_id, args):
        """Entry point for requests.

        Suddenly set `resource` attribute for block to `request.resource`
        and prepare `response_dict` with useful info to return in response.

        Every inherited class SHOULD overload this method instead 
        of override it. Call to this method in inherited classes 
        SHOULD happen before doing anything else.

        """

        self.request = request
        self.resource = request.resource
        self.response_dict = { 
                'resource_type' : self.resource.resource_type, 
                'resource_id' : self.resource.pk,
                'error_msg' : [],
        }

        log.debug(u"[block:%s] user: %s, resource: %s, args: %s, response_dict: %s" % (
            self.name, 
            request.user.username,
            self.resource, args,
            self.response_dict,
        ))

        return ""

    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def create_block_signature(self, resource_type, resource_id):
        
        resource_class = type_model_d[resource_type]
        resource = resource_class.objects.get(pk=int(resource_id))
        
        return self.create_block_signature_from_resource(resource)
        
    def create_block_signature_from_resource(self, resource):

        self.resource = resource
        # WARNING: se self.resource rather than resource! 
        # It is a property and getter and setter could be overridden
        block_urn = '%s/%s/%s/' % (self.resource.resource_type, self.resource.id, self.name)
        
        return '<block \
                     block_name="%s" \
                     block_description="%s" \
                     \
                     block_urn="%s" \
                     resource_name="%s" \
                     \
                     refresh_rate="%s" \
                     auto_refresh="%s" \
                     start_open="%s" \
                />' % (
            self.block_name,
            '%s' % (self.get_description()),
            block_urn,
            self.resource, #was: str(self.resource)... that's why it may be None?!?
            self.refresh_rate,
            str(self.auto_refresh).lower(),
            str(self.start_open).lower(),
        )

    #------------------------------------------------------------------------------#        
    # Useful methods                                                               #
    #------------------------------------------------------------------------------#        

    def load_user_configuration(self, user, resource_type, resource_id):
        # Retrieve block configuration stored by a user
    
        config = None
        
        try:
            blocks_conf = BlockConfiguration.objects.get(blocktype=self.block_name
                                       ,user=user
                                       ,resource_type=resource_type
                                       ,resource_id=resource_id
                                       )
                                       
            config = blocks_conf.get_configuration()
            
            config = self.from_xml_to_dict(config)
            
            return config            
            
        except Exception, e:
            pass

        return config 
    
    def from_xml_to_dict(self, xml_string):
        from xml.dom import minidom
        
        d = {}
        xmldoc = minidom.parseString(xml_string)             
        
        for param in xmldoc.getElementsByTagName("param"):
            name = param.attributes['name'].value
            val  = param.attributes['value'].value
            
            d[name] = val

        return d



    def read_cookie(self, resource_type, resource_id, cookie):
        
        d = {}
        for k,v in cookie.items():
            
            # block_<app>_<resource type>_<resource_id>_<block_name>_ + _<var_name> = <val>
            
            parts = k.split('__')
            if len(parts) != 2: continue
            
            block_id = parts[0]
            var_name = parts[1]
            
            if block_id[ -len(self.name) : ] != self.name: continue
            block_id = block_id[ : - (1+len(self.name)) ] 

            (dummy, app, t, i) = re.split('_', block_id)
            
            if app != self.app:
                continue
                
            if t == resource_type and i == resource_id:
                
                d[var_name] = v
                
        return d
