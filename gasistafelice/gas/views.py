from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db import transaction

from django.utils.decorators import method_decorator
from django.conf import settings

from gas.models.base import GAS
from gas.forms.base import BaseGASForm

from lib import views_support

import exceptions
import logging, datetime

log = logging.getLogger(__name__)



class GASDetailView(DetailView, views_support.LoginRequiredView):
    """ List the details of a GAS """

    model = GAS
    template_name="gas/detail.html"

    def get_object(self):
        self.instance = super(GASDetailView, self).get_object()
        return self.instance

    def get_context_data(self, **kwargs):
        context = super(GASDetailView, self).get_context_data(**kwargs)
        # needs to do something here...?
        from django.contrib.sites.models import get_current_site

        return context

class GASCreateView(CreateView):
    """ Create a GAS from ModelForm """

    form_class = BaseGASForm
    template_name = "gas/create.html"
    
    def get_form(self, form_class):

        # Override default get_form() in order to pass "request" correctly
        form = form_class(self.request, **self.get_form_kwargs())
        return form

    @transaction.commit_on_success
    def form_valid(self, form):

        form.save()
        success_url = GAS.get_absolute_url()
        return views_support.response_redirect(self.request, success_url)

class GASUpdateView(UpdateView, views_support.LoginRequiredView):
    """ Update a GAS """
    
    form_class = BaseGASForm
    model = GAS
    template_name = "gas/update.html"

    def get_form(self, form_class):

        # Override default get_form() in order to pass "request" correctly
        form = form_class(self.request, **self.get_form_kwargs())
        return form
    #def get_form_kwargs(self):
    #    kwargs = super(UpdateView, self).get_form_kwargs()
    #    #add kwarg here
    #    return kwargs
    
    @transaction.commit_on_success
    def form_valid(self, form):

        gas = self.get_object()
       
        #insert here user permissions check
 
        name = form.cleaned_data['name']
        id_in_des = form.cleaned_data['id_in_des']
        headquarter = form.cleaned_data['headquarter']
        description = form.cleaned_data['description']
        birthday = form.cleaned_data['birthday']
        #contact_set = form.cleaned_data['contact_set']
        #orders_email_contact = form.cleaned_data['']

        if gas:
            gas.name = name
       
        gas.save() 

        # Code to update a generic set of objects  
        #to_add, to_remove = self.update_values(old_categories, 
        #    new_categories
        #)
        #action.category_set.add(*to_add)
        #action.category_set.remove(*to_remove)

        #if form.cleaned_data['politician_set']:

        success_url = gas.get_absolute_url()
        return views_support.response_redirect(self.request, success_url)

    def update_values(self, old_values, new_values, attr='id'):
        """ Get two sets of values as input and return two sets of values as output.

        This can be used when receiving a set of objects of the same tipe from a form 
        to determine, knowing the old set of values, which objects have to be
        removed, which ones have to be added and which ones have to be kept.
        
        The outputted set contain respectively the objects to add and the objects
        to remove.
        """

        to_add = []
        to_remove = []
        count = 0
        values_new_length = len(new_values)

        for obj_new in new_values:
            to_add.append(obj_new)

        for obj_old in old_values:
            for obj_new in new_values:
                if obj_old.__getattribute__(attr) == obj_new.__getattribute__(attr):
                    #already present, does not need 
                    #to be added
                    to_add.remove(obj_new)
                    break
                else:
                    count = count + 1

            if values_new_length == count:
                #the old value is not present in the new set
                #of selected values
                to_remove.append(obj_old)

            count = 0
        
        return to_add, to_remove
