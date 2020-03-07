import configparser
import logging
import os

from chalicelib import APP_NAME, APP_VERSION

ini_parser = configparser.ConfigParser()

_CONFIG = None


# Default values
class Configuration:
    # APP
    APP_ENV = 'development'
    APP_NAME = ''
    APP_VERSION = ''
    APP_HOST = ''

    PORT = 8000
    HTTPS = False
    APP_LOADED = False

    # DB
    DB_HOST = ''
    DB_USER = ''
    DB_PASSWORD = ''
    DB = ''

    # LOG
    LOG_LEVEL = logging.INFO

    # NEW RELIC
    NEW_RELIC_DEVELOPER_MODE = 'development'
    NEW_RELIC_LICENSE_KEY = "license_key"
    NEW_RELIC_LOG_HOST = "https://log-api.newrelic.com/log/v1"

    def __init__(self):
        if not 'APP_ENV' in os.environ:
            raise Exception('boot.init() must be called')

        self.APP_ENV = os.getenv("APP_ENV") if 'APP_ENV' in os.environ else 'development'
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION
        self.APP_HOST = os.getenv("APP_HOST") if 'APP_HOST' in os.environ else 'localhost'
        self.PORT = os.getenv("PORT") if 'PORT' in os.environ else self.PORT
        self.APP_LOADED = os.getenv("APP_LOADED") if 'APP_LOADED' in os.environ else False
        self.LOG_LEVEL = os.app_env = logging.getLevelName(
            os.getenv("LOG_LEVEL").upper()) if 'LOG_LEVEL' in os.environ else logging.INFO

        self.load_newrelic_props()

    def load_newrelic_props(self, config_file=None):

        self.NEW_RELIC_DEVELOPER_MODE = os.getenv(
            "NEW_RELIC_DEVELOPER_MODE") if 'NEW_RELIC_DEVELOPER_MODE' in os.environ \
            else self.APP_ENV
        self.NEW_RELIC_LOG_HOST = os.getenv(
            "NEW_RELIC_LOG_HOST") if 'NEW_RELIC_LOG_HOST' in os.environ \
            else self.NEW_RELIC_LOG_HOST

        if config_file:
            ini_parser.read(config_file)
            if ini_parser.sections():
                self.NEW_RELIC_LICENSE_KEY = ini_parser.get('newrelic', 'license_key')
        else:
            self.NEW_RELIC_LICENSE_KEY = os.getenv(
                "NEW_RELIC_LICENSE_KEY") if 'NEW_RELIC_LICENSE_KEY' in os.environ \
                else self.NEW_RELIC_LICENSE_KEY


def get_config():
    global _CONFIG
    if not _CONFIG:
        config = Configuration()
    else:
        config = _CONFIG
    return config
