from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response

from supplier.models import Supplier

from django.core.exceptions import FieldError

from django.core.servers.basehttp import FileWrapper

import urllib

def suppliers(request):
    """ 
    GDXP API

    suppliers?<key>=<value>*&opt_<option>=<0|1>*
    
    Options are:

    - catalog
    - order
    - download
     
    """

    # If querystring is empty return all suppliers and catalogs
    supplier_qs = Supplier.objects.all()
    options = {
        'opt_catalog' : True,
        'opt_order' : False,
        'opt_download' : False,
    }

    qs_filter = request.GET.copy() 
    for k,values in qs_filter.iterlists(): 
        for v in values:

            if k.startswith('opt_'):
                options.update({k : bool(int(v))})
            else:

                if k.endswith('__in'):
                    v = v.split(',')
                
                try:
                    supplier_qs = supplier_qs.filter(**{k : v})
                except FieldError as e:
                    return HttpResponse('<h1>Request parameter is not supported</h1>', status=400, content_type='text/xml')

    if not supplier_qs:
        return HttpResponse('<h1>No supplier found for the requested filter</h1>', status=404, content_type='text/xml')

    gdxp_version = 'v0_2'

    xml_response = render_to_xml_response(
        'gdxp/%s/base.xml' % gdxp_version, {'qs' : supplier_qs, 'opts' : options}
    )

    fname = u"GF_%s.gdxp" % urllib.quote_plus(
        u"_".join(map(unicode, supplier_qs)).encode('latin-1')
    )
    xml_response['Content-Disposition'] = "attachment; filename=%s" % fname
    return xml_response

