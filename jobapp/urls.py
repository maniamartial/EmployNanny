from os import name

from django.urls import path
from .import views
urlpatterns = [

    path('', views.home, name='home'),
    path('jobPosting', views.jobPosting, name="jobPosting"),
    path('job_listing', views.job_listings, name="job_listing"),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),

    # employer edit job
    path('jobs/<int:job_id>/edit/', views.edit_job,
         name='edit_job'),
    # employer delete the job

    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
]
