from django.contrib import admin, messages
from django.utils.translation import ugettext, ugettext_lazy as _

from gasistafelice.base import models as base_models
from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models
from django.core import urlresolvers

class GASMemberAdminInline(admin.TabularInline):
    model = gas_models.GASMember

#class PlaceAdmin(admin.ModelAdmin):

class PersonAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'surname', 'city', 'display_name')
    list_editable = ('name', 'surname') #, 'display_name', 'uuid')
    list_display_links = ('__unicode__', 'display_name')


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

    class Media:
        css = {
            "all": ("css/addchangestyles.css",)
        }
        js = ("js/addchangecode.js",)

    
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
                # FIXME: Delivery and Withdrawal info is encapsulated in specific models, now!   
                ('delivery_date', 'delivery_place'), 
                ('withdraw_date', 'withdraw_place'), 
                'product_set'
              )
            }),
    )

class GASSupplierOrderProductAdmin(admin.ModelAdmin):
    pass

class GASMemberOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : ('supplier', 
                ('date_start', 'date_end'),
                # FIXME: Delivery and Withdrawal info is encapsulated in specific models, now!   
                ('delivery_date', 'delivery_place'), 
                ('withdraw_date', 'withdraw_place'), 
                'product_set'
              )
            }),
    )

    
class ProductAdmin(admin.ModelAdmin):

    save_on_top = True
    
    fieldsets = (
        (None, {
            'fields': ('name', 'producer', 'description','category','mu')
        }),
        )

    list_display = ('name', 'producer', 'category', 'description',)
    list_display_links = ('name',)
    list_filter = ('producer', 'category')
    search_fields = ['name', 'producer__name', 'description']


class SupplierAdmin(admin.ModelAdmin):

    save_on_top = True
    
    fieldsets = (
        (None, {
            'fields': ('name', 'seat', 'website',)
        }),
        ('Details', {
            'fields': ('flavour', 'vat_number','certifications',)
        }),        
        )

    list_display = ('name', 'flavour', 'website_with_link',)
    list_display_links = ('name',)
    list_filter = ('flavour',)
    search_fields = ['name', 'referrers__name', 'referrers__surname',]
    
    def website_with_link(self, obj):
        url = obj.website
        return u'<a href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"


class SupplierStockAdmin(admin.ModelAdmin):

    save_on_top = True
    
    fieldsets = (
        (None, {
            'fields': ('product', 'supplier', 'price', 'amount_available',)
        }),
        ('Constraints', {
            'classes': ('collapse',),
            'fields': ('order_minimum_amount', 'order_step', 'delivery_terms',)
         })
        )

    list_display = ('product','supplier', 'price_pretty', 'amount_avail_pretty', 'order_min_amount_pretty', 'order_step_pretty',)
    list_display_links = ('product',)
    list_filter = ('supplier',)
    search_fields = ['product', 'supplier__name',]
    
    # FIXME: try to make it more generic !
    def order_min_amount_pretty(self, obj):
        return obj.order_minimum_amount or '--'
    order_min_amount_pretty.short_description = "minimum amount"
    
    # FIXME: try to make it more generic !
    def order_step_pretty(self, obj):
        return obj.order_step or '--'
    order_step_pretty.short_description = "increment step"
    
    def amount_avail_pretty(self, obj):
        if obj.amount_available == ALWAYS_AVAILABLE:
            return 'infinity'
    amount_avail_pretty.short_description = 'amount available'
    
    # FIXME: try to make it more generic !
    # TODO: 'euro' should be rendered as a currency symbol 
    def price_pretty(self, obj):
        return str(obj.price) + ' euro'
    price_pretty.short_description = "price"
    
admin.site.register(base_models.Person)

admin.site.register(supplier_models.Supplier, SupplierAdmin)
admin.site.register(supplier_models.Product, ProductAdmin)
admin.site.register(supplier_models.ProductCategory)
admin.site.register(supplier_models.SupplierStock, SupplierStockAdmin)
admin.site.register(gas_models.GASMember, GASMemberAdmin)
admin.site.register(gas_models.GAS, GASAdmin)
admin.site.register(gas_models.order.GASSupplierStock)
admin.site.register(gas_models.order.GASSupplierOrder) #, GASSupplierOrderAdmin)
admin.site.register(gas_models.order.GASSupplierOrderProduct, GASSupplierOrderProductAdmin)
admin.site.register(gas_models.order.GASMemberOrder)
