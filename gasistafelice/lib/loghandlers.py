#!/usr/bin/env python

import logging, os
import logging.handlers, logging.config

class GroupWriteRotatingFileHandler(logging.handlers.RotatingFileHandler):    

    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """

        fstat = os.stat(self.baseFilename)
        curr_gid = fstat.st_gid
        curr_uid = fstat.st_uid

        # Rotate the file first.
        logging.handlers.RotatingFileHandler.doRollover(self)

        # Change group to the current permissions.
        os.chown(self.baseFilename, curr_uid, curr_gid)

    def _open(self):
        prevumask=os.umask(0o002)
        #os.fdopen(os.open('/path/to/file', os.O_WRONLY, 0600))
        rtv=logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv


if __name__ == "__main__":

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    LOG_FILE = os.path.join(PROJECT_ROOT, 'handlertest.log')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
            },
            'logfile_debug':{
                'level':'DEBUG',
                'class':'loghandlers.GroupWriteRotatingFileHandler',
                'filename': LOG_FILE,
                'maxBytes': 1024, #TEST SMALL VALUE
                'backupCount' : 10,
            },
        },
        'loggers': {
            'default': {
                'handlers': ['console', 'logfile_debug'],
                'level': 'DEBUG',
            }
        }
    }

    logging.config.dictConfig(LOGGING)

    c = 0
    while c < 2050:
        msg = 'writing some debug data %s'
        log = logging.getLogger('default')
        log.warning(msg, c)
        c += len(msg)

    print("Check %s log file" % LOG_FILE)
