from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response

def suppliers(request):

    pk = request.GET.get('pk')

    if not pk:
        return HttpResponse('mettici pk')

    kw = { 'pk' : pk }
    supplier_qs = Supplier.objects.filter(**kw)

    if not supplier_qs:
        return HttpResponse('da ritornare un 404 not found')

    gdxp_version = 'v0_2'
    return render_to_xml_response(
        'gdxp/%s/base.xml' % gdxp_version, context={'qs' : supplier_qs}
    )
