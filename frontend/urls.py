# frontend/urls.py
from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('clients/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    path('create-program/', views.create_health_program, name='create_health_program'),
    path('programs/', views.health_program_list, name='health_program_list'),
    path('program/<int:program_id>/edit/', views.edit_health_program, name='edit_health_program'),
    path('program/<int:program_id>/delete/', views.delete_health_program, name='delete_health_program'),
    path('register-client/', views.register_client, name='register_client'),
    path('clients/', views.client_list, name='client_list'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('enroll/', views.enroll_client, name='enroll_client'),
    path('un-enroll/<int:enrollment_id>/delete/', views.un_enroll_client, name='un_enroll_client'),
]
