from django.shortcuts import render
from .form import CreateUserForm, nannyDetailsForm
from django.contrib.auth.models import Group
#from users.decorators import unauthenticated_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
#from django.forms.widgets import EmailInput
from django.shortcuts import redirect, render
from .import form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NannyDetails


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


@login_required
def nanny_profile(request):
    nanny = NannyDetails.objects.get(user=request.user)
    context = {
        'nanny': nanny
    }
    return render(request, 'users/nannyProfile.html', context)
