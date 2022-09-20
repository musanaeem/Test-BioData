from django.urls import path
#from knox import views as knox_views
from . import views

urlpatterns = [
    path('api/user/', views.get_user),
    path('api/login/', views.login),
    path('api/register/', views.register),
    path('api/logout/', views.logout),
    path('api/bio/', views.get_bio, name='get-bio'),
    path('api/add-bio/', views.add_bio, name='add-bio'),
    path('api/update-bio/<int:id>/', views.update_bio, name='update-bio'),
    path('api/delete-bio/<int:id>/', views.delete_bio, name='delete-bio'),
    path('api/blogs/', views.get_all_blogs, name='get-blogs'),
    path('api/user-blogs/', views.get_users_blogs, name='user-blogs'),
    path('api/add-blog/', views.add_blog, name='addblog'),
    path('api/update-blog/<int:id>/', views.update_blog, name='update-blog'),
    path('api/delete-blog/<int:id>/', views.delete_blog, name='deleteb-log'),
]