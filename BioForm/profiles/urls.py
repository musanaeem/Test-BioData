from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_user),
    path('home/', views.index, name='home'),
    path('profiles/register/', views.register_user, name='register'),
    path('profiles/login/', views.login_user, name='login'),
    path('profiles/logout', views.logout_user,name='logout'),

    path('profiles/bio/', views.bio_view, name='bio-view'),
    path('profiles/bio/new/', views.bio_create, name='create-bio'),
    path('profiles/bio/<int:id>/edit/', views.bio_update, name='update-bio'),
    path('profiles/bio/<int:id>/delete/', views.bio_delete, name='delete-bio'),
    
    path('blogs/', views.blog_list_view, name='blog-list'),
    path('blogs/new/', views.blog_create, name='create-blog'),
    path('blogs/<int:id>/', views.blog_view, name='blog-view'),
    path('blogs/<int:id>/edit/', views.blog_update, name='update-blog'),
    path('blogs/<int:id>/delete/', views.blog_delete, name='delete-blog'),

]