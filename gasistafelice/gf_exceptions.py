# -*- coding: utf-8 -*-

from django.core import exceptions

class NoSenseException(Exception):
    pass

class InvalidStateException(Exception):
    pass

class DatabaseInconsistent(Exception):
    pass

class ReferrerIsNoneException(exceptions.PermissionDenied):

    def __unicode__():
        return u"Non è possibile creare un ordine senza referente" 
