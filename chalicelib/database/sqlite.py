import os
from time import sleep

import boto3

from chalicelib.config import get_config
from chalicelib.logging import get_logger

from sqlalchemy import create_engine

logger = get_logger()

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


def get_connection(config=None, connect=True, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
    if not _CONNECTION:
        connection = None
        if config is None:
            config = get_config()
        try:

            connection_string = 'sqlite:///:memory:'
            if config.DB:
                connection_string = 'sqlite:///%s.db' % config.DB

            connection = create_engine(connection_string, echo=True)
            if connect:
                connection.connect()
            _CONNECTION = connection
            _RETRY_COUNT = 0
            logger.info('SQLite - Connected')
        except Exception as err:
            if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                _RETRY_COUNT = 0
                logger.error(err)
                connection = None
                return connection
            else:
                logger.error(err)
                logger.info('SQLite - Trying to reconnect... {}'.format(_RETRY_COUNT))

                sleep(0.1)
                # retry
                if not retry:
                    _RETRY_COUNT += 1
                    return get_connection(config, True)
    else:
        connection = _CONNECTION

    return connection
