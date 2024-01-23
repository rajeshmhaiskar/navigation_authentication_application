import psycopg2


def create_connection(params):
    try:
        connection = psycopg2.connect(**params)
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database - {e}")
        return None
