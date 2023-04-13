from django.urls import path
from . import views

urlpatterns=[
path('nannyRegister', views.nannyRegister, name='nannyRegister'),
path('employerRegister', views.employRegister, name="employerRegister"),
path('login', views.userlogin, name="login"),
path('nannyDetails', views.nannyVerificationDetails, name="nannyDetails"),
path('profile', views.profile, name="profile")
]