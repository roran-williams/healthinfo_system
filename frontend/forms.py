# frontend/forms.py
from django import forms
from api.models import HealthProgram, Client, Enrollment

class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description',]
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3,'class':'form-control'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'national_id', 'date_of_birth', 'contact']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['client', 'program']
