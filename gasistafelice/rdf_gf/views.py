from django.http import HttpResponse
from supplier.models import SupplierStock, Supplier
from gasistafelice.lib.shortcuts import render_to_xml_response
import rdfxmlutils as utils

from gasistafelice.lib.http import XMLHttpResponse


def show_supplier_stock(request, stock_id):
    """ Show rdf/xml representation of a product into a supplier catalog """ 
    stock = SupplierStock.objects.get(pk=stock_id)

    rdfxml = utils.build_rdfxml(request.get_full_path(),
        stock
    )

    return XMLHttpResponse(rdfxml)

def show_catalog_from_product(request, stock_id):
    """ Show rdf/xml representation of a catalog, starting from a product """ 
    
    stock = SupplierStock.objects.get(pk=stock_id)

    catalog = stock.parent.stock_set.iterator()

    sup = set()
    suppliers = []
    stocks = []
    products = []
    i = 1

    for stock in catalog:
        sup.add(stock.supplier)
        sup.add(stock.producer)
        sup.add(stock.product.producer)
        stocks.append([stock, i])
        products.append([stock.product, i])

        i += 1

    i = 1
    for s in sup:
        suppliers.append([s, i])
        i += 1
        
    rdfxml = utils.build_rdfxml(request.get_full_path(),
        None, 
        stocks=stocks, 
        suppliers=suppliers,
        products=products
    )

    return XMLHttpResponse(rdfxml)
    

def show_supplier(request, supplier_id):
    """ Show rdf/xml representation of a supplier """ 
    
    supplier = Supplier.objects.get(pk=supplier_id)

    rdfxml = utils.build_rdfxml(request.get_full_path(),
        supplier
    )

    return XMLHttpResponse(rdfxml)
