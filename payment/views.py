from django.http import JsonResponse
import base64
from django_daraja.mpesa.core import MpesaClient
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from datetime import datetime
from .form import PaymentForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
from . mpesa_Credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.contrib.auth.decorators import login_required

# A function to get Mpesa access token


def getAccessToken():
    # Mpesa Consumer key and secret
    consumer_key = 'XjWEg9z1ihL9zoXO1JRaCOhfIJAgB8cu'
    consumer_secret = 'y48BAeDDA0AgXqI2'
    # Mpesa OAuth API URL
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    # Make a GET request to the API URL with consumer key and secret as basic auth credentials
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    # Convert the response to JSON and extract the access token
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    # Return the access token as an HTTP response
    return HttpResponse(validated_mpesa_access_token)

# A view function to display the payment form


@login_required
def make_mpesa_payment(request):
    if request.user.is_authenticated:
        # Get the employer (authenticated user)
        employer = request.user
    # Create an instance of PaymentForm
    form = PaymentForm()
    if request.method == 'POST':
        # If the request method is POST, bind the form to the request data
        form = PaymentForm(request.POST)
        # If the form is valid, create a Payment object and save it to the database
        if form.is_valid():
            payment = form.save(commit=False)
            # Set the Payment object's user field to the authenticated user
            payment.user = request.user
            payment.save()
            # Format the phone number and amount
            number = '254' + str(payment.phone_number)
            amount = payment.amount
            # Get the Mpesa access token
            access_token = MpesaAccessToken.validated_mpesa_access_token
            # Set the API URL for STK Push
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            # Set the headers for the request
            headers = {"Authorization": "Bearer %s" % access_token}
            # Set the payload for the request
            payload = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA":  number,
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": number,
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Mania",
                "TransactionDesc": "Payment for services"
            }
            # Make a POST request to the API URL with the headers and payload
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200 and response.json().get('ResponseCode') == '0':
                payment.status = "success"
                payment.save()

                # Add a success message
                messages.success(request, "Payment was successful!")

                return redirect('payment_complete')
            else:
                payment.status = "failure"
                payment.save()

    context = {'form': form}
    return render(request, 'payments/home.html', context)


# The last page
# Comfirming payments


@login_required
def payment_complete(request):
    if request.user.is_authenticated:
        employer = request.user
        payments = Payment.objects.filter(user=employer)
        total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        print(total_amount)
        context = {'payments': payments, 'total_amount': total_amount}
        return render(request, 'payments/mpesa_payment_complete.html', context)
    else:
        return redirect('login')


# Paypal payment implementation
@login_required
def paypal_payment(request):
    return render(request, "payments/paypal_payments.html")


def payment_select(request):
    if request.user.is_authenticated:
        # Get the employer (authenticated user)
        employer = request.user
    # Create an instance of PaymentForm
    form = PaymentForm()
    if request.method == 'POST':
        # If the request method is POST, bind the form to the request data
        form = PaymentForm(request.POST)
        # If the form is valid, create a Payment object and save it to the database
        if form.is_valid():
            payment = form.save(commit=False)
            # Set the Payment object's user field to the authenticated user
            payment.user = request.user
            payment.save()
            # Format the phone number and amount
            number = '254' + str(payment.phone_number)
            amount = payment.amount
            # Get the Mpesa access token
            access_token = MpesaAccessToken.validated_mpesa_access_token
            # Set the API URL for STK Push
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            # Set the headers for the request
            headers = {"Authorization": "Bearer %s" % access_token}
            # Set the payload for the request
            payload = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA":  number,
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": number,
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Mania",
                "TransactionDesc": "Payment for services"
            }
            # Make a POST request to the API URL with the headers and payload
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200 and response.json().get('ResponseCode') == '0':
                payment.status = "success"
                payment.save()

                # Add a success message
                messages.success(request, "Payment was successful!")

                return redirect('payment_complete')
            else:
                payment.status = "failure"
                payment.save()

    context = {'form': form}
    return render(request, 'payments/home.html', context)


# C2B
def pay_nanny(request):
    cl = MpesaClient()
    phone_number = '0740743521'
    amount = 1
    transaction_desc = 'Description'
    occassion = 'Occassion'
    callback_url = 'https://api.darajambili.com/b2c/result'
    response = cl.business_payment(
        phone_number, amount, transaction_desc, callback_url, occassion)


def generate_access_token(consumer_key, consumer_secret):
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token

    return None


def initiate_b2c_transaction(request):
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
    consumer_key = 'ShetFZbeG2YJSXIvUojmgGrzISPjJ4EQ'
    consumer_secret = 'd8VqfDwpR6MExxAU'
    access_token = generate_access_token(consumer_key, consumer_secret)
    print(access_token)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "InitiatorName": "Mania",
        "SecurityCredential": "EYbsRO2oqNqhjhO4Q1URRAUrfuNJkWlU27K5TnlJQL4TQPs003JMvBVky5BRRnCgYyjYuqzJNGAzCNMz4wqdleNEUNlqggV7bWN5uMdWLlthFtXo0pef31HeQBV3bgnPd1m3pGT6Otk02FuTWoW8aKeyJkMxwS1kjEW7B8bJp2veXiOYWEkml3ulmaicmjg57/XtH548HXUy4WTVDEp1/eMzQMkD98Y32Y3F+AbTr8YeMDBRuGrS6VN9QgPYTNGOw5cRFXdoIyLKTZkCbQWbxP5c6is5kD8IfvTmgWMpRHarQ6+gEtY2ChcbOc/Jk9aQR+69Y1eNG3FE6kKskc0AEQ==",
        "CommandID": "SalaryPayment",
        "Amount": 1,
        "PartyA": 999001,
        "PartyB": 254740743521,
        "Remarks": "Hope its coming along",
        "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
        "ResultURL": "https://mydomain.com/b2c/result",
        "Occassion": "Pesa",
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            response_data = response.json()
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to decode API response as JSON'}, status=500)
    else:
        error_message = response.json().get(
            'errorMessage', 'Failed to initiate B2C transaction')
        return JsonResponse({'error': error_message}, status=400)


# Replace with your own credentials
'''consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'''

# Replace with your own values
#access_token = generate_access_token(consumer_key, consumer_secret)
'''initiator_name = 'YOUR_INITIATOR_NAME'
security_credential = 'YOUR_SECURITY_CREDENTIAL'
command_id = 'SalaryPayment'
amount = '1000'
party_a = 'YOUR_ORGANIZATION_SHORTCODE'
party_b = 'RECIPIENT_PHONE_NUMBER'
remarks = 'Salary Payment'
queue_timeout_url = 'YOUR_QUEUE_TIMEOUT_URL'
result_url = 'YOUR_RESULT_URL'

response = initiate_b2c_transaction(access_token, initiator_name, security_credential,
                                    command_id, amount, party_a, party_b, remarks, queue_timeout_url, result_url)
if response:
    print(response)
else:
    print('Failed to initiate B2C transaction')'''
