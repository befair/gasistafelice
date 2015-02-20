from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from rest.views.blocks import AbstractBlock
from rest.views.contextmenu import get_context_menu
        

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(AbstractBlock):
    
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def __init__(self):
        super(Block, self).__init__()
        
        self.name = "menu"        
        self.description = _("Context menu")
    
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def is_valid(self, resource_type):
        """
        Returns true if the block is valid for the given resource_type
        """
        return True
        
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def visible_in_page(self):
        return False
        
    #------------------------------------------------------------------------------#
    #                                                                              #
    #------------------------------------------------------------------------------#
    
    def get_response(self, request, resource_type, resource_id, args):
        
        return get_context_menu(request)
