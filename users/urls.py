from django.urls import path
from . import views

urlpatterns=[
path('nannyRegister', views.nannyRegister, name='nannyRegister'),
path('employRegister', views.employRegister, name="employRegister"),

]