from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm  # <-- Add this import
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Add this import if you have a forms.py with CustomUserCreationForm
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
import requests

User = get_user_model()

# Login page
def user_login(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Prevent login if seller and not approved
            if hasattr(user, 'user_type') and user.user_type == 'seller' and not user.is_approved:
                error = "Your seller account is waiting for admin approval."
            else:
                login(request, user)
                return redirect('users:user_home_page')
        else:
            error = "Invalid credentials"
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})


# Register page
def user_register(request):
    waiting_approval = False
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Use 'role' instead of 'user_type' (matches your form field)
            user.user_type = form.cleaned_data['role']
            if user.user_type == 'seller':
                user.is_seller = True
                user.is_approved = False
                waiting_approval = True
            else:
                user.is_approved = True
            user.save()
            if waiting_approval:
                # Show waiting message after seller registration
                return render(request, 'users/waiting_approval.html')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('users:login')

# User home page
def user_home_page(request):
    return render(request, "users/user_home_page.html")  # Render the user_home_page.html template

# Contact Us View
def contact_us_view(request):
    return render(request, "users/contact_us.html")

# About Us View
def about_us_view(request):
    return render(request, "users/about_us.html")

# Profile View
@login_required
def profile(request):
    if request.method == 'POST' and 'photo' in request.FILES:
        request.user.photo = request.FILES['photo']
        request.user.save()
    return render(request, 'profile.html')

