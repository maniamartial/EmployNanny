from django.http import HttpResponse
from .models import ContractModel
from django.shortcuts import render, get_object_or_404
#from django_q.tasks import async_task
from datetime import timedelta
from django.utils import timezone
from .models import jobModel, JobApplication
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import jobModel, ContractModel
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import jobModel
from .form import jobPostingForm, JobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import NannyDetails
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, "jobapp/home.html")


@login_required
def jobPosting(request):
    form = jobPostingForm()
    if request.method == 'POST':
        form = jobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('job_listing')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'jobapp/jobPostingTemplate.html', context)

# employer contract form


def job_listings(request):
    jobs = jobModel.objects.all().order_by('-date_posted')
    context = {'jobs': jobs}
    return render(request, 'jobapp/joblistings.html', context)


def show_all_nannies(request):
    nannies = NannyDetails.objects.all().order_by("-date_joined")

    context = {"nannies": nannies}
    print(context)
    return render(request, "jobapp/nannies_available.html", context)
# single job


def job_detail(request, job_id):
    job = get_object_or_404(jobModel, pk=job_id)
    return render(request, 'jobapp/job_detail.html', {'job': job})

# employer to update the job

# employer wh created the job can also delete the job


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(jobModel, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job_id)
        else:
            print(form.errors)
    else:
        form = JobForm(instance=job, user=request.user)
    return render(request, 'jobapp/update_job.html', {'form': form, 'job': job})


# employer who created the job, can also delete it
@login_required
def delete_job(request, pk):
    job = get_object_or_404(jobModel, pk=pk)

    if request.method == 'POST' and request.user == job.employer:
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('job_listing')

    context = {
        'job': job,
    }

    return render(request, 'jobapp/update_job.html', context)


# will return to the page later
# employer contract form
'''def create_contract(request, job_id):
    job = get_object_or_404(jobModel, pk=job_id)
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.job = job
            contract.employer = request.user
            contract.nanny = job.nanny_set.first()
            contract.save()
            return redirect('contracts:contract_detail', contract.pk)
    else:
        initial_data = {
            'duration': job.duration,
            'amount': round(float(job.salary) * 0.9, 2)
        }
        form = ContractForm(initial=initial_data)
    context = {
        'job': job,
        'form': form
    }
    return render(request, 'jobapp/create_contract.html', context)'''


# nanny making an applcations

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(jobModel, id=job_id)
    nanny_details = request.user.nannydetails

    if nanny_details is None:
        # Redirect to a page that explains that the user needs to have a NannyDetails object
        return redirect('nannyDetails')

    # Check if the nanny has already applied for the job
    if JobApplication.objects.filter(job=job, nanny=nanny_details).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_listing')

    # Create a new JobApplication object
    job_application = JobApplication(job=job, nanny=nanny_details)
    job_application.save()

    messages.success(
        request, 'Your job application has been submitted successfully.')
    return redirect('job_application_status')


# nanny page to track the status of teh job applied for
def application_status(request):
    nanny = request.user.nannydetails
    job_applications = JobApplication.objects.filter(nanny=nanny)
    context = {"job_applications": job_applications}

    for job_application in job_applications:
        contract = None
        try:
            contract = ContractModel.objects.get(
                job=job_application.job, nanny=nanny)
        except ContractModel.DoesNotExist:
            pass

        job_application.contract = contract
        context["contract"] = contract

    return render(request, 'jobapp/application_status.html', context)


# employer able to view applicants
@login_required
def job_applications(request, job_id):
    job = jobModel.objects.get(id=job_id)
    job_applications = JobApplication.objects.filter(job=job)
   # print(job_applications.nanny)
    context = {'job': job, 'job_applications': job_applications}
    return render(request, 'jobapp/job_applications.html', context)


def about_us(request):
    return render(request, "jobapp/about_us.html")


def help(request):
    return render(request, "jobapp/help.html")


# tracker timer
'''def start_contract_duration_timer(contract_id: int, end_date: timezone.datetime):
    # define a function that will be executed when the timer is done
    def timer_done():
        contract = ContractModel.objects.get(id=contract_id)
        contract.status = 'completed'
        contract.save()

    # schedule the function to run at the end of the timer
    async_task('time.sleep', (end_date - timezone.now()).total_seconds())
    async_task(timer_done)'''


#


def create_contract_and_start_duration(request, application_id):
    # Get the job application object
    application = JobApplication.objects.get(id=application_id)

    # Get the nanny and employer objects from the application object
    nanny = application.nanny
    employer = application.job.employer

    # Check if the contract has already been created
    try:
        contract = ContractModel.objects.get(
            job=application.job, nanny=nanny, employer=employer)
        message = "Contract has already been created."
    except ContractModel.DoesNotExist:
        # Create the contract
        contract = ContractModel.objects.create(
            job=application.job, nanny=nanny, employer=employer)

        # Start the duration timer
        contract.start_date = timezone.now()
        contract.save()

        # Set the timer to end the contract
        duration = application.job.duration
        # end_date = contract.start_date + timedelta(days=duration)
        # timer_id = start_contract_duration_timer(contract.id, end_date)
        end_date = timezone.now()
        contract.timer_id = end_date
        contract.save()

        application.status = 'active'
        application.save()

        message = "Contract has been created successfully."

    context = {
        'message': message,
        'application': application,
        'contract': contract
    }

    return render(request, 'jobapp/create_contract.html', context)


# nanny accepting_rejecting the contract
def accept_contract(request, contract_id):
    contract = get_object_or_404(ContractModel, id=contract_id)

    if request.method == 'POST':
        if 'accept' in request.POST:
            # Handle contract acceptance
            contract.status = 'active'
            contract.save()
            # TODO: Add code to notify the employer of the nanny's acceptance
        elif 'reject' in request.POST:
            # Handle contract rejection
            contract.status = 'terminated'
            contract.save()
            # TODO: Add code to notify the employer of the nanny's rejection

        # Redirect to the contract details page
        return redirect('view_contract', contract_id=contract_id)

    context = {
        'contract': contract,
    }

    return render(request, 'jobapp/accept_contract.html', context)


    # Set the timer to end the contract
''' end_date = contract.start_date + timedelta(days=job.duration)
    start_contract_duration_timer(contract.id, end_date)'''


# contractor to view the state of contract
'''def view_contract(request, contract_id):
    # Get the contract object
    contract = get_object_or_404(ContractModel, id=contract_id)

    # Determine the status of the contract
    if contract.accepted_by_nanny:
        status = "Accepted"
    elif contract.rejected_by_nanny:
        status = "Rejected"
    else:
        status = "Pending"

    # Render the template with the contract details and status
    return render(request, "view_contract.html", {"contract": contract, "status": status})
'''


def view_contract(request, contract_id):
    # Get the contract object
    contract = get_object_or_404(ContractModel, id=contract_id)

    # Determine the status of the contract
    if contract.status == 'active':
        status = "Active"
    elif contract.status == 'terminated':
        status = "Terminated"
    elif contract.accepted_by_nanny:
        status = "Accepted"
    elif contract.rejected_by_nanny:
        status = "Rejected"
    else:
        status = "Pending"

    # Render the template with the contract details and status
    return render(request, "jobapp/view_contract.html", {"contract": contract, "status": status})


# employer to view all the contracts that exists
@login_required
def view_all_contracts(request):
    # Get all contracts
    contracts = ContractModel.objects.filter(employer=request.user)

    # Render the template with the contract list
    return render(request, "jobapp/view_all_contracts.html", {"contracts": contracts})


@login_required
def view_all_contracts_nanny(request):
    # Get all contracts
    contracts = ContractModel.objects.filter(nanny=request.user)

    # Render the template with the contract list
    return render(request, "jobapp/view_all_contracts.html", {"contracts": contracts})
