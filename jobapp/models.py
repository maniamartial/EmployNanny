from django.db import models
from django.contrib.auth.models import User
from users.models import NannyDetails
# Create your models here.
from decimal import Decimal
from django.db.models import Q


CATEGORIES = (
    ('Full-time Nanny', 'full-time nanny'),
    ('Part-time Nanny', 'parttime nanny'),
    ('Live-in Nanny', 'live-in nanny'),
    ('Live-out Nanny', 'Live-out Nanny'),
    ('Night Nanny', 'night nanny')
)


HIGHEST_LEVEL_EDUCATION = (
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)

CONTRACT_DURATION = (
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
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    city = models.CharField(max_length=100)
    addresss = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    nanny_age = models.CharField(max_length=100, choices=AGE_GROUP_CHOICES)
    hours_per_day = models.IntegerField(default=2)
    start_date = models.DateField()
    years_of_experience = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, choices=CONTRACT_DURATION)
    date_posted = models.DateTimeField(auto_now_add=True)
    job_description = models.TextField(blank=True)

    def __str__(self):
        return self.category


CONTRACT_STATUS = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('terminated', 'Terminated'),
)


class ContractModel(models.Model):
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE)
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE, limit_choices_to={
                              'user__groups__name': 'nanny'})
    employer = models.ForeignKey(User, on_delete=models.CASCADE,  limit_choices_to={
                                 'groups__name': 'employer'})
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    duration = models.CharField(max_length=100, choices=CONTRACT_DURATION)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=100, choices=CONTRACT_STATUS, default=CONTRACT_STATUS[0][0])
    '''company_commission = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)'''

    def save(self, *args, **kwargs):
        # calculate contract amount as 90% of job salary
        job_salary = Decimal(self.job.salary)
        self.amount = round(job_salary * Decimal('0.9'), 2)

        # calculate company commission as 10% of job salary
        self.company_commission = round(job_salary * Decimal('0.1'), 2)

        # calculate contract duration based on job duration
        job_duration = self.job.duration
        if job_duration == 'Full-Time':
            self.duration = '1 Year'
        elif job_duration == 'Part-Time':
            self.duration = '6 Months'

        super().save(*args, **kwargs)
