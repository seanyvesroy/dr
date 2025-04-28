from django.shortcuts import render
from .models import Doctor, User
from .forms import DoctorSearchForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def index(request):
    return render(request, "vouch/index.html")
def search(request):
    if request.method == 'POST':
        form = DoctorSearchForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['fName']
            last_name = form.cleaned_data['lName']
            specialty = form.cleaned_data['specialty']
            conditions_treated = form.cleaned_data['conditions_treated']
            zip_code = form.cleaned_data['zip_code']

            filter_args = {}
            if first_name:
                filter_args['first_name__icontains'] = first_name
            if last_name:
                filter_args['last_name__icontains'] = last_name
            if specialty:
                filter_args['specialty'] = specialty
            if zip_code:
                filter_args['zip_code'] = zip_code
            if conditions_treated:
                filter_args['conditions_treated'] = conditions_treated

            doctors = Doctor.objects.filter(**filter_args).distinct()

            return render(request, 'vouch/search.html', {'doctors': doctors, 'form': form})
    else:
        form = DoctorSearchForm()

    return render(request, 'vouch/search.html', {'form': form})

def loginAttempt(request):
    if request.method == 'GET':
        return render(request, "vouch/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, "vouch/index.html")
        else:
            return render(request, "vouch/login.html", {'error': 'Invalid username or password'})
    
def logoutAttempt(request):
    auth_logout(request)
    return render(request, "vouch/index.html")

def changePassword(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return render(request, "vouch/changePassword.html")
        else:
            return render(request, "vouch/login.html", {'error': 'Invalid username or password'})

def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
        if user:
            # Here you would typically send an email with a password reset link
            return render(request, "vouch/index.html", {'message': 'Password reset link sent to your email.'})
        else:
            return render(request, "vouch/forgotPassword.html", {'error': 'User not found.'})
    return render(request, "vouch/forgotPassword.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        reenter_password = request.POST['reenter_password']
        
        errors = []  # <--- Collect multiple errors here
        
        if password != reenter_password:
            errors.append('Passwords do not match.')
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        if User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password):
            errors.append('Password must contain at least one digit.')
        if not any(char.isalpha() for char in password):
            errors.append('Password must contain at least one letter.')
        if not any(char in "!@#$%^&*()-_+=<>?/|{}[]:;'" for char in password):
            errors.append('Password must contain at least one special character.')
        if not any(char.isupper() for char in password):
            errors.append('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            errors.append('Password must contain at least one lowercase letter.')

        # If there are any errors, re-render the signup page with them
        if errors:
            return render(request, "vouch/signup.html", {'errors': errors})
        else:
        # Otherwise, create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)
            return render(request, "vouch/index.html", {'message': 'User created successfully.'})
    return render(request, "vouch/signup.html")
    