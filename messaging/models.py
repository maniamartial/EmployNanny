from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')


# creates a table in teh db called message, which will store all the fields
class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.id
