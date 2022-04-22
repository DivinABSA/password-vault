import psycopg2


def default_connection(user=None, password=None, host=None, db_name=None):
    return psycopg2.connect(
        host= host if host else 'localhost',
        password=password if password else 'postgres',
        port='5432',  # default postgres port
        user=user if user else 'postgres',
        database=db_name if db_name else 'vault'
    )
