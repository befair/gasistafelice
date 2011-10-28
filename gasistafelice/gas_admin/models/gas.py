
from gasistafelice.base.models import Person
from gasistafelice.admin.models import GASAdmin, GASSupplierOrderAdmin, gas_models, supplier_models

from gasistafelice.consts import EDIT, CREATE

class GASAdmin_GAS(GASAdmin):
    change_list_template = 'gas_admin/change_list.html'

    def has_change_permission(self, request, obj=None):
        if obj is None:
            rv = super(GASAdmin, self).has_change_permission(request, None)
        else:
            rv = request.user.has_perm(EDIT, obj=obj)
        return rv

    def queryset(self, request):
        qs = super(GASAdmin_GAS, self).queryset(request)
        p = Person.objects.get(user=request.user)
        rv = qs.filter(pk__in=p.gasmember_set.values('pk'))
        return rv

class GASAdmin_GASSupplierOrder(GASSupplierOrderAdmin):

    change_list_template = 'gas_admin/change_list.html'

    def has_add_permission(self, request):
        # COMMENT fero: typical situation in which the admin interface is not enough!
        # COMMENT fero: here add is not in the context of a specific solidal pact
        #if obj is None:
        rv = super(GASSupplierOrderAdmin, self).has_add_permission(request)
        #else:
        #    rv = request.user.has_perm(CREATE, obj=obj) #if user has_perm on GASSupplierSolidalPact
        return rv

    def has_change_permission(self, request, obj=None):
        if obj is None:
            rv = super(GASSupplierOrderAdmin, self).has_change_permission(request, None)
        else:
            rv = request.user.has_perm(EDIT, obj=obj)
        return rv

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "gas":
            gas_qs = gas_models.GAS.objects.filter(gasmember__in=[request.user.person])
            kwargs["queryset"] = gas_qs
        elif db_field.name == "supplier":
            gas_qs = gas_models.GAS.objects.filter(gasmember__in=[request.user.person])
            supplier_qs = supplier_models.Supplier.objects.filter(gas__in=gas_qs)
            kwargs["queryset"] = supplier_qs
        return super(GASSupplierOrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(GASAdmin_GASSupplierOrder, self).queryset(request)
        p = Person.objects.get(user=request.user)
        #FIXME: error using gas-admin url http://127.0.0.1:8000/gas-admin/gas/gassupplierorder/
        #rv = qs.filter(gas__in=p.gasmember_set.all())
        rv = qs.filter(pact__gas__in=p.gasmember_set.all())
        return rv

