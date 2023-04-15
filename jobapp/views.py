from django.shortcuts import render, redirect, get_object_or_404
from .models import jobModel
from .form import jobPostingForm
from django.contrib.auth.decorators import login_required
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
            return redirect('home')
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
