from django.urls import reverse
from django.shortcuts import render, redirect
from jobapp.models import Rating
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from .form import CreateUserForm, nannyDetailsForm, EmployerProfileForm
from django.contrib.auth.models import Group
# from users.decorators import unauthenticated_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
# from django.forms.widgets import EmailInput
from .import form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NannyDetails, EmployerProfile


# create nanny registration function
def nannyRegister(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='nanny')
            user.groups.add(group)
            #nanny_details = NannyDetails.objects.create(user=user)

            messages.success(request, "Account created successful "+username)
            return redirect('login')
    context = {'form': form}
    return render(request, "users/nannyRegistration.html", context)


# employers registration functionality
def employRegister(request):
    # get the form fields
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        # validate the form
        if form.is_valid():
            user = form.save()
            # get the username from the form
            username = form.cleaned_data.get('username')
            # get the group name from the database
            group = Group.objects.get(name='employer')
            # save the user as per teh specified group
            user.groups.add(group)
            messages.success(request, "Account created successful "+username)
            return redirect('login')
    context = {'form': form}
    return render(request, "users/employerRegistration.html", context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                # Replace 'home' with the desired URL name
                return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {'next': request.GET.get('next')}
    return render(request, "users/login.html", context)

# nanny to fill in more details


@login_required
def nanny_verification_details(request):
    # check first if the nanny has already filled the details
    try:
        nanny = NannyDetails.objects.get(user=request.user)
        created = False
    except NannyDetails.DoesNotExist:
        nanny = NannyDetails(user=request.user)
        created = True

    # from generated should be an instance of nanny, which means it updated the data o existing nanny
    form = nannyDetailsForm(instance=nanny)
    if request.method == "POST":
        # form should take both files and raw data
        form = nannyDetailsForm(request.POST, request.FILES, instance=nanny)
        # validate the form
        if form.is_valid():
            nanny = form.save()
            messages.success(
                request, "Your details have been updated successfully.")
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, "users/nannyDetails.html", context)


# show specified nanny profile with all the details


def nanny_profile(request, nanny_id):
    try:
        nanny = NannyDetails.objects.get(id=nanny_id)
    except ObjectDoesNotExist:
        return render(request, 'users/404.html')

    ratings = Rating.objects.filter(receiver=nanny.user)
    # Calculate the average rating of the nanny

    context = {
        "nanny": nanny,
        "ratings": ratings,
        "ratings": ratings
    }
    return render(request, 'users/nannyProfile.html', context)


# create employer profile
@login_required
def create_employer_profile(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assuming the current user is authenticated
            profile.save()
            # Replace 'profile' with the URL or name of the profile view
            return redirect('employer_profile', employer_id=profile.id)
    else:
        form = EmployerProfileForm()

    return render(request, 'users/create_employer_profile.html', {'form': form})


# show the employer details
def employer_profile(request, employer_id):
    # check if employer exists
    try:
        # get the specified employer
        employer = EmployerProfile.objects.get(id=employer_id)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')
    # display the details
    context = {
        "employer": employer
    }
    return render(request, 'users/employer_profile.html', context)


# employer can view his/her profile
@ login_required
def update_employer_profile(request):
    # check if the logged-in employer has details
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')

# change/modify some details
    if request.method == 'POST':
        form = EmployerProfileForm(
            request.POST, request.FILES, instance=profile)
        # if form is valid, save in the database
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('employer_profile', employer_id=profile.id)
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


# handle any nt found error
def handler404(request, exception):
    return render(request, 'users/404.html', status=404)
