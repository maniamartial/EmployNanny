"""
URL configuration for Employnannys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('AdminReports.urls')),
    path('', include('jobapp.urls')),
    path('auth/', include('users.urls')),
    path('chat/', include('messaging.urls')),
    path('payment/', include('payment.urls')),
    path('notifications/', include('Notifications.urls')),

    # authentication
    # Password reset form view.
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'),

    # Password reset done view.
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    # Password reset confirmation view.
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # Password reset complete view.
    path('password-reset-complete/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
