from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import BlogViewSet

router = DefaultRouter()
router.register(r'api/blog',BlogViewSet, basename='api-blog-view')

urlpatterns = [
    path('api/login/', views.LoginView.as_view(), name='login-api'),
    path('api/register/', views.RegisterView.as_view(), name='register-api'),
    path('api/logout/', views.LogoutView.as_view(), name='logout-api'),

    path('api/bio/', views.BioView.as_view(), name='api-bio-view'),
    path('', include((router.urls, 'api'))),
]

