import psycopg2
from django.http import Http404
from .models import MasterDatabase


def create_user_in_database(username, password, db_server, db_port, db_username, db_password, database):
    connection_params = {
        'host': db_server,
        'database': database.database_name,
        'user': db_username,
        'password': db_password,
        'port': db_port,
    }

    try:
        with psycopg2.connect(**connection_params) as conn, conn.cursor() as cursor:
            cursor.callproc('create_user_with_password', (username, password))
            conn.commit()
            print(f"User created successfully in {database.database_name} on server {db_server}!")
    except Exception as e:
        print(f"Error creating user in {database.database_name} on server {db_server}: {e}")


def create_user_condition_check_validations(username, password, database):
    db_server = database.server_ip
    db_port = database.port
    db_username = database.username
    db_password = database.password

    databases_for_server1 = ["Highfidelity", "poi_core", "WoNoRoadNetwork"]
    databases_for_server2 = ["nmmc", "adas", "innomap"]

    # Connect to the specified database
    if db_server == "127.0.0.1" and database.database_name in databases_for_server1:
        create_user_in_database(username, password, db_server, db_port, db_username, db_password, database)

    elif db_server == "172.0.0.1" and database.database_name in databases_for_server2:
        create_user_in_database(username, password, db_server, db_port, db_username, db_password, database)


def grant_database_privileges(user, schema_names, database_name, func_n,
                              db_access=False, privilege_select=False, privilege_insert=False,
                              privilege_update=False, privilege_delete=False, privilege_sequence=False,
                              ):
    try:
        try:
            master_db = MasterDatabase.objects.get(database_name=database_name, is_active=True)
        except MasterDatabase.DoesNotExist:
            raise Http404("MasterDatabase not found with the given conditions.")

        # Get the emp_id from the user
        user_emp_id = user.emp_id

        # Extract relevant fields from MasterDatabase
        db_name = master_db.database_name
        username = master_db.username
        password = master_db.password
        server_ip = master_db.server_ip
        port = master_db.port

        # Establish a connection using the extracted configuration
        connection = psycopg2.connect(
            dbname=db_name,
            user=username,
            password=password,
            host=server_ip,
            port=port
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Call the PostgreSQL function
        cursor.callproc('grant_privs', [user_emp_id, db_name, func_n,
                                        db_access, privilege_select, privilege_insert,
                                        privilege_update, privilege_delete, privilege_sequence, schema_names])

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return 'Privileges granted successfully'
    except Exception as e:
        print(e)
        return f'Error: {e}'


def grant_function_validation_privileges(user, schema_name, table_name, column_name, database_name):
    try:
        try:
            master_db = MasterDatabase.objects.get(database_name=database_name, is_active=True)
        except MasterDatabase.DoesNotExist:
            raise Http404("MasterDatabase not found with the given conditions.")

        # Get the emp_id from the user
        user = user.emp_id

        # Extract relevant fields from MasterDatabase
        db_name = master_db.database_name
        username = master_db.username
        password = master_db.password
        server_ip = master_db.server_ip
        port = master_db.port

        # Establish a connection using the extracted configuration
        connection = psycopg2.connect(
            dbname=db_name,
            user=username,
            password=password,
            host=server_ip,
            port=port
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Call the PostgreSQL function
        cursor.callproc('valid_func',
                        [user, schema_name, table_name, column_name ])

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return 'validation granted successfully'
    except Exception as e:
        print(e)
        return f'Error: {e}'
