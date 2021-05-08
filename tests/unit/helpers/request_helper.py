import json
from os import path

from chalicelib.http_resources.request import ApiRequest
from tests import ROOT_DIR


def get_sale_event_request():
    with open(path.join(ROOT_DIR, 'tests/datasources/request/protheus/sale-event.json')) as f:
        request_str = f.read()
    try:
        request_json = json.loads(request_str)
        request = ApiRequest()
        request.host = 'localhost'
        request.path = '/v1/event/sale-event'
        request.method = 'POST'
        request.server_type = "Flask"
        request.where = request_json
        return request
    except Exception as err:
        print(err)
        raise Exception('Invalid JSON')
