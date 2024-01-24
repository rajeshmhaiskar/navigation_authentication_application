from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError
from .forms import RegistrationForm
from GenesysAuthenticator.postgresql_fun_call import create_user_condition_check_validations
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import *
from GenesysAuthenticator.models import *


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'GenesysUserApp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def registration_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('emp_id')
            password = request.POST.get('password2')
            selected_database_ids = request.POST.getlist('selected_databases', [])
            selected_databases = MasterDatabase.objects.filter(id__in=selected_database_ids)

            for database in selected_databases:
                create_user_condition_check_validations(username, password, database)

            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                database_access = DatabaseAccess.objects.create(user=user)

                # Add selected databases and  DatabaseAccess entry
                database_access.databases.add(*selected_databases)

                # login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('login')
            else:
                messages.error(request, 'Form is not valid. Please correct the errors.')
        except Exception as e:
            print(f"Error during registration: {e}")
            messages.error(request, 'An error occurred during registration. Please try again.')

    else:
        form = RegistrationForm()

    return render(request, 'GenesysUserApp/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'GenesysUserApp/change_password.html'
    success_url = reverse_lazy('password_change_done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'GenesysUserApp/password_change_done.html'


def dashboard(request):
    return render(request, 'GenesysUserApp/dashboard.html')
