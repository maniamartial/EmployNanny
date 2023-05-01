from django.db import models
from django.contrib.auth.models import User


# This class create a table in the db called Payment that will store all details defined
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField()
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s Payment of {self.amount} ({self.status})"
