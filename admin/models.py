from django.contrib import admin
from django.db import models

from gasistafelice.base import models as base_models

class GASUserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gas')
    fieldsets = ((None,
            { 'fields' : ('gas', ('name', 'surname'), 'uuid')
    }),
    )

class SupplierOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : ('supplier', 
                ('date_start', 'date_end'), 
                ('delivery_date', 'delivery_place'), 
                ('withdrawal_date', 'withdrawal_place'), 
                'product_set'
              )
            }),
    )
    
admin.site.register(base_models.Person)
admin.site.register(base_models.GASUser, GASUserAdmin)
admin.site.register(base_models.GAS)

admin.site.register(base_models.Supplier)
admin.site.register(base_models.Product)
admin.site.register(base_models.ProductCategory)
admin.site.register(base_models.SupplierStock)
admin.site.register(base_models.SupplierStockGAS)
admin.site.register(base_models.SupplierOrder, SupplierOrderAdmin)


