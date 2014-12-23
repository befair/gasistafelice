from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response

from supplier.models import Supplier

from django.core.exceptions import FieldError

def suppliers(request):
    """ 
    GDXP API

    suppliers?<key>=<value>*&<option>=<True | other>*
    
    Options are:

    - opt_catalog
    - opt_order
     
    """

    qs_filter = request.GET.copy() 

    if not qs_filter:
        return HttpResponse('imposta un filtro')

    supplier_qs = Supplier.objects.all()
    options = {}

    for k,values in qs_filter.iterlists(): 
        for v in values:
            try:
                is_opt = k.startswith('opt')
            except AttributeError as e:
                is_opt = False
                
            if not is_opt:
                try:
                    supplier_qs = supplier_qs.filter(**{k : v})
                except FieldError as e:
                    pass
            else:
                options.update({k : v})

    if not supplier_qs:
        return HttpResponse('da ritornare un 404 not found')

    gdxp_version = 'v0_2'
    return render_to_xml_response(
        'gdxp/%s/base.xml' % gdxp_version, {'qs' : supplier_qs, 'opts' : options}
    )

