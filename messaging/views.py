'''from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user


def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    receiver = get_user(request)  # Get the receiver, who is the logged-in user
    return render(request, "chat/room.html", {"room_name": room_name, "receiver": receiver})
'''
import uuid  # Import the uuid module
from django.shortcuts import get_object_or_404
from .models import Message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from jobapp.models import JobApplication

'''
def index(request):
    users = User.objects.all()  # Get all registered users
    return render(request, "chat/index.html", {"users": users})
'''


'''def index(request, job_application_id):
    job_application = get_object_or_404(JobApplication, id=job_application_id)
    # Assuming the nanny is stored as a foreign key in the JobApplication model
    receiver = job_application.nanny
    # Get all registered users except the current user
    return render(request, "chat/index.html", {"receiver": receiver})'''


def index(request, job_application_id):

    job_application = get_object_or_404(JobApplication, id=job_application_id)
    receiver = job_application.nanny
    room_name = str(uuid.uuid4())  # Generate a unique group name using uuid
    return render(request, "chat/index.html", {"receiver": receiver, "room_name": room_name})


@login_required
def room(request, room_name, receiver_id):
    sender = request.user
    receiver = User.objects.get(id=receiver_id)

    # Retrieve previous chat messages between sender and receiver
    messages = Message.objects.filter(sender=sender, receiver=receiver).order_by('timestamp') | Message.objects.filter(
        sender=receiver, receiver=sender).order_by('timestamp')

    return render(request, "chat/room.html", {"room_name": room_name, "receiver": receiver, "messages": messages})
