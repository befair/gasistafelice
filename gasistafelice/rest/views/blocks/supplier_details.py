"""View for block details specialized for a GAS"""

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core.urlresolvers import reverse
from django.conf import settings

from flexi_auth.models import ObjectWithContext
from ajax_select.fields import autoselect_fields_check_can_add

from gasistafelice.consts import EDIT

from gasistafelice.rest.views.blocks.base import ResourceBlockAction, EXPORT_GDXP
from gasistafelice.rest.views.blocks import details
from gasistafelice.supplier.models import Supplier

from gasistafelice.lib.shortcuts import render_to_context_response

from gasistafelice.supplier.forms import EditSupplierForm, SupplierRoleForm

from gdxp.views import suppliers

import logging
log = logging.getLogger(__name__)

class Block(details.Block):

    BLOCK_NAME = "supplier_details"
    BLOCK_VALID_RESOURCE_TYPES = ["supplier"]
    FORMCLASS_MANAGE_ROLES = SupplierRoleForm

    def _get_user_actions(self, request):
        """Who can edit Supplier informations, has also the ability to configure it."""

        user_actions = super(Block, self)._get_user_actions(request)

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            
            act_configure = ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="configure", verbose_name=_("Configure"),
                    popup_form=True,
                    url = reverse('admin:supplier_supplierconfig_change', args=(request.resource.config.pk,))
            )

            #gdxp_export = ResourceBlockAction(
            #        block_name = self.BLOCK_NAME,
            #        resource = request.resource,
            #        name="export", verbose_name=_("Export"),
            #        popup_form=False,
            #        url = "%s?%s" % (reverse('gdxp.views.suppliers'), "pk=%s&opt_catalog=0&opt_download=1" % request.resource.pk),
            #        method="GET"
            #)
            #user_actions.insert(0, gdxp_export)

            for i,act in enumerate(user_actions):
                # Change URL for action EDIT, insert "configure" action
                if act.name == EDIT:
#                   act.url = reverse('admin:supplier_supplier_change', args=(request.resource.pk,)) 
                   user_actions.insert(i+1, act_configure)
                   break
                   
            user_actions += [
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name="export", verbose_name=_("Export"),
                    popup_form=False,
                    #MATTEO
                    #WAS: url = "%s?%s" % (reverse('gdxp.views.suppliers'), "pk=%s&opt_catalog=0&opt_download=1" % request.resource.pk),
                    #method="GET"
                ),
            ]

        return user_actions

    def _get_edit_form_class(self):
        form_class = EditSupplierForm
        autoselect_fields_check_can_add(form_class, Supplier, self.request.user)
        return form_class


    def get_response(self, request, resource_type, resource_id, args):
        """ MATTEO """

        self.request = request
        self.resource = resource = request.resource

        if args == EXPORT_GDXP:
            #MATTEO
            #WAS:request.META['QUERY_STRING'] = "pk=%s&opt_catalog=0&opt_download=1" % request.resource.pk
            #WAS:request.META['PATH_INFO'] = reverse('gdxp.views.suppliers')
            #WAS:return suppliers(request)
            return HttpResponseRedirect("%s?%s" % (reverse('gdxp.views.suppliers'), "pk=%s&opt_catalog=0&opt_download=1" % request.resource.pk))
        else:
            return super(Block, self).get_response(request, resource_type, resource_id, args)

