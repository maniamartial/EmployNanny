from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import NannyDetails
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Payment, SalaryPayment, EmployerTransactions
from .models import Payment, EmployerTransactions
from .models import SalaryPayment
import math
from jobapp.models import ContractModel, DirectContract
from django.http import JsonResponse
import base64
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
        payments = Payment.objects.filter(user=employer, status='success')
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

# mpesa


@login_required
def payment_select(request):
    if request.user.is_authenticated:
        # Get the employer (authenticated user)
        employer = request.user

        # Retrieve or create the EmployerTransactions object for the employer
        employer_transactions, _ = EmployerTransactions.objects.get_or_create(
            employer=employer)

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

            # Update EmployerTransactions for the deposited amount
            '''employer_transactions.total_deposited += payment.amount
            employer_transactions.balance += payment.amount
            employer_transactions.save()'''

            # Format the phone number and amount
            number = '254' + str(payment.phone_number)
            amount = payment.amount
            print(number)
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

                # Update EmployerTransactions for the withdrawn amount
                employer_transactions.total_deposited += payment.amount
                employer_transactions.balance += payment.amount
                employer_transactions.save()

                # Add a success message
                messages.success(request, "Payment was successful!")

                return redirect('payment_complete')
            else:
                payment.status = "failure"
                payment.save()

    context = {'form': form}
    return render(request, 'payments/home.html', context)


# generate access token for B2C
def generate_access_token(consumer_key, consumer_secret):
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token

    return None


# Pay nanny after 30 days
def initiate_b2c_transaction(request, contract_id):
    employer = request.user

    try:
        contract = ContractModel.objects.get(id=contract_id)
        direct_contract = None
    except ContractModel.DoesNotExist:
        try:
            direct_contract = DirectContract.objects.get(id=contract_id)
            contract = None
        except DirectContract.DoesNotExist:
            return JsonResponse({'error': 'Invalid contract ID'}, status=400)

    if request.method == 'POST':
        increase_salary = request.POST.get('increase_salary', False)
        extra_amount = request.POST.get('extra_amount', '0')
        try:
            extra_amount = Decimal(extra_amount)
        except InvalidOperation:
            extra_amount = Decimal('0')
        # Update job salary if the employer wants to increase it
        if increase_salary:
            if contract:
                job = contract.job
                salary = int(contract.amount)
                salary += math.ceil(extra_amount)
                contract.amount = salary
                job.salary = salary
                job.save()
                contract.save()
            elif direct_contract:

                salary = int(direct_contract.salary)
                salary += math.ceil(extra_amount)
                direct_contract.salary = int(salary)
                print(salary)
                print(direct_contract.salary)

                direct_contract.save()
                print(direct_contract.amount_to_receive)

    if contract:
        nanny = contract.nanny
        amount = math.ceil(contract.amount)
    elif direct_contract:
        nanny = direct_contract.nanny
        amount = math.ceil(direct_contract.amount_to_receive)
    else:
        return JsonResponse({'error': 'Contract not found'}, status=404)

    phone_number = '254' + str(nanny.phone)

    employer_transactions, _ = EmployerTransactions.objects.get_or_create(
        employer=employer)

    # Check if the employer's balance is sufficient
    if employer_transactions.balance < amount:
        print(employer_transactions.balance)
        messages.warning(
            request, 'Your balance is too low to make the payment, kindly deposit amount.')
        return redirect(request.META.get('HTTP_REFERER'))
    amount = str(amount)
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
        "InitiatorName": "EmployNanny",
        "SecurityCredential": "EYbsRO2oqNqhjhO4Q1URRAUrfuNJkWlU27K5TnlJQL4TQPs003JMvBVky5BRRnCgYyjYuqzJNGAzCNMz4wqdleNEUNlqggV7bWN5uMdWLlthFtXo0pef31HeQBV3bgnPd1m3pGT6Otk02FuTWoW8aKeyJkMxwS1kjEW7B8bJp2veXiOYWEkml3ulmaicmjg57/XtH548HXUy4WTVDEp1/eMzQMkD98Y32Y3F+AbTr8YeMDBRuGrS6VN9QgPYTNGOw5cRFXdoIyLKTZkCbQWbxP5c6is5kD8IfvTmgWMpRHarQ6+gEtY2ChcbOc/Jk9aQR+69Y1eNG3FE6kKskc0AEQ==",
        "CommandID": "SalaryPayment",
        "Amount": amount,
        "PartyA": 999001,
        "PartyB": phone_number,
        "Remarks": "Hope its coming along",
        "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
        "ResultURL": "https://mydomain.com/b2c/result",
        "Occasion": "Pesa",
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            response_data = response.json()
            amount = Decimal(amount)
            # save salary payment
            if contract:
                payment = SalaryPayment.objects.create(
                    employer=employer,
                    nanny=nanny,
                    contract=contract,
                    amount=amount
                )
            elif direct_contract:
                payment = SalaryPayment.objects.create(
                    employer=employer,
                    nanny=nanny,
                    direct_contract=direct_contract,
                    amount=amount
                )
            else:
                return JsonResponse({'error': 'Invalid contract'}, status=400)

            # update the employer transaction
            # Update EmployerTransactions for the withdrawn amount
            employer_transactions.total_withdrawn += amount
            employer_transactions.balance -= amount
            employer_transactions.save()

            return redirect("employer_transaction_report")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to decode API response as JSON'}, status=500)

    else:
        error_message = response.json().get(
            'errorMessage', 'Failed to initiate B2C transaction')
        return JsonResponse({'error': error_message}, status=400)


def employer_report(request):
    if request.user.is_authenticated:
        # Get the employer (authenticated user)
        employer = request.user

        # Retrieve employer transactions
        employer_transactions = EmployerTransactions.objects.get(
            employer=employer)

        # Retrieve payments made by the employer
        payments = Payment.objects.filter(user=employer)

        # Retrieve salary payments made by the employer
        salary_payments = SalaryPayment.objects.filter(employer=employer)

        context = {
            'employer': employer,
            'employer_transactions': employer_transactions,
            'payments': payments,
            'salary_payments': salary_payments,
        }
        return render(request, 'payments/employer_transaction_report.html', context)
    else:
        # Redirect to login if user is not authenticated
        return redirect('login')


def generate_employer_transaction(request):
    # Retrieve the necessary data for the report
    payments = Payment.objects.filter(user=request.user)
    salary_payments = SalaryPayment.objects.filter(employer=request.user)
    employer_transactions = EmployerTransactions.objects.get(
        employer=request.user)

    # Create the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employer_transaction_report.pdf"'

    # Create the document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define paragraph styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    # Add the title
    title = "Employer Transaction Report"
    elements.append(Paragraph(title, title_style))

    # Add the Payment Details table
    payment_data = [
        ["Phone Number", "Amount", "Status", "Timestamp"]
    ]
    for payment in payments:
        payment_data.append([
            payment.phone_number,
            str(payment.amount),
            payment.status,
            payment.timestamp.date().strftime("%Y-%m-%d")
        ])

    payment_table = Table(payment_data, colWidths=[100, 100, 100, 100])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph("Payment Details", heading_style))
    elements.append(payment_table)

    # Add the Salary Payment Details table
    salary_payment_data = [
        ["Nanny", "Contract", "Amount", "Payment Date"]
    ]
    for salary_payment in salary_payments:
        salary_payment_data.append([
            salary_payment.nanny.first_name,
            salary_payment.contract.job.category,
            str(salary_payment.amount),
            salary_payment.payment_date.strftime("%Y-%m-%d")
        ])

    salary_payment_table = Table(
        salary_payment_data, colWidths=[100, 100, 100, 100])
    salary_payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph("Salary Payment Details", heading_style))
    elements.append(salary_payment_table)

    # Add the Employer Transaction Details table
    employer_transaction_data = [
        ["Total Deposited", "Total Withdrawn", "Balance"],
        [employer_transactions.total_deposited,
            employer_transactions.total_withdrawn, employer_transactions.balance]
    ]

    employer_transaction_table = Table(
        employer_transaction_data, colWidths=[150, 150, 150])
    employer_transaction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph("Employer Transaction Details", heading_style))
    elements.append(employer_transaction_table)

    # Build the PDF document
    doc.build(elements)

    return response


def nanny_transaction_report(request):
    nanny = NannyDetails.objects.get(user=request.user)
    nanny_transactions = SalaryPayment.objects.filter(nanny=nanny)
    total_amount_paid = nanny_transactions.aggregate(total=Sum('amount'))[
        'total']

    context = {
        "nanny_transaction": nanny_transactions,
        "total_amount_paid": total_amount_paid,
    }
    return render(request, "payments/nanny_transaction.html", context)


# generate pdf nanny
def generate_nanny_transaction(request):
    # Retrieve the necessary data for the report
    nanny = NannyDetails.objects.get(user=request.user)
    nanny_transactions = SalaryPayment.objects.filter(nanny=nanny)
    total_amount_paid = nanny_transactions.aggregate(total=Sum('amount'))[
        'total']

    # Create the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nanny_transaction_report.pdf"'

    # Create the document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define paragraph styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    # Add the title
    title = "Nanny Transaction Report"
    elements.append(Paragraph(title, title_style))

    # Add the Transaction Details table
    transaction_data = [
        ["Employer", "Amount", "Date of Payment",
            "Contract Category", "Contract Status"]
    ]
    for transaction in nanny_transactions:
        transaction_data.append([
            f"{transaction.employer.first_name} {transaction.employer.last_name}",
            str(transaction.amount),
            transaction.payment_date.strftime("%Y-%m-%d"),
            transaction.contract.job.category,
            transaction.contract.status
        ])

    transaction_table = Table(transaction_data, colWidths=[
                              120, 80, 100, 120, 100])
    transaction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph("Transaction Details", heading_style))
    elements.append(transaction_table)

    # Add the Total Amount Paid
    elements.append(
        Paragraph(f"Total Amount Paid: {total_amount_paid}", heading_style))

    # Build the PDF document
    doc.build(elements)

    return response
