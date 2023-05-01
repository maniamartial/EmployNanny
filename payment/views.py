from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import math
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


def getAccessToken(request):
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
    return render(request, 'payments/mpesa_details.html', context)


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
