from django.urls import path
from .views import get_schema_table_col_from_server, grant_permission, grant_privileges_function_validation_view, get_tables, get_schemas, get_columns

urlpatterns = [
    path('create_database_permission/', grant_permission, name='create_database_permission'),
    path('grant_validation/', grant_privileges_function_validation_view, name='grant_validation'),
    path('trigger_data_retrieval/', get_schema_table_col_from_server, name='trigger_data_retrieval'),
    path('get_schemas/', get_schemas, name='get_schemas'),
    path('get_tables/', get_tables, name='get_tables'),
    path('get_columns/', get_columns, name='get_columns'),

]
