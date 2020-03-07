import datetime

from chalicelib import APP_NAME, APP_VERSION, helper
from chalicelib.http.request import ApiRequest
from chalicelib.http.response import ApiResponse


class ApiController:
    def __init__(self, logger):
        self.logger = logger

    def index(self, app):
        api_request = ApiRequest(app)
        api_response = ApiResponse(api_request)
        api_response.set_body({'result': 'service: %s:%s' % (APP_NAME, APP_VERSION)})
        return api_response.get_response()

    def ping(self, app):
        api_request = ApiRequest(app)
        api_response = ApiResponse(api_request)
        api_response.set_body({'result': 'Pong'})
        return api_response.get_response()

    def alive(self, app):
        """
        Load Balancer check
        :param app:
        :return:
        """
        api_request = ApiRequest(app)
        api_response = ApiResponse(api_request)
        api_response.set_body({'result': 'I\'am alive'})
        return api_response.get_response()
