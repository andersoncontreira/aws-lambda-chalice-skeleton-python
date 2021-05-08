import requests
import json

from chalicelib.logging import get_logger


class Api:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'

    def __init__(self, logger=None):
        # logger
        self.logger = logger if logger is not None else get_logger()

        self.method = None
        self.url = None
        self.body = None
        self.headers = {}
        self.accepted_codes = (200,)

    def request(self, method=None, url=None, body=None, headers: dict = None):
        if headers is None:
            headers = {}
        if method is None:
            raise Exception("Required field {} is not found".format(method))
        if url is None:
            raise Exception("Required field {} is not found".format(url))

        self.method = method
        self.url = url
        self.body = body
        self.headers = headers
        self.accepted_codes = (200,)

    def exec(self):
        headers = self.headers
        if self.body is not None:
            try:
                body = json.loads(self.body)
                response = requests.request(
                    method=self.method,
                    url=self.url,
                    json=body,
                    headers=headers
                )
            except Exception as err:
                self.logger.debug('Not a JSON body: {}'.format(err))
                body = self.body
                response = requests.request(
                    method=self.method,
                    url=self.url,
                    body=body,
                    headers=headers
                )
        else:
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=headers
            )

        return response

    def build_headers_from_string(self, headers_string):
        headers = {}
        try:
            self.logger.debug('try json string')
            headers = json.loads(headers_string)
        except Exception as err:
            self.logger.debug('Not a json string')
            headers_list = headers_string.split(",")
            for key_value in headers_list:
                data = key_value.split(':')
                if len(data) == 2:
                    key = str(data[0]).strip()
                    value = str(data[1]).strip()
                    headers[key] = value

        return headers

    def log(self, response=None):
        self.logger.info("Request: {} {}".format(self.method, self.url))
        self.logger.info("Request headers: {}".format(self.headers))
        self.logger.info("Request body: {}".format(self.body))
        if response:
            self.logger.info("Response Code: {}".format(response.status_code))
            self.logger.info("Response Content: {}".format(response.content))
            self.logger.info("Response Headers: {}".format(response.headers.items()))

    def __dict__(self):
        return {
            "method": self.method,
            "url": self.url,
            "body": self.body,
            "headers": self.headers,
            "accepted_codes": self.accepted_codes
        }

    def __str__(self):
        return str(self.__dict__())

    def to_json(self):
        return json.dumps(self.__dict__())

    def get(self, url, headers: dict = None):
        if headers is None:
            headers = {}
        self.request(self.GET, url=url, headers=headers)
        return self.exec()

    def post(self, url, body=None, headers: dict = None):
        if headers is None:
            headers = {}
        self.request(self.POST, url=url, body=body, headers=headers)
        return self.exec()
