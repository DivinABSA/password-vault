from pprint import pprint

from PyInquirer import prompt


from lib.common import custom_style

from model.fetch import fetch_credentials


def run_read_flow(session):
    """
    Command line interface questions for creating a new account.
    Asks details of account to create, adds account to vault locally and then updates vault in cloud.
    """
    new_account = None
    questions = [
        {
            'type': 'list',
            'name': 'read_flow',
            'message': 'Select Flow to view?',
            'choices': [
                'Vault Credentials',
                'Normal Credentials',
                'Database Credentials',
                'Cloud Credentials',
            ]
        },

    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        print('No valid response was provide')
        exit()

    if answers['read_flow'] == 'Vault Credentials':
        pprint(fetch_credentials(table_name='vault'))

    if answers['read_flow'] == 'Normal Credentials':
        pprint(fetch_credentials(table_name='normal_creds'))

    if answers['read_flow'] == 'Database Credentials':
        pprint(fetch_credentials(table_name='database_creds'))

    if answers['read_flow'] == 'Cloud Credentials':
        pprint(fetch_credentials(table_name='cloud_creds'))

    return session
