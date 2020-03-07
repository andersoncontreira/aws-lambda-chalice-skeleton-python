from unittest.mock import Mock

from chalice.app import Request, MultiDict, CaseInsensitiveMapping

query_params = {}
headers = {}
request = Mock(spec=Request)
request.query_params = MultiDict(query_params)
request.headers = CaseInsensitiveMapping(headers)
request.context = {}
request.uri_params = {}
request.method = ''
request._is_base64_encoded = False
request._body = ''
request._json_body = None
request._raw_body = b''
request.stage_vars = {}
