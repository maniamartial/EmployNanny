from django.urls import path
from . import views
urlpatterns = [

    # make payment from push stk
    #path('pay', views.make_mpesa_payment, name='pay'),

    # return page when the mpesa payment is successful
    path('payment_complete', views.payment_complete, name='payment_complete'),

    # make paypal payment
    path("paypal_payments", views.paypal_payment, name="paypal_payment"),

    path('payment', views.payment_select, name="payment"),


    #path('pay_nanny', views.initiate_b2c_transaction, name="pay_nanny")
    path('initiate-payment/<int:contract_id>/',
         views.initiate_b2c_transaction, name='initiate_payment'),

    path('employer_transaction_report',
         views.employer_report, name="employer_transaction_report"),

    path('generate_employer_transaction', views.generate_employer_transaction,
         name="generate_employer_transaction"),

    path('nanny_transaction_report', views.nanny_transaction_report,
         name="nanny_transaction_report"),
    path('generate_nanny_transaction/', views.generate_nanny_transaction,
         name="generate_nanny_transaction"),

    # Dealing with advance payment
    path('advance-payment/<int:contract_id>/',
         views.advance_payment, name='advance_payment'),

]
