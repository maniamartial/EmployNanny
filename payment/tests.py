from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Payment, SalaryPayment, EmployerTransactions
from .views import initiate_b2c_transaction, paypal_payment


class PaymentTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_mpesa_payment_initiation(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a payment object
        payment = Payment.objects.create(
            user=self.user,
            phone_number='0712345678',
            amount=100
        )

        # Call the initiate_b2c_transaction view
        response = self.client.post(
            reverse('initiate_payment', args=[payment.id]))

        # Print the response content for debugging
        print(response.content)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

    # Rest of the test code...

        # Check if the payment status is set to "success"
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'success')

        # Check if the employer's balance and total deposited are updated correctly
        employer_transactions = EmployerTransactions.objects.get(
            employer=self.user)
        self.assertEqual(employer_transactions.balance, 100)
        self.assertEqual(employer_transactions.total_deposited, 100)

        # Check if a salary payment object is created
        salary_payment = SalaryPayment.objects.filter(
            employer=self.user).first()
        self.assertIsNotNone(salary_payment)
        self.assertEqual(salary_payment.amount, 100)

    def test_paypal_payment_initiation(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Call the paypal_payment view
        response = self.client.get(reverse('paypal_payment'))

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Assert any other necessary conditions for PayPal payment initiation

        # Add additional assertions as per your implementation
