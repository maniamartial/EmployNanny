from django.shortcuts import render
from .form import CreateUserForm
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

def nannyRegister(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='nanny')
            user.group.add(group)
            messages.success(request, "Account created sucessfully "+username)
            return redirect('login')
    contex={'form':form}
    return render(request, "users/nannyRegistration.html")

def employRegister(request):
    return render(request, "users/employregistration.html")

def login(request):
    return render(request, 'users/login.html')

def profile(request):
    return render(request, "users/")


