from rest_framework import serializers
from .models import HealthProgram, Client, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class ClientProfileSerializer(serializers.ModelSerializer):
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'national_id', 'date_of_birth', 'contact', 'programs']

    def get_programs(self, obj):
        return [enrollment.program.name for enrollment in obj.enrollment_set.all()]
