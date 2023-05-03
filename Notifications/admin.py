from django.contrib import admin
from .models import Notification
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'read', )


admin.site.register(Notification, NotificationAdmin)
