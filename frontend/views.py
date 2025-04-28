# frontend/views.py
from django.shortcuts import render, redirect
from .forms import HealthProgramForm, ClientForm, EnrollmentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .api_client import api_request
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:  # Only allow staff users
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                token = request.user.auth_token.key
            except Exception:
                return redirect('frontend:get_token')
            
            response = api_request('post', 'clients/', data=data, token=token)

            if response and response.status_code == 201:
                return redirect('frontend:client_list')
            else:
                form.add_error(None, 'Failed to register client. Please try again.')
    else:
        form = ClientForm()
    return render(request, 'frontend/register_client.html', {'form': form})

@login_required
def enroll_client(request):
   
    # Get the API token for the current user
    try:
        token = request.user.auth_token.key
    except Exception:
        return redirect('frontend:get_token')

    # Fetch clients and programs data from the API
    try:
        clients_response = api_request('get', 'clients/list/', token=token)
        programs_response = api_request('get', 'healthprograms/', token=token)

        # If the response is successful, parse the JSON data
        if clients_response.status_code == 200:
            clients = clients_response.json()
        else:
            clients = []

        if programs_response.status_code == 200:
            programs = programs_response.json()
        else:
            programs = []

    except Exception as e:
        messages.error(request, f"Error fetching data: {str(e)}")
        clients = []
        programs = []

    # Handle form submission
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data['client'].id
            program_id = form.cleaned_data['program'].id

            # Prepare data to be sent to the API
            data = {
                'client': client_id,
                'program': program_id,
            }

            # Send the data to the API
            response = api_request('post', 'enroll/', data=data, token=token)
            if response:
                print(f"Response status: {response.status_code}")
                print(f"Response text: {response.text}")
            else:
                print("API request returned None")
            if response and response.status_code == 201:
                messages.success(request, 'Client successfully enrolled in the program.')
                return redirect('frontend:client_list')
            else:
                messages.error(request, f"Failed to enroll client. API response: {response.text}")
        else:
            messages.error(request, 'Invalid form submission.')

    else:
        form = EnrollmentForm()  # Initialize the form

    return render(request, 'frontend/enroll_client.html', {
        'form': form,
        'clients': clients,
        'programs': programs
    })


@login_required
def client_detail(request, client_id):
    # Define the token for authentication
    try:
        token = request.user.auth_token.key
    except Exception:
        return redirect('frontend:get_token')
        
    # Fetch client details from the API
    client_response = api_request('get', f'clients/{client_id}', token=token)
    
    if not client_response or client_response.status_code != 200:
        messages.error(request, "Failed to fetch client details.")
        return redirect('frontend:client_list')  # Redirect to a fallback page
    
    client = client_response.json()  # Assuming the response contains JSON data
    
    # Fetch enrollments for the client from the API
    enrollments_response = api_request('get', f'enrollments/?client={client_id}', token=token)
    
    if not enrollments_response or enrollments_response.status_code != 200:
        messages.error(request, "Failed to fetch enrollments.")
        enrollments = []  # Default to an empty list if enrollments fail to load
    else:
        enrollments = enrollments_response.json()  # Assuming the response contains JSON data
    
    # Render the template with the fetched data
    return render(request, 'frontend/client_detail.html', {
        'client': client,
        'enrollments': enrollments
    })

@login_required
def client_list(request):
    try:
        token = request.user.auth_token.key
    except Exception:
        return redirect('frontend:get_token')
    
    search_query = request.GET.get('q', '')  # Capture search term from query parameter

    if search_query:
        response = api_request('get', f'clients/list/?search={search_query}', token=token)
    else:
        response = api_request('get', 'clients/list/', token=token)

    if response and response.status_code == 200:
        clients = response.json()

    else:
        clients = []

    return render(request, 'frontend/client_list.html', {'clients': clients, 'search_query': search_query})


@admin_required
@login_required
def create_health_program(request):
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                token = request.user.auth_token.key
            except Exception:
                return redirect('frontend:get_token')

            response = api_request('post', 'programs/', data=data, token=token)

            if response and response.status_code == 201:
                return redirect('frontend:health_program_list')
            else:
                form.add_error(None, 'Failed to create health program. Please try again.')
    else:
        form = HealthProgramForm()
    return render(request, 'frontend/create_health_program.html', {'form': form})

@login_required
def health_program_list(request):
    try:
        token = request.user.auth_token.key
    except Exception:
        return redirect('frontend:get_token')

    response = api_request('get', 'healthprograms/', token=token)

    if response and response.status_code == 200:
        programs = response.json()
    else:
        programs = []

    return render(request, 'frontend/health_program_list.html', {'programs': programs})


@login_required
def get_token(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       data = {
                'username': username,
                'password': password,
            }
       response = api_request('post', 'login/', data=data)
       if response and response.status_code == 200:
            return redirect('frontend:health_program_list')
            
       else:
            messages.error(request, 'login failed')
       
    return render(request, 'frontend/api_login.html')

@login_required
def logout(request):
    try:
        token = request.user.auth_token.key
    except Exception:
        return redirect('/login/')

    if token:
        response = api_request('post', 'logout/' ,token=token)
    else:
        response=None

    if response and response.status_code == 200:
        return redirect('/logout')
    else:
        messages.error(request,"logout failed")
    
    return render(request, 'frontend/logout.html')

