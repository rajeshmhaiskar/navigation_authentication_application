import psycopg2
from .models import MasterDatabase, MasterDatabaseSchema, DatabaseTable
from .db_utils import create_connection
import json


def get_remote_schemas_tables_columns(remote_db_params):
    try:
        with create_connection(remote_db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT schema_name FROM information_schema.schemata WHERE "
                    "(schema_name NOT LIKE 'pg_%' AND schema_name NOT LIKE 'information_%') GROUP BY 1 ORDER BY 1")
                schemas = cursor.fetchall()

                schema_data = {}
                for schema in schemas:
                    schema_name = schema[0]
                    cursor.execute(
                        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
                    tables = cursor.fetchall()

                    table_data = {}
                    for table in tables:
                        table_name = table[0]
                        cursor.execute(
                            f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table_name}';")
                        columns = cursor.fetchall()
                        column_names = [col[0] for col in columns]
                        table_data[table_name] = column_names

                    schema_data[schema_name] = table_data

        return schema_data
    except Exception as e:
        print(f"Error: Unable to fetch remote schema, tables, and columns - {e}")
        return {}


def save_to_local_database(remote_database, data):
    for schema_name, tables_data in data.items():
        master_db, created = MasterDatabase.objects.get_or_create(database_name=remote_database)

        schema_object, created = MasterDatabaseSchema.objects.get_or_create(
            database=master_db, schema=schema_name, defaults={'is_active': True})

        for table_name, columns in tables_data.items():
            table_object, created = DatabaseTable.objects.update_or_create(
                database=master_db,
                schema=schema_object,
                table_name=table_name,
                defaults={'columns': json.dumps(columns)}
            )

            print(f"Saved Table: {table_name} for Schema: {schema_name} in Database: {remote_database}")
