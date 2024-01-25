# from django.contrib import messages
# from django.db import IntegrityError
# from .forms import GrantPermissionForm, PrivilegeFunctionValidationForm
# from .postgresql_fun_call import *
# from .models import MasterDatabase, DatabaseAccess, MasterDatabaseSchema, DatabasePermission, \
#     DatabaseTable, SchemaAccess
# from django.contrib.auth.decorators import login_required
# from .custom_decorator import designation_required
# from django.shortcuts import render, redirect
# from .get_schema_table_column import get_remote_schemas_tables_columns, save_to_local_database
# from django.http import Http404, JsonResponse
# import json
# from django.urls import reverse_lazy
#
#
# @login_required
# @designation_required('Senior Vice President - Projects', 'Vice President', 'General Manager Projects',
#                       'Senior Project Manager', 'Program Manager', 'Manager')
# def grant_permission(request):
#     if request.method == 'POST':
#         form = GrantPermissionForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = cleaned_data['user']
#             granted_by = request.user
#             database_name = cleaned_data['database']
#             func_n = 'dum_func'
#             db_access = cleaned_data.get('db_access', False)
#             privilege_select = cleaned_data.get('privilege_select', False)
#             privilege_insert = cleaned_data.get('privilege_insert', False)
#             privilege_update = cleaned_data.get('privilege_update', False)
#             privilege_delete = cleaned_data.get('privilege_delete', False)
#             privilege_sequence = cleaned_data.get('privilege_sequence', False)
#             schemas = cleaned_data.get('schemas', [])
#
#             # Extract schema names from the QuerySet
#             schema_names = list(schemas.values_list('schema', flat=True))
#
#             # Call the utility function to grant database privileges
#             result = grant_database_privileges(user, schema_names, database_name, func_n, db_access, privilege_select,
#                                                privilege_insert, privilege_update, privilege_delete,
#                                                privilege_sequence)
#
#             if result:
#                 # Save the form data to the DatabasePermission model
#                 database_permission = form.save(commit=False)
#                 database_permission.granted_by = granted_by
#
#                 # Save the instance to get an ID
#                 database_permission.save()
#
#                 # Set the selected schemas on the DatabasePermission instance
#                 database_permission.schemas.set(schemas)
#
#                 messages.success(request, 'Database permission granted successfully.')
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, f"Error: {result}")
#         else:
#             messages.error(request, 'Error: Form is not valid.')
#     else:
#         form = GrantPermissionForm()
#
#     return render(request, 'GenesysAuthenticator/database_permission_form.html', {'form': form})
#
#
# def get_data_for_server(database, databases_for_server):
#     try:
#         master_db = MasterDatabase.objects.get(database_name=database, is_active=True)
#     except MasterDatabase.DoesNotExist:
#         raise Http404("MasterDatabase not found with the given conditions.")
#
#     remote_database = master_db.database_name
#     remote_user = master_db.username
#     remote_password = master_db.password
#     remote_host = master_db.server_ip
#     remote_port = master_db.port
#
#     remote_db_params = {
#         'host': remote_host,
#         'user': remote_user,
#         'password': remote_password,
#         'database': remote_database,
#         'port': remote_port,
#     }
#
#     return remote_database, get_remote_schemas_tables_columns(remote_db_params)
#
#
# @login_required
# def get_schema_table_col_from_server(request):
#     if request.method == 'POST':
#         remote_databases = MasterDatabase.objects.values_list('database_name', flat=True).distinct()
#
#         databases_for_server1 = ["highfidelity", "poi_core", "WoNoRoadNetwork"]
#         databases_for_server2 = ["xyz", "abcd", "db_fight"]
#
#         for database in remote_databases:
#             if database in databases_for_server1 or database in databases_for_server2:
#                 remote_database, data = get_data_for_server(database, databases_for_server1 + databases_for_server2)
#                 save_to_local_database(remote_database, data)
#             else:
#                 print("Error: Unsupported database")
#
#         print("Data retrieval and saving to local database complete.")
#
#         # Redirect to the dashboard after successful data retrieval
#         return redirect('dashboard')  # Replace 'dashboard' with the actual name or URL of your dashboard view
#
#     return render(request, 'GenesysAuthenticator/trigger_data_retrieval.html')
#
#
# @login_required
# @designation_required('Senior Vice President - Projects', 'Vice President', 'General Manager Projects',
#                       'Senior Project Manager', 'Program Manager', 'Manager')
# def grant_privileges_function_validation_view(request):
#     all_columns = set()
#     for table in DatabaseTable.objects.all():
#         all_columns.update(table.columns.split(','))
#
#     if request.method == 'POST':
#         print(request.POST)
#         database_id = request.POST.get('database')
#         schema_id = request.POST.get('schema')
#         table_id = request.POST.get('table')
#         form = PrivilegeFunctionValidationForm(request.POST)
#         if form.is_valid():
#             privilege_validation_instance = form.save(commit=False)
#             privilege_validation_instance.granted_by = request.user
#
#             try:
#                 privilege_validation_instance.save()
#             except IntegrityError as e:
#                 print(f"IntegrityError: {e}")
#
#             user = request.user
#             database_name = MasterDatabase.objects.get(id=database_id).database_name
#             schema_name = MasterDatabaseSchema.objects.get(id=schema_id).schema
#             table_name = DatabaseTable.objects.get(id=table_id).table_name
#             column_name = request.POST.get('columns')
#             # privilege_function_validation = request.POST.get('privilege_function_validation')
#             # Call the second function with stored values
#             result = grant_function_validation_privileges(
#                 user,
#                 schema_name,
#                 table_name,
#                 column_name,
#                 # privilege_function_validation,
#                 database_name,
#             )
#
#             # Create or update an entry in the SchemaAccess table
#             try:
#                 schema_access_instance = SchemaAccess.objects.get(
#                     user=user,
#                     database=privilege_validation_instance.database,
#                     schema=privilege_validation_instance.schema
#                 )
#                 schema_access_instance.has_access = True
#                 schema_access_instance.save()
#             except SchemaAccess.DoesNotExist:
#                 # If the entry doesn't exist, create a new one
#                 SchemaAccess.objects.create(
#                     user=user,
#                     database=privilege_validation_instance.database,
#                     schema=privilege_validation_instance.schema,
#                     has_access=True
#                 )
#
#             return redirect('dashboard')  # You might want to handle the result or perform other actions based on it
#         else:
#             # Print form errors for debugging
#             print(form.errors)
#     else:
#         form = PrivilegeFunctionValidationForm()
#
#     context = {
#         'form': form,
#         'all_columns': list(all_columns),  # Convert the set to a list
#     }
#
#     return render(request, 'GenesysAuthenticator/privilege_function_validation_form.html', context)
#
#
# def get_schemas(request):
#     database_id = request.GET.get('database_id')
#     schemas = MasterDatabaseSchema.objects.filter(database_id=database_id, is_active=True).values('id', 'schema')
#     return JsonResponse(list(schemas), safe=False)
#
#
# def get_tables(request):
#     schema_id = request.GET.get('schema_id')
#     tables = DatabaseTable.objects.filter(schema_id=schema_id).values('id', 'table_name')
#     return JsonResponse(list(tables), safe=False)
#
#
# def get_columns(request):
#     table_id = request.GET.get('table_id')
#     columns = DatabaseTable.objects.get(id=table_id).columns
#     return JsonResponse({'columns': json.loads(columns)})
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

from django.contrib import messages
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .custom_decorator import designation_required
from .forms import GrantPermissionForm, PrivilegeFunctionValidationForm
from .models import MasterDatabase, DatabaseAccess, MasterDatabaseSchema, DatabasePermission, DatabaseTable, \
    SchemaAccess
from .postgresql_fun_call import grant_database_privileges, grant_function_validation_privileges
from .get_schema_table_column import get_remote_schemas_tables_columns, save_to_local_database
from django.http import Http404, JsonResponse
import json
from django.urls import reverse_lazy
from .utils import *


class GrantPermissionView(View):
    template_name = 'GenesysAuthenticator/database_permission_form.html'
    form_class = GrantPermissionForm
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required)
    @method_decorator(designation_required('Senior Vice President - Projects', 'Vice President',
                                           'General Manager Projects', 'Senior Project Manager',
                                           'Program Manager', 'Manager'))
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    @method_decorator(designation_required('Senior Vice President - Projects', 'Vice President',
                                           'General Manager Projects', 'Senior Project Manager',
                                           'Program Manager', 'Manager'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = cleaned_data['user']
            granted_by = request.user
            database_name = cleaned_data['database']
            func_n = 'dum_func'
            db_access = cleaned_data.get('db_access', False)
            privilege_select = cleaned_data.get('privilege_select', False)
            privilege_insert = cleaned_data.get('privilege_insert', False)
            privilege_update = cleaned_data.get('privilege_update', False)
            privilege_delete = cleaned_data.get('privilege_delete', False)
            privilege_sequence = cleaned_data.get('privilege_sequence', False)
            schemas = cleaned_data.get('schemas', [])

            # Extract schema names from the QuerySet
            schema_names = list(schemas.values_list('schema', flat=True))

            # Call the utility function to grant database privileges
            result = grant_database_privileges(user, schema_names, database_name, func_n, db_access, privilege_select,
                                               privilege_insert, privilege_update, privilege_delete,
                                               privilege_sequence)

            if result:
                # Save the form data to the DatabasePermission model
                database_permission = form.save(commit=False)
                database_permission.granted_by = granted_by

                # Save the instance to get an ID
                database_permission.save()

                # Set the selected schemas on the DatabasePermission instance
                database_permission.schemas.set(schemas)

                messages.success(request, 'Database permission granted successfully.')
                return redirect(self.success_url)
            else:
                messages.error(request, f"Error: {result}")
        else:
            messages.error(request, 'Error: Form is not valid.')
        return render(request, self.template_name, {'form': form})


@login_required
def get_schema_table_col_from_server(request):
    if request.method == 'POST':
        remote_databases = MasterDatabase.objects.values_list('database_name', flat=True).distinct()

        databases_for_server1 = ["highfidelity", "poi_core", "WoNoRoadNetwork"]
        databases_for_server2 = ["xyz", "abcd", "db_fight"]

        for database in remote_databases:
            if database in databases_for_server1 or database in databases_for_server2:
                remote_database, data = get_data_for_server(database, databases_for_server1 + databases_for_server2)
                save_to_local_database(remote_database, data)
            else:
                print("Error: Unsupported database")

        print("Data retrieval and saving to local database complete.")

        # Redirect to the dashboard after successful data retrieval
        return redirect('dashboard')  # Replace 'dashboard' with the actual name or URL of your dashboard view

    return render(request, 'GenesysAuthenticator/trigger_data_retrieval.html')


class GrantPrivilegesFunctionValidationView(View):
    template_name = 'GenesysAuthenticator/privilege_function_validation_form.html'
    form_class = PrivilegeFunctionValidationForm
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required)
    @method_decorator(designation_required('Senior Vice President - Projects', 'Vice President',
                                           'General Manager Projects', 'Senior Project Manager',
                                           'Program Manager', 'Manager'))
    def get(self, request, *args, **kwargs):
        all_columns = set()
        for table in DatabaseTable.objects.all():
            all_columns.update(table.columns.split(','))

        form = self.form_class()
        context = {'form': form, 'all_columns': list(all_columns)}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    @method_decorator(designation_required('Senior Vice President - Projects', 'Vice President',
                                           'General Manager Projects', 'Senior Project Manager',
                                           'Program Manager', 'Manager'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            privilege_validation_instance = form.save(commit=False)
            privilege_validation_instance.granted_by = request.user

            # try:
            #     privilege_validation_instance.save()
            # except IntegrityError as e:
            #     print(f"IntegrityError: {e}")

            user = request.user
            database_id = request.POST.get('database')
            schema_id = request.POST.get('schema')
            table_id = request.POST.get('table')
            database_name = MasterDatabase.objects.get(id=database_id).database_name
            schema_name = MasterDatabaseSchema.objects.get(id=schema_id).schema
            table_name = DatabaseTable.objects.get(id=table_id).table_name
            column_name = request.POST.get('columns')

            result = grant_function_validation_privileges(
                user,
                schema_name,
                table_name,
                column_name,
                database_name,
            )

            try:
                schema_access_instance = SchemaAccess.objects.get(
                    user=user,
                    database=privilege_validation_instance.database,
                    schema=privilege_validation_instance.schema
                )
                schema_access_instance.has_access = True
                schema_access_instance.save()
            except SchemaAccess.DoesNotExist:
                SchemaAccess.objects.create(
                    user=user,
                    database=privilege_validation_instance.database,
                    schema=privilege_validation_instance.schema,
                    has_access=True
                )

            return redirect(self.success_url)
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


def get_schemas(request):
    database_id = request.GET.get('database_id')
    schemas = MasterDatabaseSchema.objects.filter(database_id=database_id, is_active=True).values('id', 'schema')
    return JsonResponse(list(schemas), safe=False)


def get_tables(request):
    schema_id = request.GET.get('schema_id')
    tables = DatabaseTable.objects.filter(schema_id=schema_id).values('id', 'table_name')
    return JsonResponse(list(tables), safe=False)


def get_columns(request):
    table_id = request.GET.get('table_id')
    columns = DatabaseTable.objects.get(id=table_id).columns
    return JsonResponse({'columns': json.loads(columns)})
