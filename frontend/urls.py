# frontend/urls.py
from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('create-program/', views.create_health_program, name='create_health_program'),
    path('programs/', views.health_program_list, name='health_program_list'),
    path('register-client/', views.register_client, name='register_client'),
    path('clients/', views.client_list, name='client_list'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('enroll/', views.enroll_client, name='enroll_client'),
]
