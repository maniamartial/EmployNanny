#from users.models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class loginForm(UserCreationForm):
    class Meta:
        model=User
        fields=['email', 'password1']

        
'''
class ProfileForm(Profile):
    class Meta:
        model=Profile
        '''

