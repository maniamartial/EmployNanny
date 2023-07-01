from django.contrib import admin
from .models import NannyDetails, EmployerProfile


class NannyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'language')


class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id_number', 'phone')


admin.site.register(NannyDetails, NannyAdmin)
admin.site.register(EmployerProfile, EmployerProfileAdmin)
