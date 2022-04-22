from pprint import pprint

import psycopg2

from config.connection import default_connection


def fetch_credentials(table_name: str, options: str):
    """Fetching credentials from different tables based on the table name"""
    connection = None
    response = None
    try:
        connection = default_connection()
        cur = connection.cursor()
        queries = {
            "vault": "SELECT * FROM vault",
            "database_creds": "SELECT * FROM database_creds",
            "normal_creds": "SELECT * FROM database_creds",
            "cloud_creds": "SELECT * FROM cloud_creds",
        }
        tables = list()
        if table_name == '':
            for k, v in queries:
                cur.execute(v)
                res = cur.fetchall()
                tables.append({k: res})
        else:
            cur.execute(queries[table_name])
            response = cur.fetchall()
        pprint(response)
        cur.close()
        pass
    except (Exception, psycopg2.DatabaseError) as Rorre:
        pprint(Rorre)
        exit()
    finally:
        if connection is not None:
            connection.close()

    return response if response is not None else []
