from rest.views.blocks.base import BlockWithList
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "catalog_list"
    BLOCK_DESCRIPTION = _("Lista prodotti supplier/gas in ordine")
    BLOCK_VALID_RESOURCE_TYPES = ["site", "gas", "supplier", "gasmember"]

    def _get_resource_list(self, request):
        return request.resource.catalogs

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
        
