from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.contrib import admin, messages
from django.contrib.admin.util import unquote
from django.core import urlresolvers
from django import forms
from django.db.models import Q

from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add

from gf.base import models as base_models
from gf.base.const import ALWAYS_AVAILABLE
from gf.supplier import models as supplier_models
from gf.gas import models as gas_models
from flexi_auth import models as auth_models
from rest.models import pages as rest_models
from users import models as user_models
from simple_accounting import models as accounting_models
from gf.gas.models.base import GAS

import reversion

#from registration.models import RegistrationProfile as MyProfile

########################## Inlines #######################

class PersonContactInline(admin.TabularInline):
    model = base_models.Person.contact_set.through
    extra = 2
    # does not work :( see https://code.djangoproject.com/ticket/9025
    # fields = ('contact__flavour', 'value')

class GASMemberInline(admin.TabularInline):
    model = gas_models.GASMember
    extra = 0
    exclude = ('available_for_roles',)
    verbose_name = _("GAS membership")
    verbose_name_plural = _("GAS memberships")

class GASActivistInline(admin.TabularInline):
    model = gas_models.GASActivist
    exclude = ('info_description',)
    extra = 2

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

class GASMemberRoleFormset(BaseInlineFormSet):
    pass

class GASMemberRoleInline(admin.TabularInline):

    model = auth_models.ParamRole
    formset = GASMemberRoleFormset
    extra = 3

########################## ModelAdmin customizations ######

class PersonAdmin(reversion.VersionAdmin):

    inlines = [PersonContactInline, ]
    save_on_top = True

    list_display = ('__unicode__', 'name', 'surname', 'city', 'user')
    list_editable = ('name', 'surname')
    list_display_links = ('__unicode__',)
    search_fields = ('^name','^surname', 'address__city')
    fieldsets = ((None,
            { 'fields' : ('name', 'surname',
                'display_name',
                'address', 'avatar', 'website'
            )
    }),)

    #def user_with_link(self, obj):
    #    user = obj.user
    #    return u'<a target="_blank" href="%s">%s</a>' % (user.get_absolute_url(), user)
    #user_with_link.allow_tags = True
    #user_with_link.short_description = _("user")

class PlaceAdmin(admin.ModelAdmin):

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


class ContactAdmin(admin.ModelAdmin):

    search_fields = ('value',)
    list_display = ('pk', '__unicode__', 'flavour', 'value')
    list_editable = ('flavour', 'value')
    list_filter = ('flavour',)

class GASAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ('__unicode__', 'id_in_des',
        'city', 'website_with_link', 'economic_state'
    )
    fieldsets = ((_('Identity'),
            { 'fields' : ('name', 'id_in_des', 'birthday',
                'headquarter', 'contact_set', 'logo',
                'description', 'association_act', 'intent_act'
              )
    }),
# COMMENT fero: Economic state is disabled right now
#    (_("Economic"), {
#        'fields' : ('membership_fee', 'account', 'liquidity'),
#        'classes': ('collapse',)
#    }),
    )
    inlines = [ GASActivistInline, ]
    search_fields = ('^name', '^id_in_des', 'headquarter__city')

    def website_with_link(self, obj):
        url = obj.website
        return u'<a target="_blank" href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "contact_set":
            if hasattr(self, "instance"):
                kwargs["queryset"] = self.instance.contacts
        return super(GASAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, extra_context=None):
        self.instance = self.get_object(request, unquote(object_id))
        return super(GASAdmin, self).change_view(request, object_id, extra_context=extra_context)

class GASConfigForm(forms.ModelForm):

    default_withdrawal_place = make_ajax_field(gas_models.GASConfig,
        model_fieldname='default_withdrawal_place',
        channel='placechannel',
        #help_text="Search for place by name"
    )
    default_delivery_place = make_ajax_field(gas_models.GASConfig,
        model_fieldname='default_delivery_place',
        channel='placechannel',
        #help_text="Search for place by name"
    )

    class Meta:
        model = gas_models.GASConfig

    def __init__(self, *args, **kwargs):
        super(GASConfigForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            gas = kwargs['instance'].gas
            self.fields['intergas_connection_set'].queryset = GAS.objects.exclude(pk=gas.pk)

#--------

class GASConfigAdmin(admin.ModelAdmin):

    form = GASConfigForm
    save_on_top = True
    list_display = ('gas', 'default_close_day', 'order_show_only_next_delivery', 'order_show_only_one_at_a_time', 'default_delivery_day','is_suspended')
    fieldsets = ((_("Configuration"), {
        'fields' : ('order_show_only_next_delivery', 'order_show_only_one_at_a_time',
            'gasmember_auto_confirm_order', #KO by fero always True until Gasista Felice 2.0: 'auto_populate_products',
            'default_close_day', 'default_close_time', 'default_delivery_day',
            'default_delivery_time', 'can_change_delivery_place_on_each_order',
            'default_delivery_place', 'can_change_withdrawal_place_on_each_order',
            'default_withdrawal_place','notice_days_before_order_close',
            'use_order_planning', 'intergas_connection_set',
            'send_email_on_order_close', 'registration_token',
            'is_suspended'
        ),
    }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(GASConfigAdmin,self).get_form(request,obj,**kwargs)
        autoselect_fields_check_can_add(form,self.model,request.user)
        return form


class GASMemberAdmin(admin.ModelAdmin):

    save_on_top = True

    list_display = ('__unicode__', 'gas_with_link')
    fieldsets = ((None,
            { 'fields' : ('gas', 'person')
    }),
    ("Extra", {
        'fields' : ('available_for_roles', 'is_suspended', 'suspend_reason'),
        'classes': ('collapse',)
    }),
    )
    filter_horizontal = ('available_for_roles',)
    search_fields = ('person__name','person__surname')
    list_filter = ('gas', )

    actions = ['say_hello']

    class Media:
        css = {
            "all": ("css/adminchangestyles.css",)
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            person_qs = base_models.Person.objects.filter(user__isnull=False)
            kwargs["queryset"] = person_qs
        return super(GASMemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SupplierAdmin(admin.ModelAdmin):
    # Disabled inlines = [SupplierStockInline, ]

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('name', 'frontman', 'seat', 'website', 'logo')
        }),
        ('Details', {
            'fields': ('flavour', 'vat_number','certifications',)
        }),
        )

    list_display = ('name', '__unicode__', 'flavour', 'website_with_link',)
    list_display_links = ('name',)
    list_filter = ('flavour',)
    search_fields = ['name']

    def website_with_link(self, obj):
        url = obj.website
        return u'<a target="_blank" href="%s">%s</a>' % (url, url)
    website_with_link.allow_tags = True
    website_with_link.short_description = "website"

class SupplierConfigAdmin(admin.ModelAdmin):

    save_on_top = True
    fieldsets = (
        (None, {
            'fields' : ('receive_order_via_email_on_finalize',),
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

class SupplierStockAdmin(admin.ModelAdmin):

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('product', 'price', 'amount_available',)
        }),
        ('Constraints', {
            'classes': ('collapse',),
            'fields': ('units_minimum_amount', 'units_per_box', 'detail_minimum_amount', 'detail_step', 'delivery_notes',)
         })
        )

    list_display = ('supplier', 'product', 'price', 'amount_avail_pretty', 'units_minimum_amount_pretty', 'units_per_box_pretty',)
    list_editable = ('product', 'price')
    list_display_links = ('supplier',)
    list_filter = ('supplier',)
    search_fields = ['product', 'supplier__name',]

    # FIXME: try to make it more generic !
    def units_minimum_amount_pretty(self, obj):
        return obj.units_minimum_amount or '--'
    units_minimum_amount_pretty.short_description = _("minimum amount")

    # FIXME: try to make it more generic !
    def units_per_box_pretty(self, obj):
        return obj.units_per_box or '--'
    units_per_box_pretty.short_description = _("units per box")

    def amount_avail_pretty(self, obj):
        if obj.amount_available == ALWAYS_AVAILABLE:
            return 'infinity'
    amount_avail_pretty.short_description = _('amount available')


class GASSupplierOrderAdmin(admin.ModelAdmin):
    fieldsets = ((None,
            { 'fields' : (
                'pact',
                ('datetime_start', 'datetime_end'),
                'delivery',
                'withdrawal',
              )
            }),
    )
    search_fields = ('id', 'pact__supplier__name')
    list_filter = ('pact__supplier', 'pact__gas')

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

class PPRAdmin(admin.ModelAdmin):

    list_filter = ('role__role', 'role',)
    search_fields = ('user__first_name', 'user__username', 'user__last_name','role__role__name',)

class PRAdmin(admin.ModelAdmin):

    list_filter = ('role',)

class UnitConvAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'src', 'dst', 'amount')
    list_editable = ('src', 'dst', 'amount')

class GASSupplierStockAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pact', 'enabled')
    list_filter = ('pact', 'enabled')

    actions = ['disable_selected','enable_selected']

    def disable_selected(self, request, queryset):
        """
        Set enabled to False for the selected supplier stocks
        """

        for obj in queryset:
            obj.enabled = False
            obj.save()

    disable_selected.short_description = _("Disable selected supplier stocks")

    def enable_selected(self, request, queryset):
        """
        Set enabled to True for the selected supplier stocks
        """

        for obj in queryset:
            obj.enabled = True
            obj.save()

    disable_selected.short_description = _("Enable selected supplier stocks")

class PactAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
        'gas', 'supplier', 'date_signed',
        'auto_populate_products'
    )
    list_filter = ('gas', 'supplier')

class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'kind', 'account', 'description', 'amount')

    def kind(self, obj):
        return obj.transaction.kind

class SupplierProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'supplier', 'name', 'sorting')
    list_editable = ('supplier', 'name', 'sorting')
    list_filter = ('supplier',)

class RegistrationProfileAdmin(admin.ModelAdmin):

    search_fields = ('user__first_name', 'user__username', 'user__last_name')

#class StateObjectRelationAdmin(admin.ModelAdmin):
#
#        search_fields = ('content_id',)
#
#admin.site.register(StateObjectRelation, StateObjectRelationAdmin)

admin.site.register(base_models.Person, PersonAdmin)
admin.site.register(base_models.Place, PlaceAdmin)
admin.site.register(base_models.Contact, ContactAdmin)
#admin.site.register(base_models.MU)

admin.site.register(supplier_models.Supplier, SupplierAdmin)
admin.site.register(supplier_models.SupplierConfig, SupplierConfigAdmin)
admin.site.register(supplier_models.Product, ProductAdmin)
admin.site.register(supplier_models.ProductCategory)
admin.site.register(supplier_models.SupplierStock, SupplierStockAdmin)
admin.site.register(supplier_models.Certification)
admin.site.register(supplier_models.ProductPU)
admin.site.register(supplier_models.ProductMU)
admin.site.register(supplier_models.UnitsConversion, UnitConvAdmin)
admin.site.register(supplier_models.SupplierProductCategory, SupplierProductCategoryAdmin)

admin.site.register(gas_models.GASMember, GASMemberAdmin)
admin.site.register(gas_models.GAS, GASAdmin)
admin.site.register(gas_models.GASConfig, GASConfigAdmin)
admin.site.register(gas_models.base.GASSupplierSolidalPact, PactAdmin)
admin.site.register(gas_models.order.GASSupplierStock, GASSupplierStockAdmin)
admin.site.register(gas_models.order.GASSupplierOrder, GASSupplierOrderAdmin)
admin.site.register(gas_models.order.GASSupplierOrderProduct, GASSupplierOrderProductAdmin)
admin.site.register(gas_models.order.GASMemberOrder, GASMemberOrderAdmin)
admin.site.register(gas_models.order.Delivery, DeliveryAdmin)
admin.site.register(gas_models.order.Withdrawal, WithdrawalAdmin)
admin.site.register(rest_models.HomePage)

admin.site.register(auth_models.PrincipalParamRoleRelation, PPRAdmin)
admin.site.register(auth_models.ParamRole, PRAdmin)
admin.site.register(user_models.UserProfile, UserProfileAdmin)
admin.site.register(accounting_models.LedgerEntry, LedgerEntryAdmin)

#admin.site.register(MyProfile, RegistrationProfileAdmin)

