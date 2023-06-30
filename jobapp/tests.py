from django.http import QueryDict
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import jobModel
from .form import jobPostingForm


class JobPostingTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a test client
        self.client = Client()

    def test_job_posting(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create valid job posting form data
        form_data = {
            'category': 'Full-time Nanny',
            'city': 'Test City',
            'addresss': 'Test Address',
            'salary': 23490,
            'language': 'Test Language',
            'nanny_age': '18-25',
            'hours_per_day': 2,
            'start_date': '2023-06-29',
            'years_of_experience': 0,
            'duration': '1 - 2 Years',
            'days_off': 'Every weekend',
            'leave_available': False,
            'vacation_days_per_year': '2 weeks',
            'job_description': 'Test Job Description'
        }

        # Create a job form instance with the form data and user
        form = jobPostingForm(data=form_data, user=self.user)

        # Print form errors
        if not form.is_valid():
            print(form.errors)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

        # Save the form to create a new job posting
        job_posting = form.save(commit=False)
        job_posting.employer = self.user
        job_posting.save()

        # Assert that a new job is created in the database
        self.assertEqual(jobModel.objects.count(), 1)

        # Assert the job posting attributes
        self.assertEqual(job_posting.category, 'Full-time Nanny')
        self.assertEqual(job_posting.city, 'Test City')
        self.assertEqual(job_posting.addresss, 'Test Address')
        self.assertEqual(job_posting.salary, 23490)  # Updated to integer value
        self.assertEqual(job_posting.language, 'Test Language')
        self.assertEqual(job_posting.nanny_age, '18-25')
        self.assertEqual(job_posting.hours_per_day, 2)
        self.assertEqual(job_posting.start_date.strftime(
            '%Y-%m-%d'), '2023-06-29')
        self.assertEqual(job_posting.years_of_experience, 0)
        self.assertEqual(job_posting.duration, '1 - 2 Years')
        self.assertEqual(job_posting.days_off, 'Every weekend')
        self.assertFalse(job_posting.leave_available)
        self.assertEqual(job_posting.vacation_days_per_year, '2 weeks')
        self.assertEqual(job_posting.job_description, 'Test Job Description')


# test to delete the job


class DeleteJobTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.job = jobModel.objects.create(
            employer=self.user,
            category='Full-time Nanny',
            city='Test City',
            addresss='Test Address',
            salary=23490,
            language='Test Language',
            nanny_age='18-25',
            hours_per_day=2,
            start_date='2023-06-29',
            years_of_experience=0,
            duration='1 - 2 Years',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks',
            job_description='Test Job Description'
        )

    def test_delete_job_unauthenticated(self):
        response = self.client.post(reverse('delete_job', args=[self.job.pk]))

        expected_url = '/auth/login/'
        actual_url = response.url.split('?')[0]  # Get the URL path

        self.assertEqual(actual_url, expected_url)

# Edit the job


class EditJobTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )
        self.job = jobModel.objects.create(
            employer=self.user,
            category='Full-time Nanny',
            city='Test City',
            addresss='Test Address',
            salary=23490,
            language='Test Language',
            nanny_age='18-25',
            hours_per_day=2,
            start_date='2023-06-29',
            years_of_experience=0,
            duration='1 - 2 Years',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks',
            job_description='Test Job Description'
        )

    def test_edit_job(self):
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    # Create a job
        job = jobModel.objects.create(
            employer=user,
            category='Full-time Nanny',
            city='Test City',
            addresss='Test Address',
            salary=23490,
            language='Test Language',
            nanny_age='18-25',
            hours_per_day=2,
            start_date='2023-06-29',
            years_of_experience=0,
            duration='1 - 2 Years',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks',
            job_description='Test Job Description'
        )

    # Login the test user
        login_successful = self.client.login(
            username='testuser',
            password='testpassword'
        )
        self.assertTrue(login_successful)

        # Define the updated data
        updated_data = {
            'city': 'Updated City',
            'addresss': 'Updated Address',
            'salary': 30000,
            'language': 'Updated Language',
            'nanny_age': '26-35',
            'hours_per_day': 4,
            'start_date': '2023-07-01',
            'years_of_experience': 1,
            'duration': '3 -6 years',
            'days_off': 'Every Sunday',
            'leave_available': True,
            'vacation_days_per_year': '3 weeks',
            'job_description': 'Updated Job Description'
        }

    # Send a POST request to edit the job
        response = self.client.post(
            reverse('edit_job', args=[job.pk]),
            data=updated_data
        )

        # Check for a redirect response
        self.assertEqual(response.status_code, 302)

        # Assert that the job's data has been updated
        updated_job = jobModel.objects.get(pk=job.pk)
        self.assertEqual(updated_job.city, updated_data['city'])
        self.assertEqual(updated_job.addresss, updated_data['addresss'])
        self.assertEqual(updated_job.salary, updated_data['salary'])
        self.assertEqual(updated_job.language, updated_data['language'])
        # Assert that the category remains unchanged
        self.assertEqual(updated_job.category, 'Full-time Nanny')
