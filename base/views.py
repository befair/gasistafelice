# Create your views here.

def product_update(request, product_id):
    p = get_object_or_404(pk=product_id)
    if (request.user.has_perm(const.SUPPLIER_REFERRER, p))
        context = {}
    return 
