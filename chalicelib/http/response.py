import json
import pickle
from http import HTTPStatus

from chalicelib import helper
from chalicelib.control import Pagination
from chalicelib.exceptions import ApiException
from chalicelib.http import ApiResponseStatus, _CUSTOM_DEFAULT_HEADERS
from chalicelib.http.restful import Hypermedia, transform_list_data
from chalicelib.enums.messages import MessagesEnum
from chalicelib.server import ServerType


class Control:
    def __init__(self, offset=None, limit=None, total=None, count=None):
        self.offset = offset
        self.limit = limit
        self.total = total
        self.count = count

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))


class Navigation:
    def __init__(self, previous=None, next=None, first=None, last=None):
        self.previous = previous
        self.next = next
        self.first = first
        self.last = last

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))


class ApiResponseBody:
    def __init__(self):
        self.status = ApiResponseStatus.OK
        self.code = ''
        self.message = ''
        self.label = ''
        self.meta = None
        self.data = None

        # control
        self.control = None

        # navigation
        self.navigation = None

        # links
        self.links = None

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return list(self.__dict__.keys())

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))


class ErrorResponse:
    def __init__(self, app, error_message):
        if isinstance(error_message, ApiException):
            exp = error_message
        else:
            exp = ApiException(MessagesEnum.REQUEST_ERROR)
            exp.set_message_params(error_message)
        response = ApiResponse()
        response.server_type = helper.get_server_type(app)
        response.set_exception(exp)

        self._response = response

    def get_response(self):
        return self._response.get_response()


class ApiResponse:
    DEFAULT_HEADERS = _CUSTOM_DEFAULT_HEADERS

    def __init__(self, api_request=None):
        # private
        self._exception = None
        self._body = None
        self._is_raw_body = False
        self._api_request = api_request

        # http
        self.status_code = HTTPStatus.OK.value
        self.headers = ApiResponse.DEFAULT_HEADERS

        self.meta = {}

        # list items
        self.items = []

        # others
        self.first = {}
        self.next = {}
        self.last = {}
        self.limit = Pagination.LIMIT
        self.offset = Pagination.LIMIT
        self.total = 0
        self.count = 0

        # hypermedia
        self.hypermedia = Hypermedia(self._api_request)
        self.links = None
        self.server_type = None

        if api_request:
            self.server_type = self._api_request.server_type

    def get_response(self):
        if self._exception is not None:
            body = ApiResponseBody()
            body.status = ApiResponseStatus.NOK

            if isinstance(self._exception, ApiException):
                code = self._exception.code
                label = self._exception.label
                message = self._exception.message
            else:
                # TODO Evitar por não ser seguro
                message = self._body if not None else str(self._exception)
                code = MessagesEnum.NOK.code
                label = MessagesEnum.NOK.label
                message = MessagesEnum.NOK.message % message

            body.code = code
            body.label = label
            body.message = message

            if self.status_code == HTTPStatus.OK:
                self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        else:
            has_meta = False
            meta = None
            data = None

            if not helper.empty(self.items):
                data = transform_list_data(self.items)
                self.count = len(self.items)
                has_meta = True

            if self._api_request:
                self.offset = self._api_request.offset
                self.limit = self._api_request.limit

            if has_meta:
                meta = self.hypermedia.meta.create()
                if isinstance(data, dict):
                    meta = self.hypermedia.meta.create(None, None, 'get')

            if data is not None:
                body = ApiResponseBody()
                body.status = ApiResponseStatus.OK
                body.code = MessagesEnum.OK.code
                body.label = MessagesEnum.OK.label
                body.message = MessagesEnum.OK.message

                # Apenas aplicável para listas
                if isinstance(data, list):
                    body.control = Control()
                    body.control.offset = self.offset
                    body.control.limit = self.limit
                    body.control.total = self.total
                    body.control.count = self.count

                    body.navigation = Navigation()
                    body.navigation.previous = self.hypermedia.create_previous()
                    body.navigation.next = self.hypermedia.create_next()
                    body.navigation.first = self.hypermedia.create_first()
                    body.navigation.last = self.hypermedia.create_last()
                else:
                    body.links = self.links

                body.meta = meta
                body.data = data
            else:
                if self._is_raw_body:
                    body = self._body
                else:
                    body = ApiResponseBody()
                    body.status = ApiResponseStatus.OK
                    body.code = MessagesEnum.OK.code
                    body.label = MessagesEnum.OK.label
                    body.message = MessagesEnum.OK.message
                    body.data = self._body
        if self.server_type == ServerType.CHALICE:
            from chalice import Response
            return Response(body=body.to_dict(), status_code=self.status_code, headers=self.headers)
        else:
            raise Exception("Only Chalice are supported for while")

    def _reset_data(self):
        self.items = []
        self._is_raw_body = False
        pass

    def set_body(self, body):
        self._body = body
        # reset
        self._reset_data()
        return self

    def set_raw_body(self, body):
        self._body = body
        # reset
        self._reset_data()
        self._is_raw_body = True
        return self

    def set_data(self, data):
        # reset
        self._reset_data()
        # data
        self._body = data
        self.items = data

    def set_total(self, total):
        self.total = total

    def set_exception(self, exception):
        self._exception = exception

    def set_links(self, links):
        self.links = links

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return list(self.__dict__.keys())

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))
