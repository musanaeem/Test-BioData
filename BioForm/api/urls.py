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

'''path('api/blogs/', views.blog_list_view, name='api-blog-list'),
    path('api/blog/<int:id>/', views.blog_view, name='api-blog-view'),
    path('api/blogs/user/', views.blog_view_user, name='api-user-blog-view'),
    path('api/blog/new/', views.blog_create, name='api-create-blog'),
    path('api/blog/<int:id>/edit/', views.blog_update, name='api-update-blog'),
    path('api/blog/<int:id>/delete/', views.blog_delete, name='api-delete-blog'),'''