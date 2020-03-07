import copy
import json
import uuid

from chalicelib import helper
from chalicelib.control import Pagination, Order
from chalicelib.http.parsers import request_parser


class ApiRequest:
    """

    """

    def __init__(self, app=None):
        """

        :param app:
        """
        self.uuid = uuid.uuid1()
        self._request = None
        self.server_type = None
        self.fields = []
        self.limit = Pagination.LIMIT
        self.offset = Pagination.OFFSET
        self.sort_by = None
        self.order_by = Order.ASC
        self.where = {}
        self.protocol = helper.get_protocol()
        self.host = None
        self.path = None
        self.method = None
        self._request_parser = None

        if app is not None:
            self.parse_request(app)

    def get_where(self):
        return self.where

    def keys(self):
        data = self.to_dict()
        return list(data.keys())

    def __getitem__(self, item):
        try:
            value = getattr(self, item)
        except:
            value = None
        return value

    def parse_request(self, app):
        """

        :param (chalice.app.Request) request:
        :return:
        """
        self._request_parser = request_parser(app)
        parsed_request = self._request_parser.parse()

        self.fields = parsed_request.fields
        self.limit = parsed_request.limit
        self.offset = parsed_request.offset
        self.sort_by = parsed_request.sort_by
        self.order_by = parsed_request.order_by
        self.where = parsed_request.where
        self.protocol = parsed_request.protocol
        self.host = parsed_request.host
        self.path = parsed_request.path
        self.method = parsed_request.method
        self.server_type = parsed_request.server_type
        self._request = parsed_request._request

        logger = helper.get_logger()
        logger.info('Request: {}'.format(self.to_dict()))

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self.to_json())

    def to_dict(self, force_str=False):
        data = helper.to_dict(self, force_str)
        data['_request'] = None
        data['_request_parser'] = None
        # data['_request_parser'] = helper.to_dict(self._request_parser)
        # if self._request:
            # data['_request'] = self._request_parser.request_to_dict(self._request)
            # BUG fix
            # data['_request_parser'] = None
        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    def deepcopy(self, logger=None):
        tmp_request = self._request
        tmp_parser = self._request_parser

        # Remove objetos de buffer para fazer a copia
        self._request = None
        self._request_parser = None

        # BUGFIX: copy() Vai evitar a sobrescrita de valores na requisição original
        self_copy = copy.deepcopy(self)
        self_copy._request = tmp_request
        self_copy._request_parser = tmp_parser

        self._request = tmp_request
        self._request_parser = tmp_parser



        return self_copy
