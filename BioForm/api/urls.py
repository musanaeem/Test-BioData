from django.urls import path
#from knox import views as knox_views
from . import views

urlpatterns = [
    path('api/login/', views.LoginView.as_view()),
    path('api/register/', views.RegisterView.as_view),
    path('api/logout/', views.LogoutView.as_view()),

    path('api/bio/', views.BioView.as_view(), name='api-bio-view'),

    path('api/blogs/', views.BlogListView.as_view(), name='api-blog-list'),
    path('api/blogs/user/', views.BlogUserView.as_view(), name='api-user-blog'),
    path('api/blogs/<int:id>', views.BlogDetailedView.as_view(), name='api-blog'),
    
]
