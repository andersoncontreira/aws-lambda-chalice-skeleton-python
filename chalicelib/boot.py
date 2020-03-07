import os
import sys

from dotenv import load_dotenv
from chalicelib.config import get_config

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

if not current_path[-1] == '/':
    current_path += '/'


def init():
    if not 'APP_ENV' in os.environ:
        env_file_path = current_path + '.env'

        if os.path.isfile(env_file_path):
            load_dotenv(env_file_path)
        else:
            env_file_path = current_path + '/.env'
            if os.path.isfile(env_file_path):
                load_dotenv(env_file_path)

    if not 'APP_ENV' in os.environ:
        raise Exception('Environment parameters must be defined')

    load_env()


def load_env():
    environment_path = current_path + 'environment/'
    env_file_name = ('%s.env' % os.getenv("APP_ENV") if 'APP_ENV' in os.environ else 'development')
    env_file_path = environment_path + env_file_name

    if os.path.isfile(env_file_path):
        load_dotenv(env_file_path)
    else:
        environment_path = current_path + '/environment/'
        env_file_path = environment_path + env_file_name
        if os.path.isfile(env_file_path):
            load_dotenv(env_file_path)

    if not 'DB_HOST' in os.environ:
        raise Exception('Environment parameters must be defined')

    os.environ['APP_LOADED'] = str(True)


def register_vendor():
    vendor_path = current_path + "vendor"
    # print(vendor_path)
    if not os.path.isdir(vendor_path):
        vendor_path = current_path + "/vendor"
        # print(vendor_path)

    sys.path.insert(0, vendor_path)


def register_path(path):
    if os.path.isdir(path):
        sys.path.insert(0, path)

def print_env(app, logger):
    server_type = 'chalice'
    logger.info('Server: %s' % server_type)
    logger.info('Environment: %s' % os.getenv('APP_ENV'))
    logger.info('Database: %s' % os.getenv('DB_HOST'))
    logger.info('Log Level: %s' % os.getenv('LOG_LEVEL'))
    logger.info('Debug: %s' % os.getenv('DEBUG'))