from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import JobApplication
from django.shortcuts import render, redirect
from .models import jobModel, ContractModel
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import jobModel
from .form import jobPostingForm, JobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import NannyDetails

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

    return render(request, 'jobapp/application_status.html', context)
