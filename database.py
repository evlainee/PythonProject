import psycopg2
import random


conn_params = {
    'dbname': 'postgres_M',
    'user': 'postgres_m',
    'password': 'mypassword',
    'host': '10.7.0.5',
    'port': '1000'
}


def apply_sql_script(script_path):

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        with open(script_path, 'r') as sql_file:
            cursor.execute(sql_file.read())
            conn.commit()

        print("SQL script applied successfully.")

    except psycopg2.Error as error:
        print(f"Error applying SQL script: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


