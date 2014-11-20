# This code has been taken from http://www.assembla.com/spaces/datatables_demo/wiki 

from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers

import os, json
from django.conf import settings

import logging, traceback

log = logging.getLogger(__name__) 

#TODO: Fero def prepare_datatables_list
def prepare_datatables_queryset(request, querySet, columnIndexNameMap, *args):
    """
    Retrieve querySet to be displayed in datatables..

    Usage: 
        querySet: query set to draw data from.
        columnIndexNameMap: field names in order to be displayed.

    Return a tuple:
        querySet: data to be displayed after this request
        datatables parameters: a dict which includes
            - iTotalRecords: total data before filtering
            - iTotalDisplayRecords: total data after filtering
    """
    try:
        iTotalRecords = querySet.count() #count how many records are in queryset before matching final criteria
    except:
        return prepare_datatables_list(request, querySet, columnIndexNameMap, *args)

    cols = int(request.GET.get('iColumns',0)) # Get the number of columns
    iDisplayLength =  min(int(request.GET.get('iDisplayLength',10)),100)     #Safety measure. If someone messes with iDisplayLength manually, we clip it to the max value of 100.
    startRecord = int(request.GET.get('iDisplayStart',0)) # Where the data starts from (page)
    endRecord = startRecord + iDisplayLength  # where the data ends (end of page)
    
    # Ordering data
    iSortingCols =  int(request.GET.get('iSortingCols',0))
    asortingCols = []
        
    if iSortingCols:
        for sortedColIndex in range(0, iSortingCols):
            sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
            if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  # make sure the column is sortable first
                sortedColName = columnIndexNameMap[sortedColID]
                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                asortingCols.append(sortedColName) 
        querySet = querySet.order_by(*asortingCols)

    # Determine which columns are searchable
    searchableColumns = []
    for col in range(0,cols):
        if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])

    # Apply filtering by value sent by user
    customSearch = request.GET.get('sSearch', '').encode('utf-8');
    if customSearch != '':
        outputQ = None
        first = True
        for searchableColumn in searchableColumns:
            kwargz = {searchableColumn+"__icontains" : customSearch}
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)        
        querySet = querySet.filter(outputQ)

    # Individual column search 
    outputQ = None
    for col in range(0,cols):
        if request.GET.get('sSearch_{0}'.format(col), False) > '' and request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
            kwargz = {columnIndexNameMap[col]+"__icontains" : request.GET['sSearch_{0}'.format(col)]}
            outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
    if outputQ: querySet = querySet.filter(outputQ)
        
    iTotalDisplayRecords = querySet.count() #count how many records match the final criteria
    if endRecord > startRecord:
        querySet = querySet[startRecord:endRecord] #get the slice

    return querySet, {
        'iTotalRecords' : iTotalRecords,
        'iTotalDisplayRecords' : iTotalDisplayRecords,
    }

def prepare_datatables_list(request, queryList, columnIndexNameMap, *args):
    """
    Retrieve list of objects to be displayed in datatables..

    Usage: 
        queryList: raw list of objects set to draw data from.
        columnIndexNameMap: field names in order to be displayed.

    Return a tuple:
        queryList: data to be displayed after this request
        datatables parameters: a dict which includes
            - iTotalRecords: total data before filtering
            - iTotalDisplayRecords: total data after filtering
    """
    iTotalRecords = len(queryList)

    # Ordering data

    # Determine which columns are searchable

    # Apply filtering by value sent by user

    # Individual column search 

    return queryList, {
        'iTotalRecords' : iTotalRecords,
        'iTotalDisplayRecords' : iTotalRecords,
    }

def render_datatables(request, records, dt_params, jsonTemplatePath, moreData=None):

    """
    Render datatables..

    Usage: 
        querySet: query set to draw data from.
        dt_params: encapsulate datatables parameters. DataTables reference: http://www.datatables.net/ref
        jsonTemplatePath: template file to generate custom json from.
    """

    sEcho = int(request.GET.get('sEcho',0)) # required echo response
    iTotalRecords = dt_params["iTotalRecords"]
    iTotalDisplayRecords = dt_params["iTotalDisplayRecords"]
    
    jstonString = render_to_string(jsonTemplatePath, locals()) #prepare the JSON with the response, consider using : from django.template.defaultfilters import escapejs
    response = HttpResponse(jstonString, content_type="application/javascript")

    #prevent from caching datatables result
    add_never_cache_headers(response)
    return response


def render_datatables_automagic(request, querySet, columnIndexNameMap, iTotalRecords, iTotalDisplayRecords, moreData=None):
    """
    Render datatables..

    Usage: 
        querySet: query set to draw data from.
        dt_params: encapsulate datatables parameters. DataTables reference: http://www.datatables.net/ref
        columnIndexNameMap: field names in order to be displayed.

    other parameters follows datatables specifications: http://www.datatables.net/ref
    """

    sEcho = int(request.GET.get('sEcho',0)) # required echo response
    
    # Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))
    
    aaData = []
    a = querySet.values() 
    for row in a:
        rowkeys = row.keys()
        rowvalues = row.values()
        rowlist = []
        for col in range(0,len(colitems)):
            for idx, val in enumerate(rowkeys):
                if val == colitems[col]:
                    rowlist.append(str(rowvalues[idx]))
        aaData.append(rowlist)
    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})

    response_dict.update({'moreData':moreData})

    response =  HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    #prevent from caching datatables result
    add_never_cache_headers(response)
    return response




#Needed to insert images in report

def pisa_fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

#------------------------------------------------------------------------------

# Author: Luca Ferroni
# License: AGPLv3

from django.contrib.admin import helpers
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.template import Template
from django.template.response import TemplateResponse

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Naive implementation to be tuned as data protocol exchange for Ajax requests
template_success = Template("""
    <div id="response" class="success" {{ extra_attrs }}>{{ msg }}</div>
""")

template_error = Template("""
    <div id="response" class="error" {{ extra_attrs }}>{{ msg }}</div>
""")

HTTP_ERROR_INTERNAL = 505
HTTP_SUCCESS = 200
HTTP_REDIRECT = 302

def response_error(request, msg="error", on_complete=""):
    context = { 
        'msg' : msg,
        'http_status_code' : HTTP_ERROR_INTERNAL,
        'exception_type' : type(msg),
        'exception_msg' : unicode(msg),
    }
    if on_complete:
        context['extra_attrs'] = 'on_complete="%s"' % on_complete
    return TemplateResponse(request, template_error, context)

def response_success(request, msg="ok", on_complete=""):
    context = { 
        'msg' : msg,
        'http_status_code' : HTTP_SUCCESS,
    }
    if on_complete:
        context['extra_attrs'] = 'on_complete="%s"' % on_complete
    return TemplateResponse(request, template_success, context)

def response_redirect(request, url):
    context = { 
        'http_status_code' : HTTP_REDIRECT,
    }
    return TemplateResponse(request, template_success, context)

#--------------------------------------------------------------------------------

class ResponseWrappedView(View):
    """Wrap the dispatcher in order to apply Ajax protocol for data exchange.

    Used also as entry point for logging.

    Now can be implemented also as a Middleware. 
    Let's see if we need some more customization or not...
    """

    def dispatch(self, request, *args, **kwargs):

        view_name = self.__class__.__name__.lower()
        method = request.method.upper()
        log.debug("%s:%s user %s args=%s kw=%s" % (
            view_name, method, request.user, args, kwargs
        ))
        try:
            rv = super(ResponseWrappedView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            log.debug("%s:%s user %s exception raised %s tb=%s" % (
                view_name, method, request.user, e, traceback.format_exc()
            ))
            if request.is_ajax():
                rv = response_error(request, msg=e)
            else:
                raise
        return rv
        

class LoginRequiredView(ResponseWrappedView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)

