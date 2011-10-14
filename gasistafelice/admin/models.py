from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin, messages
from django.core import urlresolvers
from django import forms

from gasistafelice.base import models as base_models
from gasistafelice.base.const import ALWAYS_AVAILABLE
from gasistafelice.supplier import models as supplier_models
from gasistafelice.gas import models as gas_models
from flexi_auth import models as auth_models
from gasistafelice.rest.models import pages as rest_models
from gasistafelice.users import models as user_models

########################## Inlines #######################

class ContactInline(admin.TabularInline):
    model = base_models.Contact
    extra = 2

class GASMemberInline(admin.TabularInline):
    model = gas_models.GASMember
    extra = 0
    exclude = ('available_for_roles',)
    verbose_name = _("GAS membership")
    verbose_name_plural = _("GAS memberships")

class GASMemberOrderInline(admin.TabularInline):
    model = gas_models.GASMemberOrder
    extra = 1

class SupplierStockInline(admin.TabularInline):
    model = supplier_models.SupplierStock
    exclude = ('delivery_notes',)
    extra = 1
    
class GASSupplierOrderProductInline(admin.TabularInline):
    model = gas_models.GASSupplierOrderProduct
    extra = 10

from django.forms.models import BaseInlineFormSet
class GASMemberRoleFormset(BaseInlineFormSet):
    pass

class GASMemberRoleInline(admin.TabularInline):

    model = auth_models.ParamRole
    formset = GASMemberRoleFormset
    extra = 3

########################## ModelAdmin customizations ######

class PersonAdmin(admin.ModelAdmin):

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


class GASAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('__unicode__', 'id_in_des', 'city', 'website_with_link', 'economic_state')
    fieldsets = ((_('Identity'),
            { 'fields' : ('name', 'id_in_des', 'logo', 'headquarter', 'description', 'association_act', 'intent_act')
    }),
# COMMENT fero: Economic state is disabled right now
#    (_("Economic"), {
#        'fields' : ('membership_fee', 'account', 'liquidity'),
#        'classes': ('collapse',)
#    }),
    )
#    inlines = [ ContactInline, ]
    search_fields = ('^name', '^id_in_des', 'headquarter__city')

    def website_with_link(self, obj):
        url = obj.website
        return u'<a target="_blank" href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"

class GASConfigAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('default_close_day', 'order_show_only_next_delivery', 'order_show_only_one_at_a_time', 'default_delivery_day', 'is_active')
    fieldsets = ((_("Configuration"), {
        'fields' : ('order_show_only_next_delivery', 'order_show_only_one_at_a_time', 'gasmember_auto_confirm_order', 'default_close_day', 'default_close_time', 'default_delivery_day', 'default_delivery_time', 'can_change_delivery_place_on_each_order', 'default_delivery_place', 'can_change_withdrawal_place_on_each_order', 'default_withdrawal_place', 'is_active'),
    }),
    )

class GASMemberAdmin(admin.ModelAdmin):

    save_on_top = True
    
    list_display = ('__unicode__', 'gas_with_link')
    fieldsets = ((None,
            { 'fields' : ('gas', 'person')
    }),
    ("Extra", {
        'fields' : ('available_for_roles',),
        'classes': ('collapse',)
    }),
    )
    filter_horizontal = ('available_for_roles',)
    search_fields = ('person__name','person__surname')
    list_filter = ('gas', )

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
    # Disabled inlines = [SupplierStockInline, ]

    save_on_top = True
    
    fieldsets = (
        (None, {
            'fields': ('name', 'seat', 'website', 'logo')
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
            'fields': ('product', 'net_price', 'amount_available',)
        }),
        ('Constraints', {
            'classes': ('collapse',),
            'fields': ('units_minimum_amount', 'units_per_box', 'detail_minimum_amount', 'detail_step', 'delivery_notes',)
         })
        )

    list_display = ('supplier', 'product', 'net_price', 'amount_avail_pretty', 'units_minimum_amount_pretty', 'units_per_box_pretty',)
    list_editable = ('product', 'net_price')
    list_display_links = ('supplier',)
    list_filter = ('supplier',)
    search_fields = ['product', 'supplier__name',]
    
    # FIXME: try to make it more generic !
    def units_minimum_amount_pretty(self, obj):
        return obj.units_minimum_amount or '--'
    units_minimum_amount_pretty.short_description = "minimum amount"
    
    # FIXME: try to make it more generic !
    def units_per_box_pretty(self, obj):
        return obj.units_per_box or '--'
    units_per_box_pretty.short_description = "units per box"

    def order_min_amount_pretty(self, obj):
        return obj.detail_minimum_amount or '--'
    order_min_amount_pretty.short_description = "minimum amount"
    
    # FIXME: try to make it more generic !
    def order_step_pretty(self, obj):
        return obj.detail_step or '--'
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
                'pact',
                ('date_start', 'date_end'),   
                'delivery',  
                'withdrawal',              
              )
            }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            pass
        elif 1: #TODO request.user.has_perm(PERM)
            if db_field.name == "gas":
                gas_qs = gas_models.GAS.objects.filter(gasmember__in=[request.user.person])
                kwargs["queryset"] = gas_qs
            elif db_field.name == "supplier":
                gas_qs = gas_models.GAS.objects.filter(gasmember__in=[request.user.person])
                supplier_qs = supplier_models.Supplier.objects.filter(gas__in=gas_qs)
                kwargs["queryset"] = supplier_qs
        return super(GASSupplierOrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        return super(GASSupplierOrderAdmin, self).queryset(request)

    #inlines = [GASSupplierOrderProductInline, ]
    
class GASSupplierOrderProductAdmin(admin.ModelAdmin):
    pass


class GASMemberOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : (
            'purchaser',
            'ordered_product',
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
    
class UserProfileAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #TODO placeholder domthu: limit choices to ParamRole bound to user with PrincipalParamRoleRelation
        #see up GASSupplierOrderAdmin class
        pass
    
admin.site.register(base_models.Person, PersonAdmin)
admin.site.register(base_models.Place, PlaceAdmin)
admin.site.register(base_models.Contact)

admin.site.register(supplier_models.Supplier, SupplierAdmin)
admin.site.register(supplier_models.Product, ProductAdmin)
admin.site.register(supplier_models.ProductCategory)
admin.site.register(supplier_models.SupplierStock, SupplierStockAdmin)
admin.site.register(supplier_models.Certification)

admin.site.register(gas_models.GASMember, GASMemberAdmin)
admin.site.register(gas_models.GAS, GASAdmin)
admin.site.register(gas_models.GASConfig, GASConfigAdmin)
admin.site.register(gas_models.base.GASSupplierSolidalPact)
admin.site.register(gas_models.order.GASSupplierStock)
admin.site.register(gas_models.order.GASSupplierOrder, GASSupplierOrderAdmin)
admin.site.register(gas_models.order.GASSupplierOrderProduct, GASSupplierOrderProductAdmin)
admin.site.register(gas_models.order.GASMemberOrder, GASMemberOrderAdmin)
admin.site.register(gas_models.order.Delivery, DeliveryAdmin)
admin.site.register(gas_models.order.Withdrawal, WithdrawalAdmin)
admin.site.register(rest_models.HomePage)

admin.site.register(auth_models.PrincipalParamRoleRelation)
admin.site.register(user_models.UserProfile, UserProfileAdmin)

