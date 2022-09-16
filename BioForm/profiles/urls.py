from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_user),
    path('profiles/index/', views.index, name="home"),
    path('profiles/register/', views.register_user, name="register"),
    path('profiles/login/', views.login_user, name="login"),
    path('profiles/createbio/', views.create_record, name="create_bio"),
    path('profiles/createblog/', views.create_blog, name="create_blog"),
    path('profiles/logout', views.logout_user,name="logout"),
    path('profiles/update/<int:id>/', views.update_record, name="update"),
    path('profiles/delete/<int:id>/', views.delete_record, name="delete"),
    path('profiles/update-blog/<int:id>/', views.update_blog, name="update-blog"),
    path('profiles/delete-blog/<int:id>/', views.delete_blog, name="delete-blog"),
    path('profiles/blogs/', views.display_blogs, name="blogs"),
    path('profiles/single-blog/<int:id>/', views.display_single_blog, name="single-blog"),
    path('profiles/bio/', views.display_bio, name="bio"),

]