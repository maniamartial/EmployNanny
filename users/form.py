#from users.models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import NannyDetails, EmployerProfile
from datetime import datetime


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class loginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1']


class nannyDetailsForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    id_number = forms.IntegerField(required=True)
    image = forms.ImageField(required=False, label='Upload a profile picture')

    class Meta:
        model = NannyDetails
        fields = "__all__"
        exclude = ('user', 'date_joined')


class EmployerProfileForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    id_number = forms.IntegerField(required=True)
    image = forms.ImageField(required=False, label='Upload a profile picture')

    class Meta:
        model = EmployerProfile
        fields = "__all__"
        exclude = ('user', 'date_joined')
