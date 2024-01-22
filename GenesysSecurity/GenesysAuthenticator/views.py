from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError
from .forms import RegistrationForm, GrantPermissionForm, PrivilegeFunctionValidationForm
from .postgresql_fun_call import *
from .models import MasterDatabase, DatabaseAccess, MasterDatabaseSchema, UserDetails, DatabasePermission, \
    DatabaseTable, SchemaAccess
from django.contrib.auth.decorators import login_required
from .custom_decorator import designation_required
from django.shortcuts import render, redirect
from .get_schema_table_column import get_remote_schemas_tables_columns, save_to_local_database
from django.http import Http404, JsonResponse


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

    return render(request, 'GenesysAuthenticator/login.html', {'form': form})


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

                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('login')
            else:
                messages.error(request, 'Form is not valid. Please correct the errors.')
        except Exception as e:
            print(f"Error during registration: {e}")
            messages.error(request, 'An error occurred during registration. Please try again.')

    else:
        form = RegistrationForm()

    return render(request, 'GenesysAuthenticator/register.html', {'form': form})


def dashboard(request):
    return render(request, 'GenesysAuthenticator/dashboard.html')


#
# def get_user_emp_id(user_email):
#     try:
#         user_details = UserDetails.objects.get(email=user_email)
#         return user_details.emp_id
#     except UserDetails.DoesNotExist:
#         return None  # Return None if the user doesn't exist
#
#
# # def get_schema_names(schema_ids):
# #     try:
# #         # Retrieve schema names based on schema IDs
# #         schema_names = MasterDatabaseSchema.objects.filter(id__in=schema_ids).values_list('name', flat=True)
# #         return list(schema_names)
# #     except MasterDatabaseSchema.DoesNotExist:
# #         # Handle the case where one or more schema IDs do not exist
# #         return []
#
#
@login_required
@designation_required('Senior Vice President - Projects', 'Vice President', 'General Manager Projects',
                      'Senior Project Manager', 'Program Manager', 'Manager')
def grant_permission(request):
    if request.method == 'POST':
        form = GrantPermissionForm(request.POST)
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
                return redirect('dashboard')
            else:
                messages.error(request, f"Error: {result}")
        else:
            messages.error(request, 'Error: Form is not valid.')
    else:
        form = GrantPermissionForm()

    return render(request, 'GenesysAuthenticator/database_permission_form.html', {'form': form})


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


def get_schema_table_col_from_server(request):
    remote_databases = MasterDatabase.objects.values_list('database_name', flat=True).distinct()

    databases_for_server1 = ["Highfidelity", "poi_core", "WoNoRoadNetwork"]
    databases_for_server2 = ["xyz", "abcd", "db_fight"]

    for database in remote_databases:
        if database in databases_for_server1 or database in databases_for_server2:
            remote_database, data = get_data_for_server(database, databases_for_server1 + databases_for_server2)
            save_to_local_database(remote_database, data)
        else:
            print("Error: Unsupported database")

    print("Data retrieval and saving to local database complete.")
    return render(request, 'GenesysAuthenticator/dashboard.html')


def grant_privileges_function_validation_view(request):
    all_columns = set()
    for table in DatabaseTable.objects.all():
        all_columns.update(table.columns.split(','))

    if request.method == 'POST':
        form = PrivilegeFunctionValidationForm(request.POST)
        if form.is_valid():
            privilege_validation_instance = form.save(commit=False)
            privilege_validation_instance.granted_by = request.user

            try:
                privilege_validation_instance.save()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                # Handle the integrity error as needed, e.g., redirect to an error page

            # Rest of your code...

            user = request.user

            # Call the second function with extracted values
            result = grant_function_validation_privileges(
                user,
                privilege_validation_instance.schema.schema,
                privilege_validation_instance.table.table_name,
                None,
                privilege_validation_instance.privilege_function_validation,
                privilege_validation_instance.table.columns.split(','),  # Columns from the form
                privilege_validation_instance.database.database_name
            )

            # Create or update an entry in the SchemaAccess table
            try:
                schema_access_instance = SchemaAccess.objects.get(
                    user=user,
                    database=privilege_validation_instance.database,
                    schema=privilege_validation_instance.schema
                )
                schema_access_instance.has_access = True
                schema_access_instance.save()
            except SchemaAccess.DoesNotExist:
                # If the entry doesn't exist, create a new one
                SchemaAccess.objects.create(
                    user=user,
                    database=privilege_validation_instance.database,
                    schema=privilege_validation_instance.schema,
                    has_access=True
                )

            return redirect('dashboard')  # You might want to handle the result or perform other actions based on it
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = PrivilegeFunctionValidationForm()

    context = {
        'form': form,
        'all_columns': list(all_columns),  # Convert the set to a list
    }

    return render(request, 'GenesysAuthenticator/privilege_function_validation_form.html', context)


def get_schemas_for_database(request):
    database_id = request.GET.get('database_id')

    # Fetch schemas based on the selected database
    schemas = MasterDatabaseSchema.objects.filter(database_id=database_id)

    # Create a list of dictionaries for the dropdown options
    schema_options = [{'id': schema.id, 'name': schema.schema} for schema in schemas]

    return JsonResponse({'schemas': schema_options})


def get_tables_for_schema(request):
    schema_id = request.GET.get('schema_id')

    # Fetch tables based on the selected schema
    tables = DatabaseTable.objects.filter(schema_id=schema_id)

    # Create a list of dictionaries for the dropdown options
    table_options = [{'id': table.id, 'name': table.table_name} for table in tables]

    return JsonResponse({'tables': table_options})


def get_columns_for_table(request):
    table_id = request.GET.get('table_id')

    # Fetch columns based on the selected table
    table = DatabaseTable.objects.get(pk=table_id)
    columns = table.columns.split(',')

    return JsonResponse({'columns': columns})
