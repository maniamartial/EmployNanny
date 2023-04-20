from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import NannyDetails
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import EmployerProfile
from django.shortcuts import render
from .form import CreateUserForm, nannyDetailsForm, EmployerProfileForm
from django.contrib.auth.models import Group
#from users.decorators import unauthenticated_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
#from django.forms.widgets import EmailInput
from django.shortcuts import redirect, render
from .import form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NannyDetails, EmployerProfile


# Create your views here.
'''
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, "Account created successful "+username)
            return redirect('login')
    context = {'form': form}
    return render(request, "users/regist.html", context)'''

# nanny registration page


def nannyRegister(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='nanny')
            user.groups.add(group)
            messages.success(request, "Account created successful "+username)
            return redirect('login')
    context = {'form': form}
    return render(request, "users/nannyRegistration.html", context)

# employers registration functionality


def employRegister(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='employer')
            user.groups.add(group)
            messages.success(request, "Account created successful "+username)
            return redirect('login')
    context = {'form': form}
    return render(request, "users/employerRegistration.html", context)


# nanny & employer login functionality
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, ' Username or Password is incorrect')
    context = {}
    return render(request, "users/login.html", context)

# nanny or employer profile


def profile(request):
    return render(request, "users/profile.html")

# nanny filling details form


@login_required
def nannyVerificationDetails(request):
    try:
        nanny = NannyDetails.objects.get(user=request.user)
        created = False
    except NannyDetails.DoesNotExist:
        nanny = NannyDetails(user=request.user)
        created = True
    form = nannyDetailsForm(instance=nanny)
    if request.method == "POST":
        form = nannyDetailsForm(request.POST, request.FILES, instance=nanny)
        if form.is_valid():
            nanny = form.save()
            messages.success(
                request, "Your details have been updated successfully.")
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, "users/nannyDetails.html", context)


'''@login_required
def nanny_profile(request):
    nanny = NannyDetails.objects.get(user=request.user)
    context = {
        'nanny': nanny
    }
    return render(request, 'users/nannyProfile.html', context)'''


'''def nanny_profile(request, nanny_id):
    nanny = NannyDetails.objects.get(id=nanny_id)
    context = {
        "nanny": nanny
    }
    return render(request, 'users/nannyProfile.html', context)'''
# rest of the code


def nanny_profile(request, nanny_id):
    try:
        nanny = NannyDetails.objects.get(id=nanny_id)
    except ObjectDoesNotExist:
        return render(request, 'users/user_not_found.html')
    context = {
        "nanny": nanny
    }
    return render(request, 'users/nannyProfile.html', context)


def employer_profile(request, employer_id):
    employer = EmployerProfile.objects.get(id=employer_id)
    context = {
        "employer": employer
    }
    return render(request, 'users/employer_profile.html', context)

# employer can view his/her profile


@login_required
def update_employer_profile(request):
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = EmployerProfileForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('employer_profile')
        else:
            print(form.errors)
    else:
        form = EmployerProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'users/update_employer_profile.html', context)


# logout


def logout_view(request):
    logout(request)
    return redirect('home')
