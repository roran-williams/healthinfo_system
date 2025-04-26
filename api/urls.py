from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', doctor_logout, name='doctor_logout'),
    path('healthprograms/', HealthProgramListView.as_view(), name='list_health_programs'),
    path('programs/', CreateHealthProgramView.as_view(), name='create_program'),
    path('clients/', RegisterClientView.as_view(), name='register_client'),
    path('clients/list/', ClientListView.as_view(), name='list_clients'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('enroll/', EnrollClientView.as_view(), name='enroll_client'),
]
