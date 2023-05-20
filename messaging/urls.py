# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    #path('index/<int:receiver_id>/', views.index, name='index'),
    path('index/<int:job_application_id>/', views.index, name='index'),

    path("<str:room_name>/<int:receiver_id>/", views.room, name="room"),
]
