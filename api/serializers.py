from rest_framework import serializers
from .models import HealthProgram, Client, Enrollment
from django.contrib.auth.models import User

class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'national_id', 'email', 'phone_number', 'address']  # Add the fields you want to allow updating

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'client', 'program', 'program_name', 'enrolled_by', 'date_enrolled']

class ClientProfileSerializer(serializers.ModelSerializer):
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'national_id', 'date_of_birth', 'contact', 'programs']

    def get_programs(self, obj):
        return [enrollment.program.name for enrollment in obj.enrollment_set.all()]
