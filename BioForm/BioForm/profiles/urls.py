import imp
from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.login_page),
    path('profiles/index', views.index, name="home"),
    path('profiles/register', views.register_page, name="register"),
    path('profiles/login', views.login_page, name="login")

]