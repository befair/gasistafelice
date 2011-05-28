
from gasistafelice.base.models import Person
from gasistafelice.admin.models import *

class GASAdmin_GAS(GASAdmin):
    change_list_template = 'gas_admin/change_list.html'

    def queryset(self, request):
        qs = super(GASAdmin_GAS, self).queryset(request)
        p = Person.objects.get(user=request.user)
        rv = qs.filter(pk__in=p.gasmember_set.values('pk'))
        return rv

class GASAdmin_GASSupplierOrder(GASSupplierOrderAdmin):

    change_list_template = 'gas_admin/change_list.html'

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
        rv = qs.filter(gas__isnull=True) #in=p.gasmember_set.all())
        return rv


