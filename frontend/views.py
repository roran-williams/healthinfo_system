from django.shortcuts import render

# Create your views here.
# frontend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from api.models import HealthProgram, Client, Enrollment
from .forms import HealthProgramForm, ClientForm, EnrollmentForm

# Health Program Views
def create_health_program(request):
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:health_program_list')
    else:
        form = HealthProgramForm()
    return render(request, 'frontend/create_health_program.html', {'form': form})

def health_program_list(request):
    programs = HealthProgram.objects.all()
    return render(request, 'frontend/health_program_list.html', {'programs': programs})

# Client Views
def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:client_list')
    else:
        form = ClientForm()
    return render(request, 'frontend/register_client.html', {'form': form})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'frontend/client_list.html', {'clients': clients})

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'frontend/client_detail.html', {'client': client})

# Enrollment Views
def enroll_client(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:client_list')
    else:
        form = EnrollmentForm()
    return render(request, 'frontend/enroll_client.html', {'form': form})
