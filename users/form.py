#from users.models import Profile
from .models import NannyDetails
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


LANGUAGE_CHOICES = [
    ('kamba', 'kamba'),
    ('kikuyu', 'kikuyu'),
    ('luhya', 'luhya'),
    ('kiswahili', 'kiswahili'),
    ('english', 'english'),
]
NATIONALITY_CHOICES = [
    ('kenyan', 'Kenyan'),
    ('nigerian', 'Nigerian'),
    ('south_african', 'South African'),
    ('ethiopian', 'Ethiopian'),
    ('egyptian', 'Egyptian'),
    # Add more nationalities as needed
]


class nannyDetailsForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    id_number = forms.IntegerField(required=True)
    image = forms.ImageField(required=False, label='Upload a profile picture')
    id_front_image = forms.ImageField(
        required=False, label='Upload ID Front Image')
    id_back_image = forms.ImageField(
        required=False, label='Upload ID Back Image')
    good_conduct_certificate = forms.FileField(
        required=False, label='Upload Good Conduct Certificate')
    recommendation_letter = forms.FileField(
        required=False, label='Upload Recommendation Letter')

    nationality = forms.ChoiceField(choices=NATIONALITY_CHOICES)
 # Validate the phone

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone is not None:
            phone_str = str(phone)

            if phone_str.startswith('07') and len(phone_str) != 10:
                raise forms.ValidationError(
                    "Phone number starting with '07' should have exactly 10 digits.")
            elif phone_str.startswith('254') and len(phone_str) != 12:
                raise forms.ValidationError(
                    "Phone number starting with '254' should have exactly 12 digits.")
            elif len(phone_str) < 9:
                raise forms.ValidationError(
                    "Phone number should have at least 9 digits.")

        return phone
# validate the ID

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')

        if id_number is not None:
            id_number_str = str(id_number)

            if len(id_number_str) < 7 or len(id_number_str) > 8:
                raise forms.ValidationError(
                    "ID number should have 7 or 8 digits.")

        return id_number

    # language = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'language-input'}))
    class Meta:
        model = NannyDetails
        fields = "__all__"
        exclude = ('user', 'date_joined')

    class Media:
        js = ['nanny_details_form.js']


class EmployerProfileForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    id_number = forms.IntegerField(required=True)
    image = forms.ImageField(required=False, label='Upload a profile picture')
# Phone number validation

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone is not None:
            phone_str = str(phone)

            if phone_str.startswith('07') and len(phone_str) != 10:
                raise forms.ValidationError(
                    "Phone number starting with '07' should have exactly 10 digits.")
            elif phone_str.startswith('254') and len(phone_str) != 12:
                raise forms.ValidationError(
                    "Phone number starting with '254' should have exactly 12 digits.")
            elif len(phone_str) < 9:
                raise forms.ValidationError(
                    "Phone number should have at least 9 digits.")

        return phone
# Id validation

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')

        if id_number is not None:
            id_number_str = str(id_number)

            if len(id_number_str) < 7 or len(id_number_str) > 8:
                raise forms.ValidationError(
                    "ID number should have 7 or 8 digits.")

        return id_number

    class Meta:
        model = EmployerProfile
        fields = "__all__"
        exclude = ('user', 'date_joined')
