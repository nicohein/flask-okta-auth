import os


def get_env_variable(variable_name,):
    variable = os.environ.get(variable_name)
    if not variable:
        raise Exception(f'{variable_name} environment variable not set')
    return variable


FLASK_SECRET_KEY = get_env_variable('FLASK_SECRET_KEY')

OKTA_CLIENT_ID = get_env_variable('OKTA_CLIENT_ID')

OKTA_CLIENT_SECRET = get_env_variable('OKTA_CLIENT_SECRET')

OKTA_BASE_URL = get_env_variable('OKTA_BASE_URL')

