from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('work/', views.work, name='work'),
    path('graph/', views.graph, name='graph'),
    path('close_record', views.close_record, name='close_record'),
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('download_file/', views.download_file, name='download_file'),
    path('pdf/<int:pk>/', views.pdf, name='pdf'),
    path('login/', auth_view.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='jobs/logout.html'), name='logout'),
]
