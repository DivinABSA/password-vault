import psycopg2

from config.connection import default_connection
from lib.api import password_hasher


def create_credentials(option, app_name=None, user_name=None, password=None, database=None, host=None,
                       cloud_platform=None,
                       subnet_id=None, security_group_id=None):
    """ Create normal app credentials"""
    connection = None
    try:
        connection = default_connection()
        cur = connection.cursor()
        # Execute the script
        if option == 'normal':
            # Normal Credentials Table
            cur.execute("INSERT INTO normal_creds (appname,username,password) VALUES(%s,%s,%s)",
                        (app_name, user_name, password_hasher(user_name, password)))
        elif option == 'db':
            # Database Credentials Table
            cur.execute("INSERT INTO database_creds (appname,username,password,host,database) VALUES(%s,%s,%s, %s,%s)",
                        (app_name, user_name, password_hasher(user_name, password), host, database))
        elif option == 'cloud':
            # CLOUD Credentials Table
            cur.execute("INSERT INTO cloud_creds (cloud_platform,subnet_id,security_group_id) VALUES(%s,%s,%s)",
                        (cloud_platform, subnet_id, security_group_id))
        else:
            print("No option provided for the creation of credentials")
            exit()
        # commit changes
        connection.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as Rorre:
        print(Rorre)
        print("something went wrong")
        exit()
    finally:
        if connection is not None:
            connection.close()
            print(f'new  Credentials created ')
