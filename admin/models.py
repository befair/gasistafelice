from django.contrib import admin
from django.db import models

from gasistafelice.base import models as base_models
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models

class GASMemberAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gas')
    fieldsets = ((None,
            { 'fields' : ('gas',)
    }),
    )

class GASSupplierOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : ('supplier', 
                ('date_start', 'date_end'), 
                ('delivery_date', 'delivery_place'), 
                ('withdraw_date', 'withdraw_place'), 
                'product_set'
              )
            }),
    )
    
admin.site.register(base_models.Person)

admin.site.register(supplier_models.Supplier)
admin.site.register(supplier_models.Product)
admin.site.register(supplier_models.ProductCategory)
admin.site.register(supplier_models.SupplierStock)
admin.site.register(gas_models.GASMember, GASMemberAdmin)
admin.site.register(gas_models.GAS)
#admin.site.register(gas_models.order.GASSupplierStock)
#admin.site.register(gas_models.order.GASSupplierOrder, GASSupplierOrderAdmin)

