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
    # path('jobs/<int:job_id>/applications/',views.job_applications, name='job_applications'),'''

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
    path('contracts/all/', views.employer_view_all_contracts,
         name='view_all_contracts'),


    # nanny deleting job
    path('job_application/<int:job_application_id>/delete/',
         views.delete_job_application, name='delete_job_application'),


    # end contract - employer
    path('end-contract/<int:contract_id>/',
         views.end_contract, name='end_contract'),


    # nanny view all contracts
    path('contracts/nanny/', views.nanny_view_all_contracts,
         name='view_all_contracts_nanny'),


    # Hire nanny directly
    path('direct_contract/<int:nanny_id>/',
         views.hire_nanny_direct, name='direct_contract'),


    # accepting direct contract
    path('contract/<int:contract_id>/accept-direct/',
         views.accept_direct_contract, name='accept_direct_contract'),


    # end direct contract
    path('direct-contract/<int:contract_id>/end/',
         views.end_direct_contract, name='end_direct_contract'),

    # post review
    path('post_review/<int:contract_id>/',
         views.post_review, name='post_review'),

    path('post_review_nanny/<int:contract_id>/',
         views.post_review_nanny, name='post_review_nanny'),

    path("reviews", views.display_reviews, name="display_reviews"),
    path('help', views.help, name="help")

]
