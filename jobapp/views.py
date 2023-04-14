from django.shortcuts import render, redirect
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

        