# fix config loaded
import inspect
import logging
import os

from chalicelib import APP_NAME, APP_VERSION

_CONFIG = None


class Configuration:
    # APP
    APP_ENV = 'development'
    APP_NAME = ''
    APP_VERSION = ''

    # LOG
    LOG_LEVEL = logging.INFO

    # NEW RELIC
    NEW_RELIC_DEVELOPER_MODE = 'development'
    NEW_RELIC_LICENSE_KEY = "license_key"
    NEW_RELIC_LOG_HOST = "https://log-api.newrelic.com/log/v1"

    APP_QUEUE = ""

    REDIS_HOST = ""
    REDIS_PORT = 6379
    REGION_NAME = ""

    SQS_ENDPOINT = None
    API_URL = None
    API_TOKEN = None

    def __init__(self):
        # APP
        self.APP_ENV = os.getenv("APP_ENV") if 'APP_ENV' in os.environ else 'development'
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION

        self.LOG_LEVEL = os.getenv("LOG_LEVEL") if 'LOG_LEVEL' in os.environ else self.LOG_LEVEL

        self.APP_QUEUE = os.getenv("APP_QUEUE") if 'APP_QUEUE' in os.environ else self.APP_QUEUE

        self.REDIS_HOST = os.getenv("REDIS_HOST") if 'REDIS_HOST' in os.environ else self.REDIS_HOST
        self.REDIS_PORT = os.getenv("REDIS_PORT") if 'REDIS_PORT' in os.environ else self.REDIS_PORT
        self.REGION_NAME = os.getenv("REGION_NAME") if 'REGION_NAME' in os.environ else self.REGION_NAME

        self.SQS_ENDPOINT = os.getenv("SQS_ENDPOINT") if 'SQS_ENDPOINT' in os.environ else self.SQS_ENDPOINT

        self.API_URL = os.getenv("API_URL") if 'API_URL' in os.environ else self.API_URL
        self.API_TOKEN = os.getenv("API_TOKEN") if 'API_TOKEN' in os.environ else self.API_TOKEN

    def __dict__(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return {k: v for k, v in attributes if not (k.startswith('__') and k.endswith('__'))}

    def to_dict(self):
        return self.__dict__()


def reset():
    global _CONFIG
    _CONFIG = None


def get_config():
    global _CONFIG
    if not _CONFIG:
        config = Configuration()
        _CONFIG = config
    else:
        config = _CONFIG
    return config
