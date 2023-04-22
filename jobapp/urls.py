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
    path("nannies", views.show_all_nannies, name="nannies"),

    # contract
    # path('contract/<int:job_id>/', views.create_contract, name='contract'),

    # nanny tracking teh jobs aplication status
    path("job_application_status", views.application_status,
         name="job_application_status"),

    # nanny applying for job
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),

    # view applications made on a job
    path('jobs/<int:job_id>/applications/',
         views.job_applications, name='job_applications'),

    # about page
    path("about_us", views.about_us, name="about_us"),

    # creating contract
    path('contracts/create/<int:application_id>/',
         views.create_contract_and_start_duration, name='create_contract'),



    # path for accepting contract by nanny
    path('accept-contract/<int:contract_id>/',
         views.accept_contract, name='accept_contract'),

    # viewing coontract
    path('contracts/<int:contract_id>/',
         views.view_contract, name='view_contract'),


    # employer to view all contracts
    path('contracts/all/', views.view_all_contracts, name='view_all_contracts'),

    path('contracts/all/', views.view_all_contracts_nanny,
         name='view_all_contracts_nanny'),


]
