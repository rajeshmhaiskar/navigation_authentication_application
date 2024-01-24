from django.urls import path
from .views import login_view, registration_view, dashboard, logout_view, CustomPasswordChangeView, CustomPasswordChangeDoneView

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

]
