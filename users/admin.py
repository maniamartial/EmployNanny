from django.contrib import admin
from .models import NannyDetails

class NannyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'language')

admin.site.register(NannyDetails, NannyAdmin)
