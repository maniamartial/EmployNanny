from django.contrib import admin
from .models import Message


class MessageModel(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')


# Register your models here.
# admin.site.register(Conversation)
admin.site.register(Message, MessageModel)
