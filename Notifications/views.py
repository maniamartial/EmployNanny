from .models import Notification
from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.conf import settings


# confirm if teh email was sent and change the boolean
def send_notification_email(notification):
    if not notification.email_sent:
        subject = 'New Notification'
        message = notification.message
        recipient_list = [notification.user.email]
        sender = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, sender, recipient_list)
        notification.email_sent = True
        notification.save()


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/notification_list.html', context)
