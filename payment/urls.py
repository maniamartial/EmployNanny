from django.urls import path
from . import views
urlpatterns = [
    path('mpesa', views.getAccessToken, name='mpesa'),
    #path('lipa', views.lipa_na_mpesa_online, name='lipa'),
    path('pay', views.showform, name='pay'),
    path('payment_complete', views.payment_complete, name='payment_complete'),
    path("paypal_payments", views.paypal_payment, name="paypal_payment")
]
