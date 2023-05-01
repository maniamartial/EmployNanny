from django.urls import path

from . import views
handler404 = views.handler404
urlpatterns = [
    # URL for the nanny registration form
    path('nannyRegister', views.nannyRegister, name='nannyRegister'),

    # URL for the employer registration form
    path('employerRegister', views.employRegister, name="employerRegister"),

    # URL for the user login form
    path('login', views.user_login, name="login"),

    # URL for the nanny verification form
    path('nannyDetails', views.nanny_verification_details, name="nannyDetails"),

    # URL for the nanny profile page
    # The parameter <int:nanny_id> specifies an integer value that will be used to identify the nanny
    path('nanny_profile/<int:nanny_id>/',
         views.nanny_profile, name='nanny_profile'),

    # URL for the employer profile update form
    path('update_employer_profile', views.update_employer_profile,
         name="update_employer_profile"),

    # URL for the employer profile page
    # The parameter <int:employer_id> specifies an integer value that will be used to identify the employer
    path('employer_profile/<int:employer_id>/',
         views.employer_profile, name="employer_profile"),

    # URL for logging out the user
    path('logout/', views.logout_view, name='logout'),

    # URL for handling 404 errors
    path('handler404', views.handler404, name="handler404")
]
