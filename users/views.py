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

#nanny registration page
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

#employers registration functionality
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


#nanny & employer login functionality
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

#nanny or employer profile
def profile(request):
    return render(request, "users/profile.html")

#nannydetails to be filled before job application
def nannyDetails(request):
    form=nannyDetailsForm()
    if request.method=="POST":
        form=nannyDetailsForm(request.POST)
        if form.is_valid():
            user=form.save()
            first_name=form.cleaned_data('first_name')
            last_name=form.cleaned_data('last_name')
            name=first_name+' '+last_name
            messages.success(name+ ", your details updated successfully")
            return redirect('profile')
    context={'form':form}
    return render(request, "users/nannyDetailsForm")

