from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin, messages
from django.core import urlresolvers
from django import forms

from gasistafelice.base import models as base_models
from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models

########################## Inlines #######################
class GASMemberInline(admin.TabularInline):
    model = gas_models.GASMember
    extra = 0
    exclude = ('account', 'available_for_roles')
    verbose_name = _("GAS membership")
    verbose_name_plural = _("GAS memberships")

class GASMemberOrderInline(admin.TabularInline):
    model = gas_models.GASMemberOrder
    extra = 1

class SupplierStockInline(admin.TabularInline):
    model = supplier_models.SupplierStock
    exclude = ('delivery_terms',)
    
class GASSupplierOrderProductInline(admin.TabularInline):
    model = gas_models.GASSupplierOrderProduct
    extra = 1

########################## ModelAdmin customizations ######

class PersonAdmin(admin.ModelAdmin):
    inlines = [GASMemberInline, ] 

    save_on_top = True
    
    list_display = ('__unicode__', 'name', 'surname', 'city', 'display_name')
    list_editable = ('name', 'surname') 
    list_display_links = ('__unicode__', 'display_name')
    search_fields = ('^name','^surname', 'address__city')
    
class PlaceForm(forms.ModelForm):

    class Meta:
        model = base_models.Place

    def clean_address(self):
        if not self.cleaned_data["name"]:
            if not self.cleaned_data["address"]:
                raise forms.ValidationError("Name field and Address field cannot be empty at the same time. Please set at least one of them.")
                
        return self.cleaned_data["address"]

class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm

    save_on_top = True 
    fieldsets = ((None,
            { 'fields' : ('name', 
                'description', 'address', 
                'zipcode', 'city', 'province'
            )
    }),
    ("Geotagging", {
        'fields' : ('lat','lon'),
        'classes': ('collapse',)
    }),
    )

    list_display = ('__unicode__', 'name', 'city', 'province')
    list_editable = ('city', 'province') 
    search_fields = ('name', 'city','province')


#class GASConfigAdmin(admin.ModelAdmin):
#    pass

class GASAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('__unicode__', 'id_in_des', 'city', 'email_gas', 'website_with_link', 'economic_state')
    fieldsets = (('Identity',
            { 'fields' : ('name', 'id_in_des', 'email_gas', 'logo', 'headquarter', 'description')
    }),
    (_("Configuration"), {
        'fields' : ('can_change_price', 'show_order_by_supplier', 'default_close_day', 'default_close_time', 'default_delivery_day', 'default_delivery_time', 'use_single_delivery', 'use_headquarter_as_withdrawal', 'is_active', 'use_scheduler'),
        'classes': ('collapse',)
    }),
    ("Economic", {
        'fields' : ('membership_fee', 'account', 'liquidity'),
        'classes': ('collapse',)
    }),
    )
    inlines = [ GASMemberInline, ]
    search_fields = ('^name', '^id_in_des','email_gas', 'headquarter__city')

    def website_with_link(self, obj):
        url = obj.website
        return u'<a target="_blank" href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"


class GASMemberAdmin(admin.ModelAdmin):

    save_on_top = True
    
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


class SupplierAdmin(admin.ModelAdmin):
    inlines = [SupplierStockInline, ]

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
        return u'<a target="_blank" href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"


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



class GASSupplierOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : (
                'gas',
                'supplier', 
                ('date_start', 'date_end'),   
                'delivery',  
                'withdrawal',              
              )
            }),
    )
    
    inlines = [GASSupplierOrderProductInline, ]
    

class GASSupplierOrderProductAdmin(admin.ModelAdmin):
    pass


class GASMemberOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : (
            'purchaser',
            'product',
            'ordered_price',
            'ordered_amount',
            'withdrawn_amount',          
              )  
            }),
    )
  
    
class DeliveryAdmin(admin.ModelAdmin):
    pass

class WithdrawalAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(base_models.Person, PersonAdmin)
admin.site.register(base_models.Place, PlaceAdmin)

admin.site.register(supplier_models.Supplier, SupplierAdmin)
admin.site.register(supplier_models.Product, ProductAdmin)
admin.site.register(supplier_models.ProductCategory)
admin.site.register(supplier_models.SupplierStock, SupplierStockAdmin)

admin.site.register(gas_models.GASMember, GASMemberAdmin)
admin.site.register(gas_models.GAS, GASAdmin)
admin.site.register(gas_models.order.GASSupplierStock)
admin.site.register(gas_models.order.GASSupplierOrder, GASSupplierOrderAdmin)
admin.site.register(gas_models.order.GASSupplierOrderProduct, GASSupplierOrderProductAdmin)
admin.site.register(gas_models.order.GASMemberOrder, GASMemberOrderAdmin)
admin.site.register(gas_models.order.Delivery, DeliveryAdmin)
admin.site.register(gas_models.order.Withdrawal, WithdrawalAdmin)

