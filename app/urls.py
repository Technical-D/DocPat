from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('blog/create', views.create_blog, name='create_blog'),
    path('blog/my-blogs/', views.my_blogs, name='my_blogs'),
    path('blog/all-blogs/', views.all_blogs, name='all_blogs'),
]
