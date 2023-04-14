from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
CATEGORIES=(
    ('Full-time Nanny', 'full-time nanny'),
    ('Part-time Nanny', 'parttime nanny'),
    ('Live-in Nanny', 'live-in nanny'),
    ('Live-out Nanny', 'Live-out Nanny'),
    ('Night Nanny', 'night nanny')
)


HIGHEST_LEVEL_EDUCATION=(
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)

CONTRACT_DURATION=(
    ('Less than 6 months', "less than 6 months"),
    ('1 - 2 Years', '1 - 2 years'),
    ('3 -6 years', '3 - 6 years'),
    ('More than 7 years', 'more than 7 years')
)

AGE_GROUP_CHOICES = (
('18-25', '18-25'),
('26-35', '26-35'),
('36-45', '36-45'),
('46 and above', '46 and above'),
('No preference', 'No preference'),
)

class jobModel(models.Model):
    employer=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.CharField(max_length=100, choices=CATEGORIES)
    city=models.CharField(max_length=100)
    addresss=models.CharField(max_length=100)
    salary=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    nanny_age=models.CharField(max_length=100, choices=AGE_GROUP_CHOICES)
    hours_per_day=models.IntegerField(default=2)
    start_date=models.DateField()
    years_of_experience=models.IntegerField(default=0)
    duration=models.CharField(max_length=100, choices=CONTRACT_DURATION)
    date_posted=models.DateTimeField(auto_now_add=True)
    job_description=models.TextField(blank=True)

    def __str__(self):
        return self.category
    






    
