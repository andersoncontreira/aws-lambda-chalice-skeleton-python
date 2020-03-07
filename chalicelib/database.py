import os
from time import sleep

from chalicelib.logging import get_logger

logger = get_logger()


def get_connection(retry=False):
    connection = None
    params = {
        'host': os.environ['DB_HOST'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD'],
        'db': os.environ['DB']
    }
    # db_driver = MySQLDriver()
    try:
        # connection = Connection(params, db_driver)
        # connection.connect()
        logger.info('Connected')
    except Exception as err:
        logger.info('Trying to reconnect..')

        sleep(0.1)
        # retry
        if not retry:
            return get_connection(True)

    return connection


def check_connection(connection):
    logger.info('connection.is_connected: %s' % connection.is_connected)
    if not connection.is_connected:
        logger.info('Trying to restored the connection')
        connection = get_connection()

    return connection.is_connected
