from pprint import pprint

import psycopg2

from config.connection import default_connection


class Account(object):
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def display(self):
        print('Name: ' + self.name)
        print('Username: ' + self.username)
        print('Password: ' + self.password)


class AddCredentials:
    """ Creates Credentials based on the selected option [normal, db,cloud] """

    def __init__(self, option, app_name=None, user_name=None, password=None, database=None, host=None,
                 cloud_platform=None,
                 subnet_id=None, security_group_id=None, ):
        self.app_name = app_name
        self.user_name = user_name
        self.password = password
        self.database = database
        self.host = host
        self.option = option if option is not None else None,
        self.cloud_platform = cloud_platform
        self.subnet_id = subnet_id
        self.security_group_id = security_group_id
        self.connection = None
        self.opname = self._name_extra()
        pprint(self.opname)
    def create_credentials(self, option=None):
        """ Create normal app credentials"""
        try:
            self.connection = default_connection()
            cur = self.connection.cursor()
            # Execute the script
            if self.option == 'normal':
                # Normal Credentials Table
                cur.execute("INSERT INTO normal_creds (appname,username,password) VALUES(%s,%s,%s)",
                            (self.app_name, self.user_name, self.password))
            elif self.option == 'db':
                # Database Credentials Table
                cur.execute("INSERT INTO database_creds (appname,username,password,host,database) VALUES(%s,%s,%s)",
                            (self.app_name, self.user_name, self.password, self.host, self.database))
            elif self.option == 'cloud':
                # CLOUD Credentials Table
                cur.execute("INSERT INTO cloud_cred (cloud_platform,subnet_id,security_group_id) VALUES(%s,%s,%s)",
                            (self.cloud_platform, self.subnet_id, self.security_group_id))
            else:
                print("No option provided for the creation of credentials")
                exit()
            # commit changes
            self.connection.comit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as Rorre:
            print(Rorre)
            print("something went wrong")
            exit()
        finally:
            if self.connection is not None:
                self.connection.close()
                print(f'new {self.opname} Credentials created ')

    def _name_extra(self):
        if self.option == "normal":
            return 'Normal'
        elif self.option == 'db':
            return "database"
        elif self.option == 'cloud':
            return 'Cloud'
        else:
            pass




