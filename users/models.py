

from django.contrib.auth.models import User
from django.db import models

AVAILABILITY_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)
HIGHEST_LEVEL_EDUCATION=(
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)

class NannyDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    id_number = models.IntegerField(default=0)
    level_of_education = models.CharField(max_length=100, choices=HIGHEST_LEVEL_EDUCATION)
    recommendation_letter = models.FileField(upload_to='recommendations/', null=True)
    nationality = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, choices=AVAILABILITY_CHOICES)
    language = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    years_of_experience = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

