import psycopg2
import yaml


def parse_credentials():
    with open("../Database/cred.yaml", 'r') as stream:
        try:
            credentials = yaml.safe_load(stream)
            return credentials.get('database'), credentials.get('user'), credentials.get('password'), credentials.get(
                'host')
        except yaml.YAMLError as exc:
            print(exc)


def database_select(query):
    conn = None
    cursor = None
    dbname, user, password, host = parse_credentials()
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        print("All records in the table:")
        for row in records:
            print(row)
        print()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()

def database_exec(query, params=None):
    conn = None
    cursor = None
    dbname, user, password, host = parse_credentials()
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        cursor = conn.cursor()
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()
