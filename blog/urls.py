from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogpost_home, name='blogpost_home'),
    path('blog_post/<int:pk>/', views.show_blogpost, name='show_blogpost'),
    path('authers_blogpost/<int:pk>/', views.show_authors_blogpost, name='show_authors_blogpost'),
    path('create_blogpost/', views.create_blogpost, name='create_blogpost'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('save_commentreply/<int:comment_pk>/', views.save_commentreply, name='save_formreply'),
]