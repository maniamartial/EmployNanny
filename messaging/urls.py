# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    #path('index/<int:receiver_id>/', views.index, name='index'),
    path('index/<int:job_application_id>/', views.index, name='index'),

    # Direct contract messaging
    path('direct_contract_index/<int:nanny_id>/', views.direct_contract_index,
         name="direct_contract_index"),

    path("<str:room_name>/<int:receiver_id>/", views.room, name="room"),
    path("chat_list", views.chat_list, name="chat_list")
]
