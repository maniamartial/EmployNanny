from django.contrib import admin
from .models import jobModel, ContractModel, JobApplication, DirectContract


class PostJobdmin(admin.ModelAdmin):
    list_display = ('category', 'date_posted', 'city', 'start_date')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('job', 'employer', 'nanny', 'start_date', 'duration')


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'nanny', 'status')


class DirectContractAdmin(admin.ModelAdmin):
    list_display = ('employer', 'nanny', 'city', 'start_date')


admin.site.register(jobModel, PostJobdmin)
admin.site.register(ContractModel, ContractAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(DirectContract, DirectContractAdmin)
