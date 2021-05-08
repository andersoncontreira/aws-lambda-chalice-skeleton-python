import re
from urllib.parse import parse_qs

from chalice.app import MultiDict

from chalicelib.http_resources import _REQUEST_IGNORED_KEYS
from chalicelib import helper
from chalicelib.http_resources.request_control import Pagination, Order, PaginationType


def filter_sql_injection(value):
    check_value = str(value).replace('-', '')
    pattern = '(select|from|where)'
    if re.search(pattern, check_value, re.I):
        value = None
    return value


def filter_fields(fields):
    filtered = None
    if isinstance(fields, list):
        filtered = []
        for v in fields:
            if v == '*':
                pass
            else:
                filtered_value = filter_sql_injection(v)
                if not helper.empty(filtered_value):
                    filtered_value = filtered_value.strip()
                    filtered.append(filtered_value)
        if len(filtered) == 0:
            filtered = None
    return filtered


class ChaliceRequestParser:
    def __init__(self, logger=None):
        self.fields = []
        self.limit = Pagination.LIMIT
        self.offset = Pagination.OFFSET
        self.sort_by = None
        self.order_by = Order.ASC
        self.where = dict()
        self.protocol = helper.get_protocol()
        self.host = None
        self.path = None
        self.method = None
        self.server_type = "Chalice"
        self._request = None
        self._logger = logger

    def set_request(self, request):
        self._request = request
        return self

    def parse(self, request=None):
        if not helper.empty(request):
            self._request = request

        request = self._request

        # headers
        if not helper.empty(request.headers):
            if 'host' in request.headers:
                self.host = request.headers['host']
        # context
        if not helper.empty(request.context):
            if 'path' in request.context:
                self.path = request.context['path']
        # method
        self.method = request.method

        # query params
        if not helper.empty(request.query_params):
            if 'sort_by' in request.query_params:
                self.sort_by = str(request.query_params['sort_by']).split(',')
                # Remove SQL injections
                self.sort_by = filter_fields(self.sort_by)
            if 'order_by' in request.query_params:
                self.order_by = Order.validate(request.query_params['order_by'])
            if 'fields' in request.query_params:
                self.fields = str(request.query_params['fields']).split(',')
                # Remove SQL injections
                self.fields = filter_fields(self.fields)

            self.offset = Pagination.validate(PaginationType.OFFSET,
                                              request.query_params.get('offset', Pagination.OFFSET))
            self.limit = Pagination.validate(PaginationType.LIMIT, request.query_params.get('limit', Pagination.LIMIT))

            # print(request.query_params['offset'])
            # print(request.query_params)
            # print(request.headers)
            # print(request.raw_body)
            # print(request.json_body)

        # ***********
        # Params
        # ***********
        # GET
        # print(request.query_params)
        if not helper.empty(request.query_params):
            for key in request.query_params:
                value = request.query_params.get(key)
                # print('GET k,v', key, value)

                # convert to list
                value = [v.strip() for v in value.split(',')]
                if len(value) == 1:
                    value = value[0]
                # print(value)

                if key not in _REQUEST_IGNORED_KEYS:
                    if key not in self.where:
                        self.where[key] = value
                    else:
                        if not isinstance(self.where[key], list):
                            wlist = [self.where[key]]
                        else:
                            wlist = self.where[key]

                        if isinstance(value, list):
                            wlist = wlist + value
                        else:
                            wlist.append(value)
                        self.where[key] = wlist

        # print('where', self.where)

        if request.method in ['POST', 'PUT']:
            # json
            if request.json_body is not None:
                self.where = request.json_body

                if self.where is None:
                    if self._logger:
                        self._logger.info('Empty JSON body')
                    self.where = {}
            # form-urlenconded
            else:
                # dict()
                request_form = parse_qs(request.raw_body.decode())
                if isinstance(request_form, dict) and not request_form == {}:
                    for k, v in request_form.items():
                        # if isinstance(v, list) and len(v) == 1:
                        #     self.where[k] = v[0]
                        # else:
                        #     self.where[k] = v
                        key = k.replace('[]', '')
                        if isinstance(request_form, MultiDict):
                            value = request_form.getlist(k)
                        else:
                            value = v
                        if isinstance(value, list) and len(value) == 1:
                            value = value[0]
                        if key in self.where:
                            current = self.where[key]
                            if isinstance(current, list):
                                self.where[key] = current + value
                            else:
                                self.where[key] = value
                        else:
                            self.where[key] = value

        # **************************
        # SQL Injection validation
        # **************************
        # print('REQUEST WHERE: ', self.where)
        filtered_where = dict()
        for k, v in self.where.items():
            filtered_where[k] = filter_sql_injection(v)
        self.where = filtered_where
        # print(self.where)
        # print('REQUEST WHERE FILTERED: ', self.where)

        return self

    def request_to_dict(self, request=None):
        if not request:
            request = self._request

        dict_object = request.to_dict()
        return dict_object