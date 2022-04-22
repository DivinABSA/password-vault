import base64
import json
from pprint import pprint

import psycopg2
import requests

from config.connection import default_connection
from lib.config import api_base_url
from lib.crypto import get_auth_hash, get_key, encrypt_vault, decrypt_vault
from model.account import Account
from model.session import Session


def login(username, master_password):
    """
    Posts username and authentication hash to /login.
    Decrypts vault on successful login.
    Returns new Session.
    """
    print('Logging in...')

    connection = None
    response_body = None
    try:
        connection = default_connection()
        cursor = connection.cursor()
        find_user = f"SELECT username,hash from Vault where username='{username}'"
        cursor.execute(find_user)
        response_body = cursor.fetchone()
        pprint(response_body)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
    finally:
        if connection is not None:
            connection.close()
    if response_body is None:
        print("[PANIC]: Invalid credentials")
        exit()
    auth_hash = get_auth_hash(username, master_password)
    pprint(response_body[1].encode())
    cipher_text = base64.b64decode(response_body[1].encode())
    pprint("Cipher Text")
    pprint(cipher_text)
    key = get_key(username, master_password)
    vault_str = decrypt_vault(cipher_text, key)
    pprint(vault_str)
    # vault_dict = json.loads(vault_str)

    session = Session(username, auth_hash, key)
    # session.dict_to_vault(vault_dict)

    return session


def signup(username, master_password):
    """
    Posts username and authentication hash to /signup.
    Calls update vault with empty vault on successful signup.
    Returns new Session.
    """
    print('Signing up...')

    connection = None
    try:
        connection = default_connection()
        cursor = connection.cursor()
        # create the user
        cursor.execute(f"SELECT * FROM vault where username='{username}'; ")
        user = cursor.fetchone()
        if user is not None:
            print("User exists")
            exit()
        cursor.execute("INSERT INTO vault (username,hash) VALUES(%s,%s)",
                       (username, password_hasher(username, master_password)))
        connection.commit()  # Save the transaction
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Simple message")
        exit()
    finally:
        if connection is not None:
            connection.close()
            print("Execution completed")
    key = get_key(username, master_password)
    vault = []
    session = Session(username, get_auth_hash(username, master_password), key, vault)
    # Unnecessary method
    # update_vault(session)
    return session


def password_hasher(username, password):
    auth_hash = get_auth_hash(username, password)
    return base64.b64encode(auth_hash).decode()


def create_database_table(user, password, host, db_name):
    connection = None
    try:
        connection = default_connection(user, password, host, db_name)
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS vault(
        id serial primary key,
        username varchar(355) not null unique,
        hash text not null,
        createdAt TIMESTAMP default NOW(),
        updatedAt TIMESTAMP default NOW());
        
        CREATE TABLE IF NOT EXISTS normal_creds(
        id serial PRIMARY KEY,
        appname text not null,
        username varchar(255),
        password varchar(255),
        createdAt TIMESTAMP Default now(),
        updatedAt TIMESTAMP default now()
        );
        CREATE TABLE IF NOT EXISTS database_creds(
         id serial PRIMARY KEY,
        appname text not null,
        username varchar(255),
        password varchar(255),
        host varchar(255),
        database varchar(255),
        createdAt TIMESTAMP Default now(),
        updatedAt TIMESTAMP default now()
        );
        CREATE TABLE IF NOT EXISTS  cloud_creds(
         id serial PRIMARY KEY,
        cloud_platform text not null,
        subnet_id varchar(255),
        security_group_id varchar(255),
        createdAt TIMESTAMP Default now(),
        updatedAt TIMESTAMP default now());
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table created successfully")
    except (Exception, psycopg2.DatabaseError) as Rorre:
        print(Rorre)
        exit()
    finally:
        if connection is not None:
            connection.close()
            print("Execution completed")


def update_vault(session):
    """
    Posts username, authentication hash and encrypted vault to /update.
    """
    print('Updating vault in cloud...')
    url = api_base_url + '/update'

    vault_dict = session.vault_to_dict()
    encrypted_vault = encrypt_vault(json.dumps(vault_dict), session.key)

    body = {
        'username': session.username,
        'auth_hash': base64.b64encode(session.auth_hash).decode(),
        'vault': base64.b64encode(encrypted_vault).decode(),
    }

    response = requests.post(url, data=json.dumps(body))

    if response.status_code != requests.codes.ok:
        print('Updating vault attempt failed with status code: ' + str(response.status_code))
        exit()
