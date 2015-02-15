from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^suppliers/$', 'gdxp.views.suppliers'),

    #(r'^supplierstock/(?P<stock_id>[0-9]+)/$', 'rdf_gf.views.show_supplier_stock'),
    #(r'^supplierstock/(?P<stock_id>[0-9]+)/catalog/$', 'rdf_gf.views.show_catalog_from_product'),
)
