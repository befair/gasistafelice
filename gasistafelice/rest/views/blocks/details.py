import os
import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models #fields types
from django.db import transaction

# Notes (Comment)
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from django.contrib.sites.models import Site as DjangoSite
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from gasistafelice.lib.fields.display import ResourceList
from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response
from gasistafelice.base.models import Resource
from gasistafelice.des.models import Site
from gasistafelice.rest.views.blocks import AbstractBlock
from gasistafelice.rest.views.blocks.base import ResourceBlockAction

from gasistafelice.auth import EDIT

from gas.forms import order, EDIT_PactForm
from workflows.utils import get_allowed_transitions, do_transition
from workflows.models import Transition

#from users.models import can_write_to_resource

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

DETAILS_DEFAULT_OPTIONS = {
    'show_problems'    : 'False',
    'show_uncheckables': 'False',
}

class Block(AbstractBlock):

    BLOCK_NAME = "details"

    def __init__(self):
        super(Block, self).__init__()

        self.name        = "details"            
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

        if request.user.has_perm(EDIT, obj=request.resource):
            klass_name = self.resource.__class__.__name__
            url = None
            if klass_name == "GAS":
                url = reverse('admin:gas_gas_change', args=(request.resource.pk,))
            
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT, verbose_name=_("Edit"), 
                    popup_form=True,
                    url=url
                )
            )

            if klass_name == "GAS":
                user_actions.append( 
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name="configure", verbose_name=_("Configure"), 
                        popup_form=True,
                        url=reverse('admin:gas_gasconfig_change', args=(request.resource.config.pk,))
                    )
                )


            for t in get_allowed_transitions(request.resource, request.user):
                user_actions.append( 
                    ResourceBlockAction( 
                        block_name = self.BLOCK_NAME,
                        resource = request.resource,
                        name="transition/%s" % t.name.lower(), verbose_name=t, 
                        popup_form=False,
                        url=None
                    )
                )
                

        return user_actions

    def _get_edit_form_class(self):
        """Return edit form class. Usually a FormFromModel"""
        klass_name = self.resource.__class__.__name__
        if klass_name == "GASSupplierSolidalPact":
            return EDIT_PactForm 
        if klass_name == "GASSupplierOrder":
            return order.form_class_factory_for_request(self.request)
        else:
            raise NotImplementedError("no edit_form_class for a %s" % klass_name)

    def _edit_resource(self, request):

        form_class = self._get_edit_form_class()
        if request.method == 'POST':

            form = form_class(request, request.POST, instance=request.resource)
            if form.is_valid():
                form.save()
                return self.response_success
                
        else:
            form = form_class(request, instance=request.resource)

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

        return render_to_context_response(request, "html/admin_form.html", context)

    def get_response(self, request, resource_type, resource_id, args):

        self.request = request
        self.resource = request.resource

        if args == "":
            return self.render_details_block(request, resource_type, resource_id)
        elif args == EDIT:
            # Server-side check for permission on this view
            if request.user.has_perm(EDIT, obj=request.resource):
                with transaction.commit_on_success():
                    rv = self._edit_resource(request)
                return rv
            raise PermissionDenied

        elif args == "new_note":
            return self.add_new_note(request, resource_type, resource_id)
        elif args == "remove_note":
            return self.remove_note(request, resource_type, resource_id)
        elif args.startswith("transition"):
            t_name = args.split("/")[1]
            allowed_transitions = get_allowed_transitions(request.resource, request.user)
            t = Transition.objects.get(name__iexact=t_name, workflow=request.resource.workflow)
            if t in allowed_transitions:
                do_transition(request.resource, t, request.user)
                return HttpResponse('<div id="response" resource_type="%s" resource_id="%s" class="success">ok</div>' % (request.resource.resource_type, request.resource.id))
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
            
            #print "DETTAGLIO PRE: ", type(c)
            
            if isinstance(display_field, types.StringTypes) or isinstance(display_field, types.UnicodeType):
                element_type  = 'str'
                display_field= res._meta.get_field(display_field)
                
            element_value = getattr(res, display_field.name)
            if element_value != None:

                if isinstance(display_field, ResourceList):
                    element_type  = 'resourcelist'
                elif isinstance(element_value, Resource):
                    element_type = 'resource'
                elif isinstance(display_field, models.EmailField):
                    element_type  = 'email'
                else: 
                    element_type  = 'str'
                    if display_field.choices:
                        #TODO: set value to display value. 
                        # element_value = 
                        pass 
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
        user_actions = self._get_user_actions(request)
            
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
        
        basedir = os.path.join(settings.MEDIA_URL, "nui", "img", settings.THEME)
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
        
