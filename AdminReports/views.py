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
        done_payments = Payment.objects.filter(
            user=employer, status='success').count()

        employer_info.append({
            'username': employer.username,
            'jobs_posted': jobs_posted,
            'active_contracts': active_contracts,
            'done_payments': done_payments,
        })

    context = {'employers': employer_info}
    return render(request, 'admin/employers_list.html', context)


def delete_employer(request, employer_id):
    employer = User.objects.get(pk=employer_id)
    employer.delete()
    return redirect('employer_list')
