from django.urls import path
from . import views

urlpatterns = [
    # Transactions
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('excel/', views.ExportExcelTransactions.as_view(), name='export-excel'),
    path('delete_transaction/delete/<int:id>/',
         views.delete_transaction, name="delete_transaction"),

    path('generate_transaction_pdf/', views.generate_transaction_pdf,
         name="generate_transaction_pdf"),

    # Employers
    path('employers/', views.employers_list, name='employers_list'),
    path('delete_employers/<int:id>/',
         views.delete_employer, name='delete_employer'),
    path('reports/employers/pdf/', views.generate_employer_report,
         name='generate_employers_pdf'),


    # Nannies
    path('nannies/', views.nanny_list, name="nanny_list"),
    path('download-nanny-list/', views.generate_nanny_report,
         name='generate_nanny_report'),
    path('nanny-list/delete/<int:id>/',
         views.delete_nanny, name='delete_nanny'),

    path('job_posts/', views.job_post_list, name='job_post_list'),
    path('display_contracts', views.display_contracts, name="display_contracts"),
    path('download-contract-pdf/',
         views.generate_contract_pdf, name='generate_contract_pdf'),
    path('contracts/delete/<int:id>/',
         views.delete_contract, name='delete_contract'),

    path('direct_contracts/delete/<int:id>/',
         views.delete_direct_contract, name='delete_direct_contract'),

    path("employer_payment_report", views.employer_payments,
         name="employer_payment_report"),

    path('employer_payment_history_pdf/', views.employer_payment_history_pdf,
         name='employer_payment_history_pdf'),
    path('user-activity-logs/', views.user_activity_logs,
         name='user_activity_logs'),

    path('chats', views.messages, name="chats"),
    path('chat/delete<int:id>/', views.delete_message, name="delete_message"),

    path("dashboard", views.dashboard, name="dashboard"),
    path('edit-contract/<int:contract_id>/',
         views.edit_contract, name='edit_contract'),
    path('edit-direct-contract/<int:direct_contract_id>/',
         views.edit_direct_contract, name='edit_direct_contract'),

    path('delete_employer/<int:employer_id>/',
         views.delete_employer, name='delete_employer'),


]
