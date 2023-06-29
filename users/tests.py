from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from .models import EmployerProfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import NannyDetails

from django.db.models.signals import post_save


class NannyRegistrationTest(TestCase):

    def setUp(self):
        self.register_url = reverse('nannyRegister')
        self.login_url = reverse('login')
        self.nanny_group = Group.objects.create(name='nanny')

    def test_nanny_registration_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/nannyRegistration.html')

    def test_nanny_registration(self):
        # Test valid registration data
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Check if the user is created and assigned to the nanny group
        user = User.objects.get(username='testuser')
        self.assertTrue(user.groups.filter(name='nanny').exists())

        # Check if NannyDetails model is created for the user
        nanny_details = NannyDetails.objects.get(user=user)
        self.assertEqual(nanny_details.user, user)

    def test_nanny_registration_invalid_data(self):
        # Test registration with invalid data
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2',
                             'The two password fields didn’t match.')

        # Check if the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # Check if NannyDetails model is not created
        self.assertFalse(NannyDetails.objects.filter(
            user__username='testuser').exists())


class EmployerRegistrationTest(TestCase):

    def setUp(self):
        self.register_url = reverse('employerRegister')
        self.login_url = reverse('login')
        self.employer_group = Group.objects.create(name='employer')

    def test_employer_registration_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/employerRegistration.html')

    def test_employer_registration(self):
        # Test valid registration data
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Check if the user is created and assigned to the employer group
        user = User.objects.get(username='testuser')
        self.assertTrue(user.groups.filter(name='employer').exists())

        # Check if EmployerProfile model is created for the user
        employer_profile = EmployerProfile.objects.create(user=user)
        self.assertEqual(employer_profile.user, user)

    def test_employer_registration_invalid_data(self):
        # Test registration with invalid data
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2',
                             'The two password fields didn’t match.')

        # Check if the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # Check if EmployerProfile model is not created
        self.assertFalse(EmployerProfile.objects.filter(
            user__username='testuser').exists())


class LoginTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_valid_login(self):
        # Test valid login credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        # Replace 'home' with the expected redirect URL after successful login
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        # Test invalid login credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        # Replace 'login' with the expected URL name of the login page
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Username or Password is incorrect')

    def test_login_redirect(self):
        # Test login with redirect URL
        redirect_url = reverse('home')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
            'next': redirect_url
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
