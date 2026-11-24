from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully! You can now Log In.')
            return redirect('login_user')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
               messages.success(request, f'Welcome Back, {user.username}!')
               return redirect('dashboard')
           else:
               messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.info(request, 'You Have Been Logged Out.')
    return redirect('login_user')

@login_required(login_url = 'login_user')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url = 'login_user')
def secret(request):
    return render(request, 'accounts/secret.html')