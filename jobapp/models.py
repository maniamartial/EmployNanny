from .location import LOCATION_NAMES
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from users.models import NannyDetails
# Create your models here.
from decimal import Decimal
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone


CATEGORIES = (
    ('Full-time Nanny', 'full-time nanny'),
    ('Part-time Nanny', 'parttime nanny'),
    ('Live-in Nanny', 'live-in nanny'),
    ('Live-out Nanny', 'live-out nanny'),
    ('Night Nanny', 'night nanny')
)


HIGHEST_LEVEL_EDUCATION = (
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)

CONTRACT_DURATION = [
    ('Less than 6 months', "less than 6 months"),
    ('1 - 2 Years', '1 - 2 years'),
    ('3 -6 years', '3 - 6 years'),
    ('More than 7 years', 'more than 7 years')
]

AGE_GROUP_CHOICES = (
    ('18-25', '18-25'),
    ('26-35', '26-35'),
    ('36-45', '36-45'),
    ('46 and above', '46 and above'),
    ('No preference', 'No preference'),
)

DAYS_OFF_CHOICES = (
    ('Every weekend', 'Every weekend'),
    ('Every Saturday', 'Every Saturday'),
    ('Every Sunday', 'Every Sunday'),
    ('Second Saturday every month', 'Second Saturday every month'),
    ('Second Sunday every month', 'Second Sunday every month'),
    ('Last Saturday every month', 'Last Saturday every month'),
    ('Last Sunday every month', 'Last Sunday every month'),
    ('Others', 'Others'),
)

LEAVE_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)


VACATION_CHOICES = (
    ('1 month', '1 month'),
    ('3 weeks', '3 weeks'),
    ('2 weeks', '2 weeks'),
    ('1 week', '1 week'),
    ('Others', 'Others'),
)


class jobModel(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    city = models.CharField(max_length=100, choices=LOCATION_NAMES)
    addresss = models.CharField(max_length=100)
    salary = models.IntegerField()
    language = models.CharField(max_length=100)
    nanny_age = models.CharField(max_length=100, choices=AGE_GROUP_CHOICES)
    hours_per_day = models.IntegerField(default=2)
    start_date = models.DateField()
    years_of_experience = models.IntegerField(default=0)
    duration = models.CharField(
        max_length=100, choices=CONTRACT_DURATION, default="1 - 2 years")
    date_posted = models.DateTimeField(auto_now_add=True)
    job_description = models.TextField(blank=True)
    days_off = models.CharField(
        max_length=100, choices=DAYS_OFF_CHOICES, default='Every weekend')
    leave_available = models.BooleanField(choices=LEAVE_CHOICES, default=False)
    vacation_days_per_year = models.CharField(
        max_length=100, choices=VACATION_CHOICES, default='Two weeks')

    def __str__(self):
        return self.category


CONTRACT_STATUS = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('terminated', 'Terminated'),
    ('accepted', 'Accepted'),
)

JOB_STATUS = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('canceled', 'Canceled'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
    ('terminated', 'Terminated'),
    ('rejected', 'Rejected'),
    ('expired', 'Expired')
)

class SavedJobModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'job']


class ContractModel(models.Model):
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE, default=1)
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE, limit_choices_to={
                              'user__groups__name': 'nanny'}, default=1)
    employer = models.ForeignKey(User, on_delete=models.CASCADE,  limit_choices_to={
                                 'groups__name': 'employer'}, default=1)
    start_date = models.DateField(
        auto_now_add=True,  blank=True, null=True)
    end_date = models.DateField(default=timezone.now() + timedelta(days=30))
    duration = models.CharField(
        max_length=100, choices=CONTRACT_DURATION, default="pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=100, choices=CONTRACT_STATUS, default=CONTRACT_STATUS[0][0])
    company_commission = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    nanny_signature_image = models.ImageField(
        upload_to='nanny_signatures/', null=True, blank=True)

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


class JobApplication(models.Model):
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE)
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=JOB_STATUS, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nanny.user.username} applied for {self.job.category}"


# direct contracts, where employer dont post a job, but sends an offer directly
class DirectContract(models.Model):
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_category = models.CharField(
        max_length=100, choices=CATEGORIES, default="Full-time Nanny")
    city = models.CharField(max_length=100, choices=LOCATION_NAMES)
    salary = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    job_description = models.TextField(blank=True)
    status = models.CharField(
        max_length=100, choices=CONTRACT_STATUS, default="pending")
    nanny_signature_image = models.ImageField(
        upload_to='nanny_signatures/', null=True, blank=True)
    amount_to_receive = models.IntegerField()
    company_commission = models.IntegerField()

    def save(self, *args, **kwargs):
        # calculate amount_to_receive as 90% of salary
        self.amount_to_receive = int(self.salary * 0.9)

        # calculate company_commission as 10% of salary
        self.company_commission = int(self.salary * 0.1)

        super().save(*args, **kwargs)


#Reviews and ratings


class Rating(models.Model):
    STARS_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_given')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received')
    stars = models.PositiveSmallIntegerField(choices=STARS_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reviewer)
        #abstract = True


# nanny signature
class SignedContract(models.Model):
    contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE)
    nanny = models.ForeignKey(NannyDetails, on_delete=models.CASCADE)
    signature_image = models.ImageField(upload_to='signatures/')
    date_signed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nanny.first_name


# Employer signature
class EmployerSignature(models.Model):
    contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE)
    signature_image = models.ImageField(upload_to='employer_signatures/')
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now_add=True)

    # Additional fields as per your requirements

    def __str__(self):
        return f"Employer: {self.contract.employer.username}"
