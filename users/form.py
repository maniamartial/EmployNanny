#from users.models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

AVAILABILITY_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)
HIGHEST_LEVEL_EDUCATION=(
    ('College', 'college'),
    ('High School', 'high school'),
    ('Primary School', 'primary school')
)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class loginForm(UserCreationForm):
    class Meta:
        model=User
        fields=['email', 'password1']

        
class nannyDetailsForm(UserCreationForm):
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    phone=forms.IntegerField()
    city=forms.CharField(max_length=100)
    address=forms.CharField(max_length=200)
    id_number=forms.IntegerField()
    level_of_education=forms.ChoiceField(choices=HIGHEST_LEVEL_EDUCATION)
    recommendation_letter=forms.FileField(label='Select a file')
    nationality=forms.CharField(max_length=100)
    availability=forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    language=forms.CharField(max_length=200)
    date_joined=forms.DateTimeField(auto_now=True)
    years_of_experience=forms.IntegerField()
    description=forms.Textarea()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone',
                  'address', 'id_number', 'level_of_education', 
                  'recommendation_letter', 'nationality', 'availability'
                  ,'language', 'years_of_experience', 'description']
'''
class ProfileForm(Profile):
    class Meta:
        model=Profile
        '''

