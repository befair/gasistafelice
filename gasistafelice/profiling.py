import hotshot
import os
import time
import settings
from functools import wraps

try:
    PROFILE_LOG_BASE = settings.PROFILE_LOG_BASE
except:
    PROFILE_LOG_BASE = "/tmp"


def profile(log_file):
    """Profile some callable.

This decorator uses the hotshot profiler to profile some callable (like
a view function or method) and dumps the profile data for later processing 
and examination.

It takes one argument, the profile log name, which is joined to the end 
of the path 'gasistafelice/profiling_logs' (this absolute path is, however,  
defined by PROFILE_LOG_BASE in default_settings.py. 
It also inserts a time stamp into the file name, such that 'my_view.prof' 
become 'my_view-20100211T170321.prof',where the time stamp is in UTC. 
This makes it easy to run and compare multiple trials.
"""

    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(function):
        def _inner(request,*args, **kwargs):
            # Add a timestamp to the profile output when the callable
            # is actually called.
            (base, ext) = os.path.splitext(log_file)
            if ext == '':
                ext = '.prof'    
            base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
            final_log_file = base + ext

            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(function, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return wraps(function)(_inner)
    return _outer
