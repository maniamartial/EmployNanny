from Notifications.models import Notification
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from django.db.models import Q
from jobapp.models import JobApplication
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from datetime import timedelta
from django.utils import timezone
from .models import jobModel, JobApplication, CATEGORIES, DirectContract, ContractModel
from django.shortcuts import render, get_object_or_404, redirect
from .form import jobPostingForm, JobForm, DirectContractForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import NannyDetails, AGE_GROUP_CHOICES
from django.contrib.auth.models import User
from django.db.models import Sum
from payment.models import Payment
from django.contrib.auth.decorators import user_passes_test


# Define a view function that renders the home page template
def home(request):
    return render(request, "jobapp/home.html")


def jobPosting(request):
    # Create a new job posting form instance
    form = jobPostingForm()

    # If the form has been submitted via POST method
    if request.method == 'POST':
        # Bind form data to a new job posting form instance
        form = jobPostingForm(request.POST)

        # If the form data is valid
        if form.is_valid():
            # Save the job posting to the database
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            # Redirect to the job listing page
            return redirect('job_listing')
        else:
            # Print any form validation errors to the console
            print(form.errors)

    # Create a context dictionary with the form instance
    context = {'form': form}

    # Render the job posting form template with the context data
    return render(request, 'jobapp/jobPostingTemplate.html', context)


def job_listings(request):
    # Check if user is an employer
    if request.user.groups.filter(name='employer').exists():
        # Retrieve jobs posted by the employer and order them by date posted
        jobs = jobModel.objects.filter(
            employer=request.user).order_by('-date_posted')
    else:
        # Retrieve all jobs and order them by date posted
        jobs = jobModel.objects.all().order_by('-date_posted')

    # Check the payment status of each job
    for job in jobs:
        employer = job.employer
        total_payments = Payment.objects.filter(
            user=employer).aggregate(Sum('amount'))['amount__sum'] or 0
        # If the total payments made by the employer are greater than or equal to the job's salary, mark job as verified
        if total_payments >= int(job.salary):
            job.payment_status = 'verified'
        # Otherwise, mark job as unverified
        else:
            job.payment_status = 'unverified'

    # Apply filters if they exist
    category_query = request.GET.get('category')
    salary_min = request.GET.get('salary_min')

    if category_query:
        jobs = jobs.filter(category__iexact=category_query)
    if salary_min:
        jobs = jobs.filter(salary__gte=Decimal(salary_min))

    # Paginate the job list
    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create context dictionary with necessary variables
    context = {
        'page_obj': page_obj,
        'category_query': category_query,
        'salary_min': salary_min,
        'categories': CATEGORIES
    }

    # Render the job listings template with the context dictionary
    return render(request, 'jobapp/joblistings.html', context)


def show_all_nannies(request):
    # set to empty string if not present
    city_query = request.GET.get('city', '')
    age_query = request.GET.get('age')

    # check if both city and age queries are present
    if city_query and age_query:
        nannies = NannyDetails.objects.filter(
            city__icontains=city_query, age_bracket=age_query).order_by("-date_joined")
    # if only city query is present
    elif city_query:
        nannies = NannyDetails.objects.filter(
            city__icontains=city_query).order_by("-date_joined")
    # if only age query is present
    elif age_query:
        nannies = NannyDetails.objects.filter(
            age_bracket=age_query).order_by("-date_joined")
    # if neither city nor age queries are present
    else:
        nannies = NannyDetails.objects.all().order_by("-date_joined")

    # paginate the results
    paginator = Paginator(nannies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # set default value to '' if age_query is not present
    age_query_value = age_query if age_query else ''

    # prepare the context to be passed to the template
    context = {
        "page_obj": page_obj,
        "city_query": city_query,
        "age_query": AGE_GROUP_CHOICES,  # add age choices to context
        "selected_age_query": age_query_value,  # add selected_age_query to context
    }

    # render the template with the context
    return render(request, "jobapp/nannies_available.html", context)


# view function for displaying single job details
def job_detail(request, job_id):
    # retrieve the job object with the given id or raise a 404 error if it doesn't exist
    job = get_object_or_404(jobModel, pk=job_id)
    context = {'job': job}
    # render the job detail template with the job object passed as context
    return render(request, 'jobapp/job_detail.html',  context)


# employer to update the job
# employer who created the job can also delete the job
@login_required
def edit_job(request, job_id):
    # retrieve the job with given id, if its not available then raise 4040 error
    job = get_object_or_404(jobModel, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job, user=request.user)

        # if form is valid, save the modified data to teh database
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job_id)

        # if form is invalid, print our errors for easy debugging
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


# nanny making an applcations
'''@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(jobModel, id=job_id)
    # get the nannydetails from the loggedin nanny
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
    return redirect('job_application_status')'''


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(jobModel, id=job_id)
    # get the nannydetails from the loggedin nanny
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

    # Send email notification to the employer
    employer_email = job.employer.email
    nanny_name = f'{nanny_details.first_name} {nanny_details.last_name}'
    subject = 'New Job Applicant'
    message = f'{nanny_name} has applied for your job. Please check your dashboard to view their application.'
#html_message = render_to_string('notifications/email_template.html', {'nanny_name': nanny_name})
    email = EmailMessage(
        subject, message, 'from@example.com', [employer_email])
    email.content_subtype = "html"
    email.send()

 # Save notification to the employer's model
    title = "Received an applicant"
    notification_message = f'{nanny_name} has applied for your job. Please check your dashboard to view their application.'
    employer_notification = Notification(
        user=job.employer, message=notification_message, title=title)
    print(employer_notification)
    try:
        employer_notification.save()
    except Exception as e:
        print(f"Error saving notification: {e}")

    messages.success(
        request, 'Your job application has been submitted successfully.')
    return redirect('job_application_status')


@login_required
def application_status(request):
    # check if the nanny loggedin has nannyDetails
    try:
        nanny = request.user.nannydetails
    except NannyDetails.DoesNotExist:
        return redirect('nannyDetails')

# only after the applications that belong to the loggedin nanny
    job_applications = JobApplication.objects.filter(nanny=nanny)
    context = {"job_applications": job_applications}

# confirm if the job application have contracts
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


# employer able to view applicants for specific job he/she posted
@login_required
def job_applications(request, job_id):
    job = jobModel.objects.get(id=job_id)
    # filter the applicants only for the specified job ID
    job_applications = JobApplication.objects.filter(job=job)
    context = {'job': job, 'job_applications': job_applications}
    return render(request, 'jobapp/job_applications.html', context)


# render about us page
def about_us(request):
    return render(request, "jobapp/about_us.html")


# render the help page which has documentation on how to use the platform
def help(request):
    return render(request, "jobapp/help.html")


# The employer can create contract from teh applications received
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
        messages.success(request, "Contract has already been created.")
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

        messages.success("Contract has been created successfully.")

    context = {

        'application': application,
        'contract': contract
    }

    return render(request, 'jobapp/create_contract.html', context)


# nanny accepting/rejecting the contract
def accept_contract(request, contract_id):
    contract = get_object_or_404(ContractModel, id=contract_id)

    if request.method == 'POST':
        if 'accept' in request.POST:
            # Handle contract acceptance
            contract.status = 'active'
            contract.save()
            job_application = JobApplication.objects.get(
                job=contract.job, nanny=contract.nanny)
            job_application.status = 'accepted'
            job_application.save()
            # TODO: Add code to notify the employer of the nanny's acceptance
        elif 'reject' in request.POST:
            # Handle contract rejection
            contract.status = 'terminated'
            contract.save()
            job_application = JobApplication.objects.get(
                job=contract.job, nanny=contract.nanny)
            job_application.status = 'rejected'
            job_application.save()
            # TODO: Add code to notify the employer of the nanny's rejection

        # Redirect to the contract details page
        return redirect('job_application_status')

    context = {
        'contract': contract,
    }

    return render(request, 'jobapp/accept_contract.html', context)


def view_contract(request, contract_id):
    try:
        # Check if contract is a ContractModel
        contract = ContractModel.objects.get(id=contract_id)
        direct_contract = None

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

    except ContractModel.DoesNotExist:
        # Check if contract is a DirectContract
        direct_contract = DirectContract.objects.get(id=contract_id)
        contract = None
        if direct_contract.status == 'active':
            status = "Active"
        elif direct_contract.status == 'terminated':
            status = "Terminated"
        elif direct_contract.status == "accepted":
            status = "Accepted"
        elif direct_contract.status == "rejected":
            status = "Rejected"
        else:
            status = "Pending"

    # Render the template with the contract details and status
    return render(request, "jobapp/view_contract.html", {"contract": contract, "direct_contract": direct_contract, "status": status, })


# employer to view all the contracts that exists
@login_required
def employer_view_all_contracts(request):
    # Get all contracts related to logged-in employer
    contracts = ContractModel.objects.filter(employer=request.user)
    # Get all direct-contracts related to logged-in employer
    direct_contracts = DirectContract.objects.filter(employer=request.user)
    context = {"contracts": contracts, "direct_contracts": direct_contracts}
    # Render the template with the contract list
    return render(request, "jobapp/view_all_contracts.html", context)


@login_required
def nanny_view_all_contracts(request):
    # Get the NannyDetails instance for the logged-in user
    nanny_details = NannyDetails.objects.get(user=request.user)

    # Get all contracts for the nanny
    contracts = ContractModel.objects.filter(nanny=nanny_details)
    direct_contracts = DirectContract.objects.filter(nanny=nanny_details)
    context = {"contracts": contracts, "direct_contracts": direct_contracts}
    # Render the template with the contract list
    return render(request, "jobapp/view_all_contracts.html", context)


# delete the job application
@login_required
def delete_job_application(request, job_application_id):
    # get the specified job application
    job_application = JobApplication.objects.get(id=job_application_id)

    # Check if the current user is the nanny who applied for the job
    if job_application.nanny.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this job application.")

    # Delete the job application
    job_application.delete()

    messages.success(request, 'Job application deleted successfully.')
    return redirect('job_application_status')


# end the contract
@login_required
def end_contract(request, contract_id):
    # Check if it's a ContractModel or DirectContract
    contract = ContractModel.objects.get(id=contract_id)

    # Update the status of the contract to terminated
    contract.status = 'terminated'
    contract.save()

    # Update the status of the job application to terminated
    job_application = get_object_or_404(
        JobApplication, job=contract.job, nanny=contract.nanny)
    job_application.status = 'terminated'
    job_application.save()

    messages.success(request, "Contract has been terminated successfully")
    return redirect("view_all_contracts")


# employer to hire nanny directly
def hire_nanny_direct(request, nanny_id):
    # get the nanny Details
    nanny = NannyDetails.objects.get(id=nanny_id)
    if request.method == 'POST':
        form = DirectContractForm(request.POST)
        # validate direct-contract form
        if form.is_valid():
            contract = form.save(commit=False)
            contract.nanny = nanny
            contract.employer = request.user
            contract.status = 'active'
            contract.save()
            # replace this with your desired redirect
            return redirect('home')
    else:
        form = DirectContractForm()
    context = {'form': form, 'nanny': nanny}
    return render(request, 'jobapp/direct_contract.html', context)


# nanny accept the direct contract
def accept_direct_contract(request, contract_id):
    direct_contract = get_object_or_404(DirectContract, id=contract_id)

    if request.method == 'POST':
        if 'accept' in request.POST:
            # Handle contract acceptance
            direct_contract.status = 'accepted'
            direct_contract.save()
            # TODO: Add code to notify the employer of the nanny's acceptance
        elif 'reject' in request.POST:
            # Handle contract rejection
            direct_contract.status = 'terminated'
            direct_contract.save()
            # TODO: Add code to notify the employer of the nanny's rejection

        # Redirect to the contract details page
        return redirect('view_all_contracts_nanny')

    context = {
        'direct_contract': direct_contract,
    }

    return render(request, 'jobapp/accept_direct_contract.html', context)


# end direct contract
@login_required
def end_direct_contract(request, contract_id):
    # Get the direct contract object
    direct_contract = get_object_or_404(DirectContract, id=contract_id)

    # Update the status of the direct contract to terminated
    direct_contract.status = 'terminated'
    direct_contract.save()

    messages.success(
        request, "Direct contract has been terminated successfully")
    return redirect("view_all_contracts")
