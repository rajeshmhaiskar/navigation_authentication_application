from django.urls import path
from .views import GrantPermissionView, get_schema_table_col_from_server, GrantPrivilegesFunctionValidationView, \
    get_schemas, get_tables, get_columns

urlpatterns = [
    path('create_database_permission', GrantPermissionView.as_view(), name='create_database_permission'),
    path('get_data_for_server/', get_schema_table_col_from_server, name='get_data_for_server'),
    path('grant_validation', GrantPrivilegesFunctionValidationView.as_view(),
         name='grant_validation'),
    path('get_schemas/', get_schemas, name='get_schemas'),
    path('get_tables/', get_tables, name='get_tables'),
    path('get_columns/', get_columns, name='get_columns'),
]
