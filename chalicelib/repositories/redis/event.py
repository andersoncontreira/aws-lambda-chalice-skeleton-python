import json
import math
from itertools import zip_longest

from chalicelib.database.redis import get_connection
from chalicelib.enums.messages import MessagesEnum
from chalicelib.exceptions import DatabaseException
from chalicelib.logging import get_logger

# iterate a list in batches of size n
from chalicelib.http_resources.request_control import Pagination


def batcher(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)


class EventRepository:
    def __init__(self, logger=None, redis_connection=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # database connection
        self.redis_connection = redis_connection if redis_connection is not None else get_connection()
        self.total = 0
        self.where = None

    def get(self, key):
        return self.redis_connection.get(key)

    def list(self, where, offset=None, limit=None, fields=None, sort_by=None, order_by=None):
        result = []
        keys = []

        scan_filter = self.redis_connection.scan_iter(where)
        scan_list = list(scan_filter)
        total = len(scan_list)

        # to avoid double count request to redis
        self.total = total
        self.where = where

        #  limit by request limit option
        for keys_tuple in batcher(scan_list, limit):
            keys.append(keys_tuple)

        pages = math.ceil(total / limit)
        if offset == Pagination.OFFSET or offset < Pagination.OFFSET:
            current_page = 1
        else:
            current_page = int(abs(math.ceil(offset / limit)))

        self.logger.info('Total items: {}'.format(total))
        self.logger.info('Pages: {}'.format(pages))
        self.logger.info('Current page: {}'.format(current_page))

        for k, keys_tuple in enumerate(keys):
            page = k + 1
            if page == current_page:

                for offset, key in enumerate(keys_tuple):
                    if key is None:
                        continue

                    key_str = key.decode()
                    value = self.redis_connection.get(key_str)
                    result.append({key_str: json.loads(value.decode())})
            else:
                continue

        return result

    def count(self, where, sort_by=None, order_by=None):
        if where == self.where:
            scan_filter = self.redis_connection.scan_iter(where)
            scan_list = list(scan_filter)
            total = len(scan_list)
            self.where = where
        else:
            total = self.total
        return {"total": total}

    def create(self, key, data):
        response = self.get(key)
        if response:
            raise DatabaseException(MessagesEnum.CREATE_ERROR)
        return self.redis_connection.set(key, data)

    def update(self, key, data):
        response = self.get(key)
        if not response:
            raise DatabaseException(MessagesEnum.UPDATE_ERROR)
        return self.redis_connection.set(key, data)

    def delete(self, key):
        response = self.get(key)
        if not response:
            raise DatabaseException(MessagesEnum.DELETE_ERROR)
        return self.redis_connection.delete(key)
