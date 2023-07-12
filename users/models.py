from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from .language import LANGUAGE_CHOICES
from django import forms
from django.core.exceptions import ValidationError
AVAILABILITY_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

HIGHEST_LEVEL_EDUCATION = (
    ('College', 'College'),
    ('High School', 'High School'),
    ('Primary School', 'Primary School')
)

AGE_GROUP_CHOICES = (
    ('18-25', '18-25'),
    ('26-35', '26-35'),
    ('36-45', '36-45'),
    ('46 and above', '46 and above'),
    ('N/A', 'N/A'),
)

NATIONALITY_CHOICES = [
    ('kenyan', 'Kenyan'),
    ('nigerian', 'Nigerian'),
    ('south_african', 'South African'),
    ('ethiopian', 'Ethiopian'),
    ('egyptian', 'Egyptian'),
    # Add more nationalities as needed
]
# this creates a table for nanny details in the db


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
        upload_to='recommendations/', null=True, blank=True)
    id_front_image = models.ImageField(
        upload_to='id_images/', default=0)
    id_back_image = models.ImageField(
        upload_to='id_images/', default=0)
    good_conduct_certificate = models.FileField(
        upload_to='good_conduct/', null=True, blank=True)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES)
    availability = models.CharField(
        max_length=100, choices=AVAILABILITY_CHOICES)
    language = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    years_of_experience = models.IntegerField(default=0)
    age_bracket = models.CharField(
        max_length=100, choices=AGE_GROUP_CHOICES, default="N/A")
    description = models.TextField(blank=True)
    image = models.ImageField(
        default='default.jpg', upload_to='nanny_profile_pics')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # To resize and optimize the images
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.id_front_image:
            img_id_front = Image.open(self.id_front_image.path)

            # Resize ID front image
            if img_id_front.height > 500 or img_id_front.width > 500:
                output_size = (500, 500)
                img_id_front.thumbnail(output_size)
                img_id_front.save(self.id_front_image.path)

        if self.id_back_image:
            img_id_back = Image.open(self.id_back_image.path)

            # Resize ID back image
            if img_id_back.height > 500 or img_id_back.width > 500:
                output_size = (500, 500)
                img_id_back.thumbnail(output_size)
                img_id_back.save(self.id_back_image.path)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# this creates a table in the database called EmployerProfile
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
