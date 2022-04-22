from PyInquirer import prompt

from cli_flows.gen_pwd_flow import run_generate_password_flow
from lib.api import update_vault
from lib.common import custom_style, validate_nonempty
from model.account import Account, AddCredentials
from model.create import create_credentials


def run_create_flow(session):
    """
    Command line interface questions for creating a new account.
    Asks details of account to create, adds account to vault locally and then updates vault in cloud.
    """
    new_account = None
    questions = [
        {
            'type': 'list',
            'name': 'create_flow',
            'message': 'What type of credentials would you like to add?',
            'choices': [
                'Normal Credentials',
                'Database Credentials',
                'Cloud Credentials',
            ]
        },
        {
            'type': 'input',
            'name': 'appname',
            'message': 'What is the name of your Application?',
            'when': lambda answers: answers['create_flow'] != 'Cloud Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'What is the username of your application?',
            'when': lambda answers: answers['create_flow'] != 'Cloud Credentials',
            'validate': validate_nonempty,
        },

        # Database creadentials data

        {
            'type': 'input',
            'name': 'host',
            'message': 'What is the name of your Database Host?',
            'when': lambda answers: answers['create_flow'] == 'Database Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'database',
            'message': 'What is the name of your database ?',
            'when': lambda answers: answers['create_flow'] == 'Database Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'cloud_platform',
            'message': 'What is the Cloud platform name ?',
            'when': lambda answers: answers['create_flow'] == 'Cloud Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'subnet_id',
            'message': 'What is the subnet Id of the cloud platform?',
            'when': lambda answers: answers['create_flow'] == 'Cloud Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'security_group_id',
            'message': 'What is the Security groupId of the platform?',
            'when': lambda answers: answers['create_flow'] == 'Cloud Credentials',
            'validate': validate_nonempty,
        },
        #
        # {
        #     'type': 'input',
        #     'name': 'username',
        #     'message': 'What is the username for your new account?',
        #     'when': lambda answers: answers['create_flow'] != 'Cloud Credentials',
        #
        #     'validate': validate_nonempty,
        # },
        {
            'type': 'list',
            'name': 'password_method',
            'when': lambda answers: answers['create_flow'] != 'Cloud Credentials',

            'message': 'How would you like to create your password?',
            'choices': [
                'Input password myself',
                'Generate a password for me',
            ]
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'What is the password?',
            'when': lambda answers: answers.get('password_method', '') == 'Input password myself' and answers[
                'create_flow'] != 'Cloud Credentials',
            'validate': validate_nonempty,
        },
        {
            'type': 'password',
            'name': 'confirm_password',
            'message': 'Please confirm your password:',
            'when': lambda answers: answers.get('password', False) and answers[
                'create_flow'] != 'Cloud Credentials',
            'default': '',
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        print('No valid response was provide')
        exit()

    if answers['create_flow'] == 'Normal Credentials':
        if answers['password_method'] == 'Input password myself':
            if answers['password'] == answers['confirm_password']:
                print("Password confirmed.")
            else:
                print("Passwords do not match. Nothing will be created.")
                return
        elif answers['password_method'] == 'Generate a password for me':
            answers['password'] = run_generate_password_flow()
        new_account = create_credentials(option='normal', password=answers['password'], user_name=answers['username'],
                                         app_name=answers['appname'])
    elif answers['create_flow'] == "Database Credentials":
        if answers['password_method'] == 'Input password myself':
            if answers['password'] == answers['confirm_password']:
                print("Password confirmed.")
            else:
                print("Passwords do not match. Nothing will be created.")
                return
        elif answers['password_method'] == 'Generate a password for me':
            answers['password'] = run_generate_password_flow()
        new_account = create_credentials(option='db', host=answers['host'], database=answers['database'],
                                         password=answers['password'], user_name=answers['username'],
                                         app_name=answers['appname'])
    elif answers['create_flow'] == "Cloud Credentials":
        new_account = create_credentials(subnet_id=answers['subnet_id'],
                                         security_group_id=answers['security_group_id'], option='cloud',
                                         cloud_platform=answers['cloud_platform'])
    session.vault.append(new_account)
    print('Account created.')

    update_vault(session)

    # if not session.account_exists(answers['name']):
    #     new_account = Account(answers['name'], answers['username'], answers['password'])
    #     session.vault.append(new_account)
    #     print('Account created.')
    #     update_vault(session)
    # else:
    #     print('An account already exists with this name in the vault.')
    #     print('Nothing created.')ac
