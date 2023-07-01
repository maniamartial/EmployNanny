from jobapp.models import ContractModel, JobApplication
from django.contrib.messages import get_messages
import datetime as datetime
from django.core import mail
from .models import JobApplication, ContractModel, jobModel
from django.test import TestCase
from django.shortcuts import get_object_or_404
from users.models import NannyDetails, EmployerProfile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import jobModel
from .form import jobPostingForm
from Notifications.models import Notification


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


# test applying for a job


class ApplyForJobTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.nanny_details = NannyDetails.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Nanny',
            # Add other necessary nanny details
        )

    def test_apply_for_job(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to apply for the job
        response = self.client.post(
            reverse('apply_for_job', args=[self.job.pk]))

        # Check for a redirect response
        self.assertEqual(response.status_code, 302)

        # Check if a JobApplication object is created
        job_application = JobApplication.objects.filter(
            job=self.job, nanny=self.nanny_details).first()
        self.assertIsNotNone(job_application)

        # Assert the success message
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Your job application has been submitted successfully.')

        # Add more assertions to check if the email notification and employer notification are sent correctly

        # Redirect to the appropriate page
        self.assertRedirects(response, reverse('job_application_status'))


# create Contract


class CreateContractTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.nanny = NannyDetails.objects.create(user=self.user)
        self.employer_profile = EmployerProfile.objects.create(user=self.user)

        self.job = jobModel.objects.create(
            employer=self.employer_profile.user,
            category='Full-time Nanny',
            city='Your City',
            addresss='Your Address',
            salary=1000,
            language='English',
            nanny_age='18-25',
            hours_per_day=8,
            start_date=datetime.date.today(),
            years_of_experience=3,
            duration='1 - 2 years',
            job_description='Your job description',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks'
        )

        self.application = JobApplication.objects.create(
            job=self.job, nanny=self.nanny
        )

    def test_create_contract_and_start_duration(self):
        login_successful = self.client.login(
            username='testuser',
            password='testpassword'
        )
        self.assertTrue(login_successful)

        response = self.client.get(
            reverse('create_contract', args=[self.application.id])
        )

        # Check for a successful response
        self.assertEqual(response.status_code, 200)

        # Check if the contract has been created
        contract = ContractModel.objects.filter(
            job=self.job, nanny=self.nanny, employer=self.employer_profile.user
        ).first()
        self.assertIsNotNone(contract)

        # Check if the contract start date is set
        self.assertIsNotNone(contract.start_date)

        # Check if the application status has been updated
        self.assertEqual(self.application.status, 'pending')

        # Check if the notification has been saved to the nanny's model
        nanny_notification = Notification.objects.filter(
            user=self.nanny.user
        ).first()
        self.assertIsNotNone(nanny_notification)
        self.assertEqual(nanny_notification.title, 'New Contract')

        # Add more assertions as needed

        # Clean up the test data
        contract.delete()
        self.application.delete()
        self.job.delete()
        self.employer_profile.delete()
        self.nanny.delete()
        self.user.delete()


# Test if contract will get accepted or rejected
class AcceptContractTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.nanny = NannyDetails.objects.create(user=self.user)
        self.employer_profile = EmployerProfile.objects.create(user=self.user)
        self.job = jobModel.objects.create(
            employer=self.employer_profile.user,
            category='Full-time Nanny',
            city='Your City',
            addresss='Your Address',
            salary=1000,
            language='English',
            nanny_age='18-25',
            hours_per_day=8,
            start_date=datetime.date.today(),
            years_of_experience=3,
            duration='1 - 2 years',
            job_description='Your job description',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks'
        )
        self.application = JobApplication.objects.create(
            job=self.job, nanny=self.nanny
        )
        self.contract = ContractModel.objects.create(
            job=self.job, nanny=self.nanny, employer=self.employer_profile.user
        )

    def test_accept_contract(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accept_contract', args=[self.contract.id]), {
            'accept': 'Accept',
            'signature_data': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAgAElEQVR4XuzdC6RUZdvH8VJ+iYr5...',
        })

        # Check for a successful response
        self.assertEqual(response.status_code, 302)

        # Refresh the contract object from the database
        self.contract.refresh_from_db()

        # Check if the contract status is updated to 'active'
        self.assertEqual(self.contract.status, 'active')

        # Refresh the job application object from the database
        self.application.refresh_from_db()

        # Check if the job application status is updated to 'accepted'
        self.assertEqual(self.application.status, 'accepted')

        # Check if a success message is added to the messages framework
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn('Contract accepted successfully.', messages)

        # Add more assertions as needed

    def tearDown(self):
        self.contract.delete()
        self.application.delete()
        self.job.delete()
        self.employer_profile.delete()
        self.nanny.delete()
        self.user.delete()


# delete job application


class DeleteJobApplicationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.nanny = NannyDetails.objects.create(user=self.user)
        self.employer_profile = EmployerProfile.objects.create(user=self.user)
        self.job = jobModel.objects.create(
            employer=self.employer_profile.user,
            category='Full-time Nanny',
            city='Your City',
            addresss='Your Address',
            salary=1000,
            language='English',
            nanny_age='18-25',
            hours_per_day=8,
            start_date=datetime.date.today(),
            years_of_experience=3,
            duration='1 - 2 years',
            job_description='Your job description',
            days_off='Every weekend',
            leave_available=False,
            vacation_days_per_year='2 weeks'
        )
        self.application = JobApplication.objects.create(
            job=self.job, nanny=self.nanny
        )

    def test_delete_job_application(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_job_application', args=[self.application.id]))

        # Check for a successful response
        self.assertEqual(response.status_code, 302)

        # Check if the job application is deleted from the database
        self.assertFalse(JobApplication.objects.filter(
            id=self.application.id).exists())

        # Check if a success message is added to the messages framework
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn('Job application deleted successfully.', messages)

        # Add more assertions as needed

    def tearDown(self):
        self.application.delete()
        self.job.delete()
        self.employer_profile.delete()
        self.nanny.delete()
        self.user.delete()


class EndContractTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.nanny = User.objects.create_user(
            username='nannyuser',
            password='nannypassword'
        )
        self.employer_profile = EmployerProfile.objects.create(user=self.user)
        self.nanny_details = NannyDetails.objects.create(user=self.nanny)
        self.job_application = JobApplication.objects.create(
            job=jobModel.objects.create(
                employer=self.employer_profile.user,
                category='Full-time Nanny',
                city='Your City',
                addresss='Your Address',
                salary=1000,
                language='English',
                nanny_age='18-25',
                hours_per_day=8,
                start_date=datetime.date.today(),
                years_of_experience=3,
                duration='1 - 2 years',
                job_description='Your job description',
                days_off='Every weekend',
                leave_available=False,
                vacation_days_per_year='2 weeks'
            ),
            nanny=self.nanny_details
        )
        self.contract = ContractModel.objects.create(
            id=1,
            job=self.job_application.job,
            nanny=self.nanny_details
        )

    def test_end_contract(self):
        # Log in as the employer
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to end the contract
        response = self.client.post(
            reverse('end_contract', args=[self.contract.id]),
            follow=True
        )

        # Check if the contract and job application have been terminated
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.status, 'terminated')
        self.job_application.refresh_from_db()
        self.assertEqual(self.job_application.status, 'terminated')

        # Check if a notification has been saved for the nanny
        nanny_notification = Notification.objects.filter(
            user=self.nanny_details.user).first()
        self.assertIsNotNone(nanny_notification)
        self.assertEqual(nanny_notification.title, 'Give review')

        # Check if the user is redirected to the post-review page
        self.assertRedirects(response, reverse(
            'post_review', args=[self.contract.id]))

        # Check the success message
        messages = [str(m) for m in response.context['messages']]
        self.assertIn('Contract terminated successfully.', messages)
