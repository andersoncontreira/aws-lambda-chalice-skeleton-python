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
            params = {
                'host': config.DB_HOST,
                'user': config.DB_USER,
                'password': config.DB_PASSWORD,
                'db': config.DB
            }

            # connection = create_engine('sqlite:///:memory:', echo=True)
            # utf8mb4
            connection = create_engine(
                "mysql+pymysql://%s:%s@%s/%s?charset=utf8" %
                (params['user'], params['password'], params['host'], params['db']),
                echo=True)

            if connect:
                connection.connect()
            _CONNECTION = connection
            _RETRY_COUNT = 0
            logger.info('MySQL - Connected')
        except Exception as err:
            if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                _RETRY_COUNT = 0
                logger.error(err)
                connection = None
                return connection
            else:
                logger.error(err)
                logger.info('MySQL - Trying to reconnect... {}'.format(_RETRY_COUNT))

                sleep(0.1)
                # retry
                if not retry:
                    _RETRY_COUNT += 1
                    return get_connection(config, True)
    else:
        connection = _CONNECTION

    return connection
