import os

from lib import load_symbol

from django.conf import settings
import logging
log = logging.getLogger(__name__)
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def load_symbols_from_dir(dir, lib, cname):
    ddir = []

    modules_dir = settings.BASE_DIR + dir

    files = os.listdir(modules_dir)
    for filename in files:
        
        if not filename.endswith('.py'): continue   #ignore not python sources
        if filename.startswith('__init__'): continue   #ignore __init__

        mod_name = filename[:-3]              # remove '.py'
        # dynamic load of expression symbols (like dlopen(), dlsym() )
        mod_symbol = load_symbol('%s.%s.%s' % (lib, mod_name, cname))
        ddir.append([mod_name,mod_symbol])
        
    return ddir
    
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

def load_block_handler(block_name, module_base='rest'):
    class_path = "%s.views.blocks.%s.Block" % (module_base, block_name)
    #log.debug("load_block_handler(%s,%s)=%s" % (block_name,module_base,class_path));
    handler =load_symbol(class_path)()
    
    return handler
