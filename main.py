from PyInquirer import prompt

from cli_flows import run_view_credentials
from lib.api import login, signup, create_database_table
from lib.common import custom_style, validate_nonempty
from cli_flows.create_flow import run_create_flow
from cli_flows.read_flow import run_read_flow
from cli_flows.edit_flow import run_edit_flow
from cli_flows.delete_flow import run_delete_flow


def run_login_flow():
    questions = [
        {
            'type': 'list',
            'name': 'login_choice',
            'message': 'Welcome to Password Vault!',
            'choices': [
                'Login',
                'Sign up',
                "init DB",
            ]
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter username:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] != 'init DB',
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'input',
            'name': 'root_user',
            'message': 'Enter Database Root User:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] == 'init DB',
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'input',
            'name': 'root_password',
            'message': 'Enter Database Root Password:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] == 'init DB',
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'input',
            'name': 'database_host',
            'message': 'Enter database Host:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] == 'init DB',
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'input',
            'name': 'database_name',
            'message': 'Enter database Name:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] == 'init DB',
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'password',
            'name': 'master_password',
            'message': 'Enter master password:',
            'validate': validate_nonempty,
            "when": lambda answers: answers['login_choice'] != 'init DB',
        },
        {
            'type': 'password',
            'name': 'master_password_confirm',
            'message': 'Confirm master password:',
            'when': lambda answers: answers['login_choice'] == 'Sign up' and answers['login_choice'] != 'init DB',
            'default': '',
        },
    ]
    """
    Command line interface questions for logging in or signing up.
    Asks whether to login or signup and then credentials.
    Attempts to login or signup.
    """

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    session = None
    if answers['login_choice'] == 'Login':
        session = login(answers['username'], answers['master_password'])
    elif answers['login_choice'] == 'Sign up':
        if answers['master_password'] == answers['master_password_confirm']:
            session = signup(answers['username'], answers['master_password'])
        else:
            print('Passwords did not match. Exiting...')
            exit()
    elif answers['login_choice'] == "init DB":
        session = create_database_table(user=answers['root_user'], password=answers['root_password'],
                                        host=answers['database_host'], db_name=answers['database_name'])

    print('Welcome ' + session.username if session is not None else '' + '!')
    return session


def run_main_flow(session):
    """
    Command line interface questions for what user wants to do now that they are logged in.
    """
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do? Ctrl+C to exit.',
            'choices': [
                {
                    'name': 'Create credentials',
                    'value': run_create_flow,
                },
                {
                    'name': 'View Credentials',
                    'value': run_read_flow,
                },

                {
                    'name': 'Edit an account',
                    'value': run_edit_flow,
                },
                {
                    'name': 'Delete an account',
                    'value': run_delete_flow,
                },
            ]
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    answers['theme'](session)


def main():
    """
    Run login flow and then continuously run the main flow until user exits.
    """
    session = run_login_flow()
    while True:
        run_main_flow(session)


if __name__ == "__main__":
    main()
