"""
URL configuration for healthinfo_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from frontend import views as frontend_views  # assuming your custom registration view is in frontend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('frontend/', include('frontend.urls')),

    # Auth
    path('register/', frontend_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='frontend/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='frontend/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='frontend/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='frontend/password_reset_complete.html'), name='password_reset_complete'),

    # Email OTP verification
    path('verify-otp/', frontend_views.verify_otp, name='verify_otp'),
]

