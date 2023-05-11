from django.shortcuts import get_object_or_404
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from django.views.generic import View
from jobapp.models import jobModel
from django.contrib import messages
from datetime import datetime
from jobapp.models import JobApplication, jobModel, ContractModel, DirectContract
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
from .resources import PaymentResource
from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
from django.shortcuts import render
from payment.models import Payment
from django.db.models import Sum
# Create your views here.
from django.shortcuts import render, redirect


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


# delete nanny


def delete_nanny(request, id):
    nanny = get_object_or_404(NannyDetails, id=id)

    # if request.method == 'POST':
    nanny.delete()
    return redirect('nanny_list')


# display all the job posted and applications
def job_post_list(request):
    job_posts = jobModel.objects.all()
    for job_post in job_posts:
        job_post.num_applicants = JobApplication.objects.filter(
            job=job_post).count()
        job_post.contract_exists = ContractModel.objects.filter(
            job=job_post).exists()
    return render(request, 'admin/job_post_list.html', {'job_posts': job_posts})


# generate job_list report
def generate_job_post_report(request):
    # Get the job post data
    job_posts = jobModel.objects.all()
    job_info = []
    for job_post in job_posts:
        job_applications = JobApplication.objects.filter(
            job=job_post)
        contracts = ContractModel.objects.filter(
            job=job_post, status='active')
        job_info.append({
            'job_id': job_post.id,
            'category': job_post.category,
            'employer': job_post.employer,
            'salary': job_post.salary,
            'applicants': job_applications.count(),
            'contract_exists': True if contracts.exists() else False,
        })

    # Create the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="job_post_list.pdf"'

    # Create the canvas
    p = canvas.Canvas(response)

    # Set up the document
    p.setTitle("Job Post List")

    # Draw the title
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(300, 750, "Job Post List")

    # Draw the table
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 700, "Job ID")
    p.drawString(125, 700, "Category")
    p.drawString(250, 700, "Employer")
    p.drawString(400, 700, "Salary")
    p.drawString(475, 700, "Applicants")
    p.drawString(550, 700, "Contract Exists")
    p.line(50, 690, 550, 690)
    p.setFont("Helvetica", 10)
    y = 670
    for job in job_info:
        p.drawString(50, y, str(job['job_id']))
        p.drawString(125, y, job['category'])
        p.drawString(250, y, job['employer'])
        p.drawString(400, y, str(job['salary']))
        p.drawString(475, y, str(job['applicants']))
        p.drawString(550, y, 'Yes' if job['contract_exists'] else 'No')
        y -= 20

    # Close the PDF file
    p.showPage()
    p.save()
    return response


# Display all the contracts available


def display_contracts(request):
    contracts = ContractModel.objects.all()
    direct_contracts = DirectContract.objects.all()
    context = {
        'contracts': contracts,
        'direct_contracts': direct_contracts
    }
    return render(request, 'admin/contract_lists.html', context)


# download pdf


def generate_contract_pdf(request):
    # Create a file object to write the PDF to
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contracts.pdf"'

    # Create a canvas object to draw on
    pdf_canvas = canvas.Canvas(response, pagesize=letter)

    # Define styles for the table header and rows
    table_header_style = ('Helvetica-Bold', 12)
    table_row_style = ('Helvetica', 10)

    # Draw the contracts table
    pdf_canvas.setFont(*table_header_style)
    pdf_canvas.drawString(1*inch, 10*inch, 'Contracts')
    pdf_canvas.setFont(*table_row_style)
    y = 9.5*inch

    # Add table headers
    pdf_canvas.setFont("Helvetica-Bold", 11)
    pdf_canvas.drawString(1*inch, y, 'Job Category')
    pdf_canvas.drawString(2.5*inch, y, 'Employer')
    pdf_canvas.drawString(4*inch, y, 'Nanny')
    pdf_canvas.drawString(5.5*inch, y, 'Start Date')
    pdf_canvas.drawString(6.5*inch, y, 'Status')
    pdf_canvas.drawString(7.5*inch, y, 'Salary')
    y -= 0.25*inch

    # Add line after headers
    pdf_canvas.line(1*inch, y, 8.5*inch, y)
    y -= 0.25*inch

    for contract in ContractModel.objects.all():
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(1*inch, y, contract.job.category)
        pdf_canvas.drawString(2.5*inch, y, str(contract.employer))

        pdf_canvas.drawString(4*inch, y, str(contract.nanny))
        pdf_canvas.drawString(5.5*inch, y, str(contract.start_date))
        if contract.status == 'terminated':
            pdf_canvas.setFillColor(colors.red)
        elif contract.status == 'active':
            pdf_canvas.setFillColor(colors.blue)
        pdf_canvas.drawString(6.5*inch, y, contract.status)
        pdf_canvas.setFillColor(colors.black)
        pdf_canvas.drawString(7.5*inch, y, str(contract.job.salary))

        y -= 0.25*inch

    # Draw the direct contracts table
    pdf_canvas.setFont(*table_header_style)
    pdf_canvas.drawString(1*inch, y-0.25*inch, 'Direct Contracts')
    pdf_canvas.setFont(*table_row_style)
    y -= 0.75*inch
    # Add table headers
    pdf_canvas.setFont("Helvetica-Bold", 11)
    pdf_canvas.drawString(1*inch, y, 'Job Category')
    pdf_canvas.drawString(2.5*inch, y, 'Employer')
    pdf_canvas.drawString(4*inch, y, 'Nanny')
    pdf_canvas.drawString(5.5*inch, y, 'Start Date')
    pdf_canvas.drawString(6.5*inch, y, 'Status')
    pdf_canvas.drawString(7.5*inch, y, 'Salary')
    y -= 0.25*inch

    # Add line after headers
    pdf_canvas.line(1*inch, y, 8.5*inch, y)
    y -= 0.25*inch
    for direct_contract in DirectContract.objects.all():
        pdf_canvas.setFont("Helvetica", 10)

        pdf_canvas.drawString(1*inch, y, direct_contract.job_category)
        pdf_canvas.drawString(2.5*inch, y, str(direct_contract.employer))
        pdf_canvas.drawString(
            4*inch, y, str(direct_contract.nanny))

        pdf_canvas.drawString(5.5*inch, y, str(direct_contract.start_date))
        if direct_contract.status == 'terminated':
            pdf_canvas.setFillColor(colors.red)
        elif direct_contract.status == 'active':
            pdf_canvas.setFillColor(colors.blue)
        elif direct_contract.status == 'accepted':
            pdf_canvas.setFillColor(colors.blue)
        pdf_canvas.drawString(6.5*inch, y, direct_contract.status)
        pdf_canvas.setFillColor(colors.black)
        pdf_canvas.drawString(7.5*inch, y, str(direct_contract.salary))

        y -= 0.25*inch

    # Save the PDF to the response
    pdf_canvas.save()

    return response


# delete contract
def delete_contract(request, id):
    contract = ContractModel.objects.get(id=id)
    contract.delete()
    return redirect('display_contract')


def delete_direct_contract(request, id):
    direct_contract = DirectContract.objects.get(id=id)
    direct_contract.delete()
    return redirect('display_contracts')
