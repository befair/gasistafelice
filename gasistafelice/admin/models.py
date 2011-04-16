from django.contrib import admin, messages
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base import models as base_models
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models
from django.core import urlresolvers

class GASMemberAdminInline(admin.TabularInline):
    model = gas_models.GASMember

class GASAdmin(admin.ModelAdmin):
    inlines = [ GASMemberAdminInline, ]

class GASMemberAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gas_with_link')
    fieldsets = ((None,
            { 'fields' : ('gas', 'person')
    }),
    ("Extra", {
        'fields' : ('available_for_roles','roles'),
        'classes': ('collapse',)
    }),
    )
    filter_horizontal = ('roles',)
    search_fields = ('person__name','person__surname')
    list_filter = ('gas', 'roles')

    actions = ['say_hello']

    def say_hello(self, request, queryset):
        for obj in queryset.all():
            messages.info(request, ugettext("Hello %s") % obj)
    say_hello.short_description = _("Say hello to gas members")

    def gas_with_link(self, obj):
        url = urlresolvers.reverse('admin:gas_gas_change', args=(obj.gas.id,))
        return u'<a href="%s">%s</a>' % (url, obj.gas)
    gas_with_link.allow_tags = True
    gas_with_link.short_description = "GAS"

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
admin.site.register(gas_models.GAS, GASAdmin)
admin.site.register(gas_models.order.GASSupplierStock)
admin.site.register(gas_models.order.GASSupplierOrder) #, GASSupplierOrderAdmin)

