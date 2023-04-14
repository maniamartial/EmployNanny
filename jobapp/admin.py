from django.contrib import admin
from .models import jobModel

class PostJobdmin(admin.ModelAdmin):
    list_display = ('category', 'date_posted', 'city', 'start_date')

admin.site.register(jobModel, PostJobdmin)
