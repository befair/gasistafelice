import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers
from django.forms.formsets import formset_factory

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse
from django.db import models #fields types
from django.db import transaction
from django.template import RequestContext

# Notes (Comment)
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from django.contrib.sites.models import Site as DjangoSite
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from workflows.utils import get_allowed_transitions, do_transition
from workflows.models import Transition

from flexi_auth.models import PrincipalParamRoleRelation, ObjectWithContext

from lib.fields import display

from lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from lib.formsets import BaseFormSetWithRequest
from app_base.models import Resource
from des.models import Site
from rest.views.blocks import AbstractBlock
from rest.views.blocks.base import ResourceBlockAction
from app_base.workflows_utils import get_allowed_transitions, do_transition

from consts import EDIT, VIEW_CONFIDENTIAL

# Needed for HACK: see below
from consts import GAS_MEMBER

#from users.models import can_write_to_resource

import logging
log = logging.getLogger(__name__)

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

DETAILS_DEFAULT_OPTIONS = {
    'show_problems'    : 'False',
    'show_uncheckables': 'False',
}

class Block(AbstractBlock):

    BLOCK_NAME = "details"
    FORMCLASS_MANAGE_ROLES = None

    def __init__(self):
        super(Block, self).__init__()

        self.description = _("Details")
        
        self.auto_refresh = False
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

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):

            # Duck-typing
            # Invoke an unneeded method just to check if an exception happen
            try:
                self._get_edit_form_class()
            except NotImplementedError as e:
                # If edit_form_class is not implemented, log the event
                log.debug(str(e))
            else:
                klass_name = self.resource.__class__.__name__
                url = None
                
                user_actions.append(

                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name=EDIT, verbose_name=_("Edit"), 
                        popup_form=True,
                        url=url
                    )
                )

            if self._get_roles_formset_class():

                user_actions.append(

                    # Referrers assignment
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name="manage_roles", verbose_name=_("Manage roles"), 
                        popup_form=True,
                    )
                )

            # Show actions for transition allowed for this resource

            for t in get_allowed_transitions(request.resource, request.user):
                #FIXME: related to gas/workflows_data.py ugettext_laxy FIXME
                local_transitions = {
                    'Open' : 'Apri',
                    'Close' : 'Chiudi',
                    'Close and send email' : 'Chiudi e invia email',
                    'Archive' : 'Archivia',
                    'Cancel' : 'Annulla',
                }
                
                translated_t = local_transitions.get(t.name,t.name)
                #ENDFIXME

                action = ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="transition/%s" % t.name.lower(), 
                    verbose_name=translated_t, 
                    popup_form=False,
                    url=None
                )

                user_actions.append( action )
                

        return user_actions

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        klass_name = self.resource.__class__.__name__
        raise NotImplementedError("No edit_form_class for a %s, Maybe you need a subclass?" % klass_name)

    def _get_roles_formset_class(self):

        if self.FORMCLASS_MANAGE_ROLES:
            rv = formset_factory(
                form=self.FORMCLASS_MANAGE_ROLES, 
                formset=BaseFormSetWithRequest, 
                extra=5
            )
        else:
            rv = None

        return rv

    def manage_roles(self, request):

        formset_class = self._get_roles_formset_class()

        if request.method == 'POST':

            formset = formset_class(request, request.POST)
            
            if formset.is_valid():
                with transaction.commit_on_success():
                    for form in formset:
                        # Check for data: empty formsets are full of empty data ;)
                        if form.cleaned_data:
                            form.save()
                return self.response_success()
        else:

            data = {}
            roles = self.resource.roles

            # HACK HERE
            # Exclude GAS_MEMBER role which is managed by "Add gasmember" action
            # ...it could be excluded everytime, even if resource_type is not "gas"...
            if self.resource.resource_type == "gas":
                roles = roles.exclude(role__name=GAS_MEMBER)

            # Roles already assigned to resource
            pprrs = PrincipalParamRoleRelation.objects.filter(role__in=roles)

            i = 0
            for i,pprr in enumerate(pprrs):

                key_prefix = 'form-%d' % i
                data.update({
                   '%s-id' % key_prefix : pprr.pk,
                   '%s-person' % key_prefix : pprr.user.person.pk,
                   '%s-role' % key_prefix : pprr.role.pk,
                })

            data['form-TOTAL_FORMS'] = i + formset_class.extra
            data['form-INITIAL_FORMS'] = i
            data['form-MAX_NUM_FORMS'] = 0

            formset = formset_class(request, data)

        context = {

            "formset": formset,
            'opts' : PrincipalParamRoleRelation._meta,
            'is_popup': False,
            'save_as' : False,
            'save_on_top': False,
            #'errors': helpers.AdminErrorList(form, []),
            #'media': mark_safe(adminForm.media),
            'form_url' : request.build_absolute_uri(),
            'add'  : False,
            'change' : True,
            'has_add_permission': False,
            'has_delete_permission': True,
            'has_change_permission': True,
            'show_delete' : True,

        }

        return render_to_context_response(request, "html/formsets.html", context)

    def _edit_resource(self, request):

        form_class = self._get_edit_form_class()
        if request.method == 'POST':

            form = form_class(request, request.POST, request.FILES, instance=request.resource)
            if form.is_valid():
                form.save()
                return self.response_success()
            else:
                try:
                    #TODO fero
                    form.write_down_messages()
                except AttributeError as e:
                    log.warning('Refactory needed: calling non-existent write_down_messages on form_class=%s' % form_class)
                    pass #don't worry for this exception...

        else:
            form = form_class(request, instance=request.resource)
            try:
                #TODO fero
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
            'add'  : False,
            'change' : True,
            'is_popup': False,
            'save_as' : False,
            'save_on_top': False,
            'has_add_permission': False,
            'has_delete_permission': True,
            'has_change_permission': True,
            'show_delete' : False,
            'errors': helpers.AdminErrorList(form, []),
        }

        template = "html/admin_form.html"
        return render_to_response(template, context, context_instance=RequestContext(request))

    def get_response(self, request, resource_type, resource_id, args):

        super(Block, self).get_response(request, resource_type, resource_id, args)

        if args == "":
            return self.render_details_block(request, resource_type, resource_id)
        elif args == EDIT:
            # Server-side check for permission on this view
            if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
                with transaction.commit_on_success():
                    rv = self._edit_resource(request)
                return rv
            raise PermissionDenied

        elif args == "new_note":
            return self.add_new_note(request, resource_type, resource_id)
        elif args == "remove_note":
            return self.remove_note(request, resource_type, resource_id)
        elif args == "manage_roles":
            return self.manage_roles(request)
        elif args.startswith("transition"):
            t_name = args.split("/")[1]
            allowed_transitions = get_allowed_transitions(request.resource, request.user)
            t = Transition.objects.get(name__iexact=t_name, workflow=request.resource.workflow)
            if t in allowed_transitions:
                request.resource.do_transition(t, request.user)
                return self.response_success()
            else:
                return HttpResponse('')

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
            
            #log.debug("DETTAGLIO PRE: ", type(c))
            
            if isinstance(display_field, types.StringTypes) or isinstance(display_field, types.UnicodeType):
                element_type  = 'str'
                display_field= res._meta.get_field(display_field)
                
            element_value = getattr(res, display_field.name)
            if element_value != None:

                if isinstance(display_field, display.ResourceList):
                    element_type  = 'resourcelist'
                elif isinstance(element_value, Resource):
                    element_type = 'resource'
                elif isinstance(display_field, models.EmailField):
                    element_type  = 'email'
                elif isinstance(display_field, models.FileField):
                    element_type  = 'file'
                    try:
                        element_value = element_value.url
                    except ValueError:
                        element_value = ''
                elif isinstance(element_value, bool):
                    element_type = 'bool'
                else: 
                    element_type  = 'str'
                    if display_field.choices:
                        element_value = getattr(res, "get_%s_display" % display_field.name)()
            else:
                element_type = 'none'
                element_value = ''
            

            if (display_field.name in self.resource.confidential_fields) and \
                not self.request.user.has_perm(
                    VIEW_CONFIDENTIAL, 
                    obj=ObjectWithContext(self.request.resource)
                ):

                element_value = _("confidential data")
                
                    
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
        user_actions = self._get_user_actions(request)
            
        #
        # Prepare data for the templage
        #
        ctx = {
            'resource'      : res,
            'sanet_urn'     : "%s/%s" % (resource_type, resource_id),
            'rimage'        : res.icon.url,
            'display_fields': df,
            'more_details'  : res.details if hasattr(res, 'details') else None,
            'notes'         : notes,
            'user_actions'  : user_actions,
            'config'        : options,
        }
        
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

            return self.response_success()
            
        return HttpResponse('')
            
    #------------------------------------------------------------------------------#    
    #                                                                              #     
    #------------------------------------------------------------------------------#
            
    def remove_note(self, request, resource_type, resource_id):
        
        resource = request.resource
        
        note_id = request.REQUEST.get('note_id')
        
        note = Comment.objects.get(id=note_id)
        note.delete()

        return self.response_success()
        
