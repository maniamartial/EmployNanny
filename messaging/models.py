from django.db import models

# Create your models here.
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User

'''
class Conversation(models.Model):
    participants = models.ManyToManyField(

        User, related_name='conversations', symmetrical=False)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message {self.id}"
'''

from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.id)
