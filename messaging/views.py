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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    users = User.objects.all()  # Get all registered users
    return render(request, "chat/index.html", {"users": users})


@login_required
def room(request, room_name, receiver_id):
    # Get the receiver using the receiver_id
    receiver = User.objects.get(id=receiver_id)
    return render(request, "chat/room.html", {"room_name": room_name, "receiver": receiver})
