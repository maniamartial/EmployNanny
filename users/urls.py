from django.urls import path
from . import views

urlpatterns = [
    path('nannyRegister', views.nannyRegister, name='nannyRegister'),
    path('employerRegister', views.employRegister, name="employerRegister"),
    path('login', views.userlogin, name="login"),
    path('nannyDetails', views.nannyVerificationDetails, name="nannyDetails"),

    #path('nanny_profile/', views.nanny_profile, name='nanny_profile'),
    path('nanny_profile/<int:nanny_id>/',
         views.nanny_profile, name='nanny_profile'),

    path('update_employer_profile', views.update_employer_profile,
         name="update_employer_profile"),

    path('employer_profile/<int:employer_id>/', views.employer_profile,
         name="employer_profile"),

    # logout
    path('logout/', views.logout_view, name='logout'),


]
