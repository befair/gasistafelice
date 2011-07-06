import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse

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

class BlockWithList(AbstractBlock):

    #TODO fero
    #def options_response(self, request, resource_type, resource_id):

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        resource = request.resource

        if args == "":

            context = {
                'block_type' : self.name,
                'resource'   : resource,
                'resource_list'   : self._get_resource_list(request)
            }
            return render_to_xml_response('blocks/resource_list.xml', context)

        else:
            raise NotImplementedError

