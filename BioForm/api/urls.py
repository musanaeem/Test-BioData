from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import BlogViewSet

app_name = 'api'

router = DefaultRouter()
router.register('api/blog',BlogViewSet, basename='api-blog-view')

urlpatterns = [
    path('api/login/', views.LoginView.as_view()),
    path('api/register/', views.RegisterView.as_view()),
    path('api/logout/', views.LogoutView.as_view()),

    path('api/bio/', views.BioView.as_view(), name='api-bio-view'),
]

urlpatterns += router.urls
