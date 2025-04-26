# frontend/forms.py
from django import forms
from api.models import HealthProgram, Client, Enrollment

class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'national_id', 'date_of_birth', 'contact']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['client', 'program']
