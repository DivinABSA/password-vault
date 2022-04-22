from pprint import pprint

import psycopg2

from config.connection import default_connection


def fetch_credentials(table_name: str, options: str = None):
    """Fetching credentials from different tables based on the table name"""
    connection = None
    response = list()
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
                response.append({k: res})
        else:
            cur.execute(queries[table_name])
            pa = cur.fetchall()
            data = list()
            for _, i in enumerate(pa):
                if table_name == '':
                    itesm = {
                        "appname": i[1],
                        "username": i[2],
                        "password": i[3],
                        "host": i[4],
                        "database": i[5]
                    }
                    response.append(itesm)
                elif table_name == 'cloud_creds':
                    itesm = {
                        "cloud_platform": i[1],
                        "subnet_id": i[2],
                        "security_group_id": i[3],
                    }
                    response.append(itesm)
                elif table_name == 'vault':
                    itesm = {
                        "username": i[1],
                        "hash": i[2],
                    }
                    response.append(itesm)
                elif table_name == 'normal_creds':
                    itesm = {
                        "appname": i[1],
                        "username": i[2],
                        "password": i[3],
                    }
                    response.append(itesm)

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
