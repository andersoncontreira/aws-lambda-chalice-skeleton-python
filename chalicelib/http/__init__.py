import os

from chalicelib import APP_ARCH_VERSION, APP_VERSION

_REQUEST_IGNORED_KEYS = ['sort_by', 'order_by', 'offset', 'limit', 'fields']

_OFFSET_DEFAULT = 0
_LIMIT_DEFAULT = 20

# https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Controle_Acesso_CORS
# custom headers of the app
_CUSTOM_DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Custom-Arch-Version': APP_ARCH_VERSION,
    'Custom-Service-Version': APP_VERSION,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS, GET, POST, PATH, PUT, DELETE',
    # 'Access-Control-Allow-Headers': 'Content-Type'
}

class ApiResponseStatus:
    OK = 'OK'
    NOK = 'NOK'
