from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm
from GenesysAuthenticator.postgresql_fun_call import create_user_condition_check_validations
from .models import MasterDatabase, UserDetails
from GenesysAuthenticator.models import *


class LoginView(FormView):
    template_name = 'GenesysUserApp/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)


class LogoutView(TemplateView):
    template_name = 'GenesysUserApp/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class RegistrationView(FormView):
    template_name = 'GenesysUserApp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'Registration successful. You are now logged in.'

    def form_valid(self, form):
        try:
            username = form.cleaned_data['emp_id']
            password = form.cleaned_data['password2']
            selected_database_ids = self.request.POST.getlist('selected_databases', [])
            selected_databases = MasterDatabase.objects.filter(id__in=selected_database_ids)

            for database in selected_databases:
                create_user_condition_check_validations(username, password, database)

            user = form.save()
            database_access = DatabaseAccess.objects.create(user=user)
            database_access.databases.set(selected_databases)

            # login(self.request, user)

        except Exception as e:
            print(f"Error during registration: {e}")
            form.add_error(None, 'An error occurred during registration. Please try again.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form is not valid. Please correct the errors.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'GenesysUserApp/change_password.html'
    success_url = reverse_lazy('password_change_done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'GenesysUserApp/password_change_done.html'


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'GenesysUserApp/dashboard.html'
