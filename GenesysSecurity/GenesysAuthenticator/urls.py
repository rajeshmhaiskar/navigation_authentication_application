# urls.py
from django.urls import path
from .views import login_view, registration_view, dashboard, logout_view, get_schema_table_col_from_server, \
    grant_permission, grant_privileges_function_validation_view, get_schemas_for_database, get_tables_for_schema, \
    get_columns_for_table

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_database_permission/', grant_permission, name='create_database_permission'),
    path('grant_validation/', grant_privileges_function_validation_view, name='grant_validation'),
    path('get_data/', get_schema_table_col_from_server, name='get_data'),
    path('get_schemas_for_database/', get_schemas_for_database, name='get_schemas_for_database'),
    path('get_tables_for_schema/', get_tables_for_schema, name='get_tables_for_schema'),
    path('get_columns_for_table/', get_columns_for_table, name='get_columns_for_table'),

]
