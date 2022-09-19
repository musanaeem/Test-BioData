from django.urls import path
#from knox import views as knox_views
from . import views

urlpatterns = [
    path('api/user/', views.get_user),
    path('api/login/', views.login),
    path('api/register/', views.register),
    path('api/logout/', views.logout),
    path('api/bio/', views.get_bio, name="getbio"),
    path('api/addbio/', views.add_bio, name="addbio"),
    path('api/blogs/', views.get_all_blogs, name="getblogs"),
    path('api/userblogs/', views.get_users_blogs, name="userblogs"),
    path('api/addblog/', views.add_blog, name="addblog"),

    
]