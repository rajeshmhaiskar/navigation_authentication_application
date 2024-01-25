from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from .models import MasterDatabase, DatabaseAccess, MasterDatabaseSchema, DatabasePermission, DatabaseTable, \
    SchemaAccess
from .postgresql_fun_call import grant_database_privileges, grant_function_validation_privileges
from .get_schema_table_column import get_remote_schemas_tables_columns, save_to_local_database


def get_data_for_server(database, databases_for_server):
    try:
        master_db = MasterDatabase.objects.get(database_name=database, is_active=True)
    except MasterDatabase.DoesNotExist:
        raise Http404("MasterDatabase not found with the given conditions.")

    remote_database = master_db.database_name
    remote_user = master_db.username
    remote_password = master_db.password
    remote_host = master_db.server_ip
    remote_port = master_db.port

    remote_db_params = {
        'host': remote_host,
        'user': remote_user,
        'password': remote_password,
        'database': remote_database,
        'port': remote_port,
    }

    return remote_database, get_remote_schemas_tables_columns(remote_db_params)
