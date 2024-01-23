# urls.py
from django.urls import path
from .views import login_view, registration_view, dashboard, logout_view, get_schema_table_col_from_server, \
    grant_permission, grant_privileges_function_validation_view, get_tables, get_schemas, get_columns, CustomPasswordChangeView, CustomPasswordChangeDoneView

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_database_permission/', grant_permission, name='create_database_permission'),
    path('grant_validation/', grant_privileges_function_validation_view, name='grant_validation'),
    path('trigger_data_retrieval/', get_schema_table_col_from_server, name='trigger_data_retrieval'),
    path('get_schemas/', get_schemas, name='get_schemas'),
    path('get_tables/', get_tables, name='get_tables'),
    path('get_columns/', get_columns, name='get_columns'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

]
