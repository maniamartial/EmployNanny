from django.contrib.auth.models import User
from django.db import models
from PIL import Image

AVAILABILITY_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)
HIGHEST_LEVEL_EDUCATION = (
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)

AGE_GROUP_CHOICES = (
    ('18-25', '18-25'),
    ('26-35', '26-35'),
    ('36-45', '36-45'),
    ('46 and above', '46 and above'),
    ('N/A', 'N/A'),
)


class NannyDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    id_number = models.IntegerField(default=0)
    level_of_education = models.CharField(
        max_length=100, choices=HIGHEST_LEVEL_EDUCATION)
    recommendation_letter = models.FileField(
        upload_to='recommendations/', null=True)

    nationality = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=100, choices=AVAILABILITY_CHOICES)
    language = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    years_of_experience = models.IntegerField(default=0)
    age_bracket = models.CharField(
        max_length=100, choices=AGE_GROUP_CHOICES, default="N/A")
    description = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg',
                              upload_to='nanny_profile_pics')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    id_number = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg',
                              upload_to='employer_profile_pics')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
