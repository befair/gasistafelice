from django.contrib import admin

from api_remote.models import ExternalResource

class ExternalResourceAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'backend_name', 'first_get_on', 'last_get_on', 'is_valid', 'is_deleted')
    

admin.site.register(ExternalResource, ExternalResourceAdmin)


