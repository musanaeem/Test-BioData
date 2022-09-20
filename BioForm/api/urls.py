from django.urls import path
#from knox import views as knox_views
from . import views

urlpatterns = [
    path('api/user/', views.user_view),
    path('api/login/', views.login),
    path('api/register/', views.register),
    path('api/logout/', views.logout),

    path('api/bio/', views.bio_view, name='api-bio-view'),
    path('api/bio/new', views.bio_create, name='api-create-bio'),
    path('api/bio/<int:id>/edit/', views.bio_update, name='api-update-bio'),
    path('api/bio/<int:id>/delete/', views.bio_delete, name='api-delete-bio'),

    path('api/blogs/', views.blog_list_view, name='api-blog-list'),
    path('api/blog/<int:id>/', views.blog_view, name='api-blog-view'),
    path('api/blogs/user/', views.blog_view_user, name='api-user-blog-view'),
    path('api/blog/new/', views.blog_create, name='api-create-blog'),
    path('api/blog/<int:id>/edit/', views.blog_update, name='api-update-blog'),
    path('api/blog/<int:id>/delete/', views.blog_delete, name='api-delete-blog'),
]