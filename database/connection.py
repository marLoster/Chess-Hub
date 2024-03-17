import psycopg2
import yaml


class DBconnection():

    @staticmethod
    def _parse_credentials():
        with open("../database/cred.yaml", 'r') as stream:
            try:
                credentials = yaml.safe_load(stream)
                return credentials.get('database'), credentials.get('user'), credentials.get(
                    'password'), credentials.get(
                    'host')
            except yaml.YAMLError as exc:
                print(exc)

    def __init__(self):
        dbname, user, password, host = self._parse_credentials()
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def select(self, query):
        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            print("All records in the table:")
            for row in records:
                print(row)
            print()

        except (Exception, psycopg2.Error) as error:
            print("Error while executing statement:", error)

    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while executing statement:", error)

    def create_csv(self, query, filename, args):
        try:
            self.cursor.execute(query, args)
            records = self.cursor.fetchall()
            print("All records in the table:")
            with open(filename, "w") as f:
                for row in records:
                    f.write(",".join(row))

        except (Exception, psycopg2.Error) as error:
            print("Error while executing statement:", error)