 
# Copyright (C) 2008 Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of SANET
# SANET is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# SANET is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SANET. If not, see <http://www.gnu.org/licenses/>.


from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.db import models
from django.http import *
from django.utils import simplejson

#from email.Header import Header

#------------------------------------------------------------------------------
# Json Facilities

class MyJSONEncoder(DjangoJSONEncoder):
	def default(self, o):
		if isinstance(o, models.Model):
			return o.toJson()
		else:
			return super(MyJSONEncoder, self).default(o)

class JsonResponse(HttpResponse):
	def __init__(self, object):
		if isinstance(object, QuerySet):
			try:
				object = map(lambda x : x.toJson() , object)
				content = simplejson.dumps(object, ensure_ascii=False, cls=MyJSONEncoder)
			except:
				content = serialize('json', object)
		else:
			content = simplejson.dumps(object, ensure_ascii=False, cls=MyJSONEncoder)
		super(JsonResponse, self).__init__(content, mimetype='application/json')

#------------------------------------------------------------------------------

class SVGHttpResponse(HttpResponse):
	def __init__(self, *args, **kw):
		kw['mimetype']="image/svg+xml"
		HttpResponse.__init__(self, *args, **kw)

#------------------------------------------------------------------------------

class XMLHttpResponse(HttpResponse):
	def __init__(self, *args, **kw):
		kw['mimetype']="text/xml"
		HttpResponse.__init__(self, *args, **kw)

#------------------------------------------------------------------------------

class HttpResponseWithXJSONMessages(HttpResponse):
	def __init__(self, request, *args, **kw):
		HttpResponse.__init__(self, *args, **kw)
		messages = request.user.get_and_delete_messages()
		jsoned = simplejson.dumps({ 'user_messages' : messages })
		#TODO: Javascription X-JSON evaluation does not support quoting, support it !!!
		#jsoned = str(Header(jsoned, 'iso-8859-1'))
		self['X-JSON'] = jsoned

