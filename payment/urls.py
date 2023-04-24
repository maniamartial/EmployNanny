from django.urls import path
from . import views
urlpatterns = [
    path('mpesa', views.getAccessToken, name='mpesa'),
    #path('lipa', views.lipa_na_mpesa_online, name='lipa'),
    path('pay', views.showform, name='pay'),
    # path('paymentcomplete', views.thankspayment, name='paymentcomplete'),
]
