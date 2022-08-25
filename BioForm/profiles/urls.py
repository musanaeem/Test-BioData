import imp
from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_user),
    path('profiles/index/<int:username>/', views.index, name="home"),
    path('profiles/register', views.register_user, name="register"),
    path('profiles/login', views.login_user, name="login"),
    path('profiles/create/', views.create_record, name="create"),
    path('profiles/logout', views.logout_user,name="logout"),
    path('profiles/update/<int:id>/', views.update_record, name="update"),
    path('profiles/delete/<int:id>/', views.delete_record, name="delete")

]