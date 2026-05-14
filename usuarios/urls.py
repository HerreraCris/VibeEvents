# usuarios/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
]