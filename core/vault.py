import psycopg2


def db_connection():
    cons = psycopg2.connect(
        host='localhost',
        database="postgres",
        user='postgres',
        password='password'
    )

    return cons


class VaultApi:
    def __init__(self, *, username, password):
        self.username = username
        self.password = password

    def login(self):
        conn = None
        try:
            conn = db_connection
            ex = conn.cursor("select * from vault where email=?")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                pass

    def register(self):
        pass
