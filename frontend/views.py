# frontend/views.py
from pyexpat.errors import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from api.models import HealthProgram, Client, Enrollment
from .forms import HealthProgramForm, ClientForm, EnrollmentForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
import random

# views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm  # Assuming you have a ClientForm

from django.contrib.auth.decorators import login_required

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id, is_deleted=False)

    # Only the creator can edit
    if client.created_by != request.user:
        return redirect('frontend:client_list')

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('frontend:client_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'frontend/edit_client.html', {'form': form})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id, is_deleted=False)

    # Only the creator can delete
    if client.created_by != request.user:
        return redirect('frontend:client_list')

    if request.method == 'POST':
        client.is_deleted = True
        client.save()
        return redirect('frontend:client_list')

    return render(request, 'frontend/confirm_delete_client.html', {'client': client})

# Temporary store OTPs in session (later you can make a model for security)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Deactivate account until email OTP is verified
        user.save()

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp
        request.session['user_id'] = user.id

        # Send OTP to user's email
        send_mail(
            'Your OTP Code',
            f'Your verification code is {otp}',
            'noreply@healthinfo.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, 'We sent a verification code to your email')
        return redirect('verify_otp')
    return render(request, 'frontend/register.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session.get('otp'):
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Clear session
            request.session.pop('otp')
            request.session.pop('user_id')

            messages.success(request, 'Your account has been verified! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')
    return render(request, 'frontend/verify_otp.html')

# Health Program Views
@login_required
def create_health_program(request):
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            messages.success(request, 'Program created successfully!')
            return redirect('frontend:health_program_list')
    else:
        form = HealthProgramForm()
    return render(request, 'frontend/create_health_program.html', {'form': form})

@login_required
def health_program_list(request):
    programs = HealthProgram.objects.filter(is_deleted=False)
    return render(request, 'frontend/health_program_list.html', {'programs': programs})

@login_required
def edit_health_program(request, program_id):
    program = get_object_or_404(HealthProgram, pk=program_id, is_deleted=False)

    if program.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this program.")

    if request.method == 'POST':
        form = HealthProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect('frontend:health_program_list')
    else:
        form = HealthProgramForm(instance=program)
    
    return render(request, 'frontend/edit_health_program.html', {'form': form})

@login_required
def delete_health_program(request, program_id):
    program = get_object_or_404(HealthProgram, pk=program_id, is_deleted=False)

    if program.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this program.")

    if request.method == 'POST':
        program.is_deleted = True
        program.save()
        messages.success(request, "Program deleted successfully!")
        return redirect('frontend:health_program_list')

    return render(request, 'frontend/confirm_delete_program.html', {'program': program})

# Client Views
@login_required
def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user  # 🛠️ Set the creator
            client.save()
            return redirect('frontend:client_list')
    else:
        form = ClientForm()
    return render(request, 'frontend/register_client.html', {'form': form})

@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user, is_deleted=False)
    return render(request, 'frontend/client_list.html', {'clients': clients})

@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    enrollments = Enrollment.objects.filter(client=client)
    return render(request, 'frontend/client_detail.html', {'client': client, 'enrollments': enrollments})

# Enrollment Views
@login_required
def enroll_client(request):
    clients = Client.objects.filter(created_by=request.user, is_deleted=False)
    programs = HealthProgram.objects.filter(created_by=request.user, is_deleted=False)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.enrolled_by = request.user
            form.save()
            messages.success(request,'client succesfully enrolled')
            return redirect('frontend:client_list')
        else:
            messages.error(request,'is the client already registered on that program?')
            return redirect('frontend:enroll_client')
    else:
        form = EnrollmentForm()
    return render(request, 'frontend/enroll_client.html', {'form': form, 'clients':clients, 'programs':programs})

@login_required
def un_enroll_client(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    # Only the creator can delete
    if enrollment.enrolled_by != request.user:
        messages.error(request,'you cant un-enroll')
        return redirect('frontend:client_list')

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request,'done')
        return redirect('frontend:client_list')

    return render(request, 'frontend/confirm_un_enroll_client.html', {'enrollment': enrollment})
