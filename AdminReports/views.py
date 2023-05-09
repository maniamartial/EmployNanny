from datetime import datetime
from jobapp.models import JobApplication
from users.models import NannyDetails
from reportlab.pdfgen import canvas
from jobapp.models import jobModel, ContractModel
from django.db.models import Q
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from tablib import Dataset
from .resources import PaymentResource
from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
from django.shortcuts import render
from payment.models import Payment
from django.db.models import Sum
# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def transaction_list(request):
    payments = Payment.objects.all()
    total_amount = payments.aggregate(Sum('amount'))['amount__sum']
    total_commission = round(total_amount * 0.1, 2)
    total_salary = round(total_amount*0.9, 2)
    for payment in payments:
        payment.company_commission = round(payment.amount * 0.1, 2)
        payment.salary = round(payment.amount - payment.company_commission, 2)
    context = {
        'payments': payments,
        'total_amount': total_amount,
        'total_commission': total_commission,
        'total_salary': total_salary
    }
    return render(request, 'admin/transaction_list.html', context)


class GeneratePdfTransactions(View):
    def get(self, request, *args, **kwargs):
        template = 'admin/transaction_list_table.html'
        payments = Payment.objects.all()
        for payment in payments:
            payment.company_commission = round(payment.amount * 0.1, 2)
            payment.salary = round(
                payment.amount - payment.company_commission, 2)
            payment.save()
        total_amount = payments.aggregate(Sum('amount'))['amount__sum']
        total_commission = round(total_amount * 0.1, 2)
        total_salary = round(total_amount*0.9, 2)
        context = {'payments': payments,
                   'total_amount': total_amount,
                   'total_commission': total_commission,
                   'total_salary': total_salary}

        html = render_to_string(template, context=context, request=request)
        pdf_file = open('transactions.pdf', 'w+b')
        pisa.CreatePDF(html.encode('utf-8'), pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
        pdf_file.close()
        return response


class ExportExcelTransactions(View):
    def get(self, request, *args, **kwargs):
        payments_resource = PaymentResource()
        dataset = payments_resource.export()
        response = HttpResponse(
            dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="payments.xls"'
        return response


def employers_list(request):
    employers = User.objects.filter(groups__name='employer')
    employer_info = []

    for employer in employers:
        jobs_posted = jobModel.objects.filter(employer=employer).count()
        active_contracts = ContractModel.objects.filter(
            employer=employer, status='active').count()
        payment_made = Payment.objects.filter(
            user=employer, status='success').aggregate(Sum('amount'))['amount__sum']

        employer_info.append({
            'username': employer.username,
            'jobs_posted': jobs_posted,
            'active_contracts': active_contracts,
            'payment_made': payment_made,
        })

    context = {'employers': employer_info}
    return render(request, 'admin/employers_list.html', context)

# will revisit


def delete_employer(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('employer_list')


# download pdf


def generate_employer_report(request):
    # Get the employer data
    employers = User.objects.filter(groups__name='employer')
    employer_info = []
    for employer in employers:
        jobs_posted = jobModel.objects.filter(employer=employer).count()
        active_contracts = ContractModel.objects.filter(
            employer=employer, status='active').count()

        done_payments = Payment.objects.filter(
            user=employer, status='success').count()
        payment_made = Payment.objects.filter(
            user=employer, status='success').aggregate(Sum('amount'))['amount__sum']
        employer_info.append({
            'username': employer.username,
            'jobs_posted': jobs_posted,
            'active_contracts': active_contracts,
            'payment_made': payment_made,
        })

    # Create the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employers_report.pdf"'

    # Create the canvas
    p = canvas.Canvas(response)

    # Set up the document
    p.setTitle("Employers Report")

    # Draw the title
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(300, 750, "Employers Report")

    # Draw the table
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 700, "Username")
    p.drawString(200, 700, "Jobs Posted")
    p.drawString(350, 700, "Active Contracts")
    p.drawString(500, 700, "Payment(Ksh.)")
    p.line(50, 690, 550, 690)
    p.setFont("Helvetica", 10)
    y = 670
    for employer in employer_info:
        p.drawString(50, y, employer['username'])
        p.drawString(200, y, str(employer['jobs_posted']))
        p.drawString(350, y, str(employer['active_contracts']))
        p.drawString(500, y, str(employer['payment_made']))
        y -= 20

    # Close the PDF file
    p.showPage()
    p.save()
    return response


# nannylist


def nanny_list(request):
    nanny_details = NannyDetails.objects.filter(user__groups__name='nanny')
    nanny_info = []
    for nanny_detail in nanny_details:
        job_applications = JobApplication.objects.filter(
            nanny=nanny_detail)
        contracts = ContractModel.objects.filter(
            nanny=nanny_detail, status='active')
        nanny_info.append({
            'first_name': nanny_detail.first_name,
            'last_name': nanny_detail.last_name,
            'id_number': nanny_detail.id_number,
            'date_joined': nanny_detail.date_joined,
            'jobs_applied_for': job_applications.count(),
            'contract_exists': True if contracts.exists() else False,
        })

    context = {'nannies': nanny_info}
    return render(request, 'admin/nanny_list.html', context)


'''for nanny_detail in nanny_details:
        job_applications = JobApplication.objects.filter(
            nanny=nanny_detail.user)
        contracts = ContractModel.objects.filter(
            nanny=nanny_detail.user, status='active')

        nanny_info.append({
            'first_name': nanny_detail.first_name,
            'last_name': nanny_detail.last_name,
            'id_number': nanny_detail.id_number,
            'date_joined': nanny_detail.date_joined,
            'jobs_applied_for': job_applications.count(),
            'contract_exists': True if contracts.exists() else False,
        })
'''


def generate_nanny_report(request):
    # Get the nanny data
    nanny_details = NannyDetails.objects.filter(user__groups__name='nanny')
    nanny_info = []
    for nanny_detail in nanny_details:
        job_applications = JobApplication.objects.filter(
            nanny=nanny_detail)
        contracts = ContractModel.objects.filter(
            nanny=nanny_detail, status='active')
        nanny_info.append({
            'first_name': nanny_detail.first_name,
            'last_name': nanny_detail.last_name,
            'id_number': nanny_detail.id_number,
            'date_joined': nanny_detail.date_joined,
            'jobs_applied_for': job_applications.count(),
            'contract_exists': True if contracts.exists() else False,
        })

    # Create the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nanny_list.pdf"'

    # Create the canvas
    p = canvas.Canvas(response)

    # Set up the document
    p.setTitle("Nanny List")

    # Draw the title
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(300, 750, "Nanny List")

    # Draw the table
  # Draw the table
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 700, "Name")
    p.drawString(200, 700, "ID Number")
    p.drawString(300, 700, "Date Joined")
    p.drawString(400, 700, "Applications")
    p.drawString(500, 700, "Contract Exists")
    p.line(50, 690, 550, 690)
    p.setFont("Helvetica", 10)
    y = 670
    for nanny in nanny_info:
        full_name = '{} {}'.format(nanny['first_name'], nanny['last_name'])
        p.drawString(50, y, full_name)
        p.drawString(200, y, str(nanny['id_number']))
        p.drawString(300, y, nanny['date_joined'].strftime('%m/%d/%Y'))
        p.drawString(400, y, str(nanny['jobs_applied_for']))
        p.drawString(500, y, 'Yes' if nanny['contract_exists'] else 'No')
        y -= 20

    # Close the PDF file
    p.showPage()
    p.save()
    return response
