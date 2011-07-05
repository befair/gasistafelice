 
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


from django.template import loader
from django.shortcuts import *
from django.template import RequestContext

from http import SVGHttpResponse, XMLHttpResponse

def render_to_svg_response(*args, **kwargs):
    return SVGHttpResponse(loader.render_to_string(*args, **kwargs))

def render_to_xml_response(*args, **kwargs):
    return XMLHttpResponse(loader.render_to_string(*args, **kwargs))

def render_to_context_response(request, template, context={}):
    return render_to_response(template, context, context_instance=RequestContext(request))
