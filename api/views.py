from django.shortcuts import render
from rest_framework import generics
from .models import HealthProgram, Client, Enrollment
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doctor_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully."})


class CreateHealthProgramView(generics.CreateAPIView):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class RegisterClientView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EnrollClientView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientProfileSerializer

class HealthProgramListView(generics.ListAPIView):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer