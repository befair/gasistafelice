import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.admin import helpers

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
from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.base.models import Resource
from gasistafelice.des.models import Site
from gasistafelice.rest.views.blocks import AbstractBlock

from gasistafelice.auth import CREATE

#from users.models import can_write_to_resource

#------------------------------------------------------------------------------#
# Actions                                                                      #
#------------------------------------------------------------------------------#

class Action(object):

    def __init__(self, name, verbose_name, url, has_form=True):

        self.name = name
        self.verbose_name = verbose_name
        self.url = url
        self.has_form = has_form

class ResourceBlockAction(Action):
    """Action included in a resource block.

    Usually you should use this class"""

    def __init__(self, resource, block_name, name, verbose_name, url=None, has_form=True):

        self.resource = resource
        self.block_name = block_name
        if not url:
            url = "%s/%s/%s" % (resource.urn, block_name, name)
        super(ResourceBlockAction, self).__init__(name, verbose_name, url, has_form)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class BlockWithList(AbstractBlock):

    TEMPLATE_ADD_FORM = "html/admin_form.html"
    TEMPLATE_RESOURCE_LIST = "blocks/resource_list.xml"

    #TODO fero
    #def options_response(self, request, resource_type, resource_id):

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def _get_resource_list(self, request):
        """Return resource list to be rendered"""
        raise NotImplementedError

    def _get_add_form_class(self):
        """Return add form class. Usually a FormFromModel"""
        raise NotImplementedError

    def _process_valid_form(self, form):
        """Process form which passed is_valid() check"""
        form.save()

    def _add_resource(self, request):

        form_class = self._get_add_form_class()
        if request.method == 'POST':

            form = form_class(request, request.POST)
            if form.is_valid():
                self._process_valid_form(form)
                return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (request.resource.resource_type, request.resource.pk))
                
        else:
            form = form_class(request)

        fields = form.base_fields.keys()
        fieldsets = form_class.Meta.gf_fieldsets
        adminForm = helpers.AdminForm(form, fieldsets, {}) 

        context = {
            'form' : form,
            'adminform' : adminForm,
            'opts' : form._meta.model._meta,
            'add'  : True,
            'change' : False,
            'is_popup': False,
            'save_as' : False,
            'save_on_top': False,
            'has_add_permission': True,
            'has_delete_permission': True,
            'has_change_permission': False,
            'show_delete' : False,
        }

        return render_to_context_response(request, self.TEMPLATE_ADD_FORM, context)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        resource = request.resource

        if args == "":

            context = {
                'block_type' : self.name,
                'resource'   : resource,
                'resource_list'   : self._get_resource_list(request),
                'user_actions'    : self._get_user_actions(request),
            }

            if request.GET.get('display') == 'resource_list_with_details':
                template = self.TEMPLATE_RESOURCE_LIST_WITH_DETAILS
            else:
                template = self.TEMPLATE_RESOURCE_LIST
                
            return render_to_xml_response(template, context)

        elif args == CREATE:

            return self._add_resource(request)

        else:
            raise NotImplementedError


