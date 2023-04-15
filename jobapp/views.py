from django.shortcuts import render, redirect, get_object_or_404
from .models import jobModel
from .form import jobPostingForm, JobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


def job_listings(request):
    jobs = jobModel.objects.all().order_by('-date_posted')
    context = {'jobs': jobs}
    return render(request, 'jobapp/joblistings.html', context)


# single job
def job_detail(request, job_id):
    job = get_object_or_404(jobModel, pk=job_id)
    return render(request, 'jobapp/job_detail.html', {'job': job})

# employer to update the job


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
