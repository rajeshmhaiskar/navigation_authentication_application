from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegistrationView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    DashboardView,
)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
