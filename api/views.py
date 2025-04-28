# api/views.py

from rest_framework import generics
from .models import HealthProgram, Client, Enrollment
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .registration import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_clients(request):
    clients = Client.objects.filter(created_by=request.user, is_deleted=False)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


class CreateHealthProgramView(generics.CreateAPIView):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class RegisterClientView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegistrationSerializer

class EnrollClientView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name','national_id']

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientProfileSerializer

class HealthProgramListView(generics.ListAPIView):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class EnrollmentListView(generics.ListAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['program', 'client', 'enrolled_by']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client', None)
        if client_id is not None:
            queryset = queryset.filter(client_id=client_id)  # Filter enrollments by client
        return queryset

