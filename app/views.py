from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

# Create your views here.
def index(request):
    if request.session.get('user_id') and request.session.get('user_type'):
        return redirect('dashboard')
    return render(request, 'index.html')

def register_user(request):
    if request.session.get('user_id') and request.session.get('user_type'):
        return redirect('dashboard')

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login') 
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserProfileForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.session.get('user_id') and request.session.get('user_type'):
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_type'] = user.user_type
                return redirect('dashboard') 
            else:
                error_message = "Invalid credentials. Please try again."
        except UserProfile.DoesNotExist:
            error_message = "User does not exist. Please register first."
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_user(request):
    request.session.flush() 
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def dashboard(request):
    user_type = request.session.get('user_type')

    if user_type == 'doctor':
        return render(request, 'doctor_dashboard.html')
    elif user_type == 'patient':
        return render(request, 'patient_dashboard.html')
    else:
        return redirect('login')
