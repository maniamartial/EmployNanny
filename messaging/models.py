from django.db import models

# Create your models here.
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.id)
