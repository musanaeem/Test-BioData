import imp
from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_user),
    path('profiles/index', views.index, name="home"),
    path('profiles/register', views.register_user, name="register"),
    path('profiles/login', views.login_user, name="login"),
    path('profiles/create/', views.create_record, name="create"),
    path('profiles/update/<str:username>/', views.update_record, name="update"),
    path('profiles/delete/<str:username>/', views.delete_record, name="delete")

]