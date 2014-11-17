import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.admin import helpers
from django.utils.safestring import mark_safe

from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction

# Notes (Comment)
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

#TODO fero CHECK this is not needed anymore because DES model is bound to DjangoSite
from django.contrib.sites.models import Site as DjangoSite

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from lib.views_support import prepare_datatables_queryset, render_datatables
from app_base.models import Resource
from des.models import Site
from rest.views.blocks import AbstractBlock

from consts import CREATE, EDIT_MULTIPLE
CREATE_PDF = "createpdf"
CREATE_CSV = "createcsv"
VIEW_AS_HTML = "viewhtml"
SENDME_PDF = "emailmepdf"
SENDPROD_PDF = "emailprodpdf"
CREATE_HTML = "createhtml"
EXPORT_GDXP = "export"

import logging
log = logging.getLogger(__name__)

#from users.models import can_write_to_resource
#------------------------------------------------------------------------------#
# Actions                                                                      #
#------------------------------------------------------------------------------#

class Action(object):

    def __init__(self, name, verbose_name, url, popup_form=True, method="POST", confirm_text=""):

        self.name = name
        self.verbose_name = verbose_name
        self.url = url
        self.popup_form = popup_form
        self.method = method
        self.confirm_text = confirm_text

class ResourceBlockAction(Action):
    """Action included in a resource block.

    Usually you should use this class"""

    def __init__(self, resource, block_name, name, verbose_name, url=None, 
        popup_form=True, method="POST", confirm_text=""
    ):

        self.resource = resource
        self.block_name = block_name
        if not url:
            url = "%s/%s/%s" % (resource.urn, block_name, name)
        super(ResourceBlockAction, self).__init__(name, verbose_name, 
            url, popup_form, method=method, confirm_text=confirm_text
        )

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class BlockWithList(AbstractBlock):

    TEMPLATE_ADD_FORM = "html/admin_form.html"
    TEMPLATE_RESOURCE_LIST = "blocks/resource_list.xml"
    TEMPLATE_RESOURCE_LIST_WITH_DETAILS = "blocks/resource_list_with_details.xml"

    #TODO fero
    #def options_response(self, request, resource_type, resource_id):

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def _get_more_context_info(self, request):
        """Return dict to be inserted in 'more_info' key of context dict"""
        return {}

    def _get_resource_list(self, request):
        """Return resource list to be rendered"""
        raise NotImplementedError

    def _get_add_form_class(self):
        """Return add form class. Usually a FormFromModel"""
        raise NotImplementedError

    def _add_resource(self, request):

        form_class = self._get_add_form_class()
        if request.method == 'POST':

            form = form_class(request, request.POST)
            if form.is_valid():
                form.save()
                return self.response_success()
                
            else:
                try:
                    #TODO-not-a-priority fero
                    form.write_down_messages()
                except AttributeError as e:
                    log.warning('Refactory needed: calling non-existent write_down_messages on form_class=%s' % form_class)
                    pass #don't worry for this exception...
        else:
            form = form_class(request)
            try:
                #TODO-not-a-priority fero
                form.write_down_messages()
            except AttributeError as e:
                log.warning('Refactory needed: calling non-existent write_down_messages on form_class=%s' % form_class)
                pass #don't worry for this exception...

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
            'errors': helpers.AdminErrorList(form, []),
            'media': mark_safe(adminForm.media),
        }

        return render_to_context_response(request, self.TEMPLATE_ADD_FORM, context)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        super(BlockWithList, self).get_response(request, resource_type, resource_id, args)

        if args == "":

            context = {
                'block_type' : self.name,
                'resource'   : self.resource,
                'resource_list'   : self._get_resource_list(request),
                'user_actions'    : self._get_user_actions(request),
                'more_info'     : self._get_more_context_info(request),
            }

            # Not used now
            if request.GET.get('render_as') == 'resource_list_with_details':
                template = self.TEMPLATE_RESOURCE_LIST_WITH_DETAILS
            else:
                template = self.TEMPLATE_RESOURCE_LIST
                
            return render_to_xml_response(template, context)

        elif args == CREATE:

            with transaction.commit_on_success():
                rv = self._add_resource(request)
            return rv

        else:
            raise NotImplementedError


class BlockSSDataTables(BlockWithList):
    """Block with list suitable for jQuery.dataTables http://datatables.net).

    This class helps in building blocks with list in which data representation
    is prepared for "server side processing" by jQuery.dataTables.

    Server side steps needed:

    1. return block content which holds table structure
    2. provide methods for dataTables API:
        - input: objects to retrieve, keywords to search, offset, ...
        - output: json rendering
    
    Client side use dataTables to deal with the block

    For a full example see: http://www.assembla.com/spaces/datatables_demo/wiki
    """

    KW_DATA = "view"

    # To be overridden in subclass. Required for correct sorting behaviour
    COLUMN_INDEX_NAME_MAP = {} 

    def __init__(self):
        super(BlockSSDataTables, self).__init__()
        #self.BLOCK_TEMPLATE = "blocks/%s/block.xml" % self.BLOCK_NAME
        self.BLOCK_TEMPLATE = "blocks/%s/table.xml" % self.BLOCK_NAME

    def _get_records(self, request, querySet):
        raise NotImplementedError("To be implemented in subclass")

    def _get_edit_multiple_form_class(self):
        raise NotImplementedError("_get_edit_multiple_form_class should be implemented in subclass")

    def _do_post_edit_multiple(self):

        request = self.request

        form_class = self._get_edit_multiple_form_class()
        try:
            formset = form_class(request, request.POST)
        except AttributeError as e:
            # TODO-not-a-priority: fero ... thinking about it....
            # NOTE fero: Form refactory neeeded: 'WSGIRequest' object has no attribute 'get'
            # NOTE fero: Following NOTES-FERO we will do: 
            # NOTE fero: if isinstance(form_class, FormRequestWrapper)
            # NOTE fero:    f = form_class(request, request.POST)
            # NOTE fero:    formset = f.form
            formset = form_class(request.POST)

        if formset.is_valid():
            with transaction.commit_on_success():
                for form in formset:
                    # Check for data: empty formsets are full of empty data ;)
                    if form.cleaned_data:
                        form.save()
            return self.response_success()
        else:
            return self.response_error(formset.errors)

    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#

    def get_response(self, request, resource_type, resource_id, args):

        super(BlockWithList, self).get_response(request, resource_type, resource_id, args)

        if args == "":

            context = {
                'block_type' : self.name,
                'resource'   : self.resource,
                'user_actions'    : self._get_user_actions(request),
            }

            template_name = self.BLOCK_TEMPLATE
            return render_to_xml_response(template_name, context)

        elif args == self.KW_DATA:

            querySet = self._get_resource_list(request) 
            #columnIndexNameMap is required for correct sorting behavior
            columnIndexNameMap = self.COLUMN_INDEX_NAME_MAP
            #path to template used to generate json (optional)
            jsonTemplatePath = 'blocks/%s/data.json' % self.BLOCK_NAME

            querySet, dt_params = prepare_datatables_queryset(request, querySet, columnIndexNameMap)
            return render_datatables(request, querySet, dt_params, jsonTemplatePath)

        elif args == EDIT_MULTIPLE:

            if request.method == 'POST':

                return self._do_post_edit_multiple()
                    
            querySet = self._get_resource_list(request) 
            #columnIndexNameMap is required for correct sorting behavior
            columnIndexNameMap = self.COLUMN_INDEX_NAME_MAP
            #path to template used to generate json (optional)
            jsonTemplatePath = 'blocks/%s/edit_multiple.json' % self.BLOCK_NAME

            querySet, dt_params = prepare_datatables_queryset(request, querySet, columnIndexNameMap)
            formset, records, moreData = self._get_records(request, querySet)

            return render_datatables(request, records, dt_params, jsonTemplatePath, moreData=moreData)
            
        elif args == CREATE:

            with transaction.commit_on_success():
                rv = self._add_resource(request)
            return rv

        else:
            raise NotImplementedError("args = %s" % args)

