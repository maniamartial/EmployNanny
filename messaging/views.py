
from django.db.models import Max
import uuid  # Import the uuid module
from django.shortcuts import get_object_or_404
from .models import Message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from jobapp.models import JobApplication
from users.models import NannyDetails


# Direct client
def direct_contract_index(request, nanny_id):

    job_application = get_object_or_404(NannyDetails, id=nanny_id)
    receiver = job_application
    room_name = str(uuid.uuid4())  # Generate a unique group name using uuid
    return render(request, "chat/index.html", {"receiver": receiver, "room_name": room_name})


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

    # Mark unread messages as seen for the receiver
    unread_messages = messages.filter(receiver=receiver, is_seen=False)
    print(unread_messages)
    if unread_messages.exists() and request.user == receiver:
        unread_messages.update(is_seen=True)

    return render(request, "chat/room.html", {"room_name": room_name, "receiver": receiver, "messages": messages})


def chat_list(request):
    user = request.user

    # Retrieve the latest message for each sender
    latest_messages = Message.objects.filter(receiver=user).values(
        'sender').annotate(max_timestamp=Max('timestamp'))

    # Fetch the complete message objects based on the latest messages
    chats = Message.objects.filter(receiver=user, sender__in=latest_messages.values(
        'sender'), timestamp__in=latest_messages.values('max_timestamp'))

    return render(request, 'chat/chat_list.html', {'chats': chats})
