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


def getAccessToken(request):
    consumer_key = 'XjWEg9z1ihL9zoXO1JRaCOhfIJAgB8cu'
    consumer_secret = 'y48BAeDDA0AgXqI2'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def showform(request):
    if request.user.is_authenticated:
        employer = request.user
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()

            number = '254' + str(payment.phone_number)
            amount = payment.amount

            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
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

            response = requests.post(api_url, json=request, headers=headers)
            print(response)
            return redirect('home')

    context = {'form': form}
    return render(request, 'payments/mpesa_details.html', context)


# The last page


def thankspayment(request):

    return render(request, 'payments/thanks.html', context)
