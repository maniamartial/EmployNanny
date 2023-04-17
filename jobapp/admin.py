from django.contrib import admin
from .models import jobModel, ContractModel


class PostJobdmin(admin.ModelAdmin):
    list_display = ('category', 'date_posted', 'city', 'start_date')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('job', 'employer', 'nanny', 'start_date', 'duration')


admin.site.register(jobModel, PostJobdmin)
admin.site.register(ContractModel, ContractAdmin)
