from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.contrib.auth.models import User

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
