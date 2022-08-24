import imp
from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_user),
    path('profiles/index', views.index, name="home"),
    path('profiles/register', views.register_user, name="register"),
    path('profiles/login', views.login_user, name="login")

]