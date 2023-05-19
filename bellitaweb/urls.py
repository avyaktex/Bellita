from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.index, name='index'),
    path("index/", views.index, name='index'),
    path("success/", views.success, name='success'),
    path("success/index/", views.index, name='index'),
    path("services/", views.services, name='services'),
    path("appointment/index/", views.index, name='index'),
    path("services/services", views.services, name='services'),
    path("success/services/", views.services, name='services'),
    path("appointment/success/", views.success, name='success'),
    path("appointment/", views.appointment, name='appointment'),
    path("appointment/success.html", views.success, name='success'),
    path("success/appointment/", views.appointment, name='appointment'),
    path("services/appointment/", views.appointment, name='appointment'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/profile/', views.dashboard, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/logout/login.html', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]