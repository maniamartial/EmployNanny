from django.urls import path
from . import views

urlpatterns = [
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('pdf/', views.GeneratePdfTransactions.as_view(), name='generate-pdf'),
    path('excel/', views.ExportExcelTransactions.as_view(), name='export-excel'),
    path('employers/', views.employers_list, name='employers_list'),
    path('employers/<int:employer_id>/delete/',
         views.delete_employer, name='delete_employer'),

]
