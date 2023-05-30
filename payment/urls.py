from django.urls import path
from . import views
urlpatterns = [

    # make payment from push stk
    path('pay', views.make_mpesa_payment, name='pay'),

    # return page when the mpesa payment is successful
    path('payment_complete', views.payment_complete, name='payment_complete'),

    # make paypal payment
    path("paypal_payments", views.paypal_payment, name="paypal_payment"),

    path('payment', views.payment_select, name="payment"),

    path('pay_nanny', views.pay_nanny, name="pay_nanny"),
    path('pay_nanny2', views.initiate_b2c_transaction, name="pay_nanny2")
]
