from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import BlogViewSet

app_name = 'api'

router = DefaultRouter()
router.register('api/blogview',BlogViewSet, basename='blog')

urlpatterns = [
    path('api/login/', views.LoginView.as_view()),
    path('api/register/', views.RegisterView.as_view),
    path('api/logout/', views.LogoutView.as_view()),

    path('api/bio/', views.BioView.as_view(), name='api-bio-view'),
]

urlpatterns += router.urls

'''
    path('api/blogs/', views.BlogListView.as_view(), name='api-blog-list'),
    path('api/blogs/user/', views.BlogUserView.as_view(), name='api-user-blog'),
    path('api/blogs/<int:id>', views.BlogDetailedView.as_view(), name='api-blog'),
''' 