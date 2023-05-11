from django.urls import path
from . import views

urlpatterns = [
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('pdf/', views.GeneratePdfTransactions.as_view(), name='generate-pdf'),
    path('excel/', views.ExportExcelTransactions.as_view(), name='export-excel'),
    path('employers/', views.employers_list, name='employers_list'),
    path('employers/<int:user_id>/delete/',
         views.delete_employer, name='delete_employer'),


    path('reports/employers/pdf/', views.generate_employer_report,
         name='generate_employers_pdf'),

    path('nannies/', views.nanny_list, name="nanny_list"),
    path('download-nanny-list/', views.generate_nanny_report,
         name='generate_nanny_report'),

    path('reports/nanny-list/delete/<int:id>/',
         views.delete_nanny, name='delete_nanny'),

    path('job_posts/', views.job_post_list, name='job_post_list'),
    path('display_contracts', views.display_contracts, name="display_contracts"),
    path('download-contract-pdf/',
         views.generate_contract_pdf, name='generate_contract_pdf'),
    path('contracts/delete/<int:id>/',
         views.delete_contract, name='delete_contract'),

    path('direct_contracts/delete/<int:id>/',
         views.delete_direct_contract, name='delete_direct_contract'),



]
