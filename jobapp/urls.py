from os import name

from django.urls import path
from .import views
urlpatterns = [

    path('', views.home, name='home'),
    path('jobPosting', views.jobPosting, name="jobPosting"),
    path('job_listing', views.job_listings, name="job_listings"),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]
