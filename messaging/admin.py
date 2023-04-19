from django.contrib import admin
from .models import Conversation, Message


class MessageModel(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')


# Register your models here.
admin.site.register(Conversation)
admin.site.register(Message, MessageModel)
