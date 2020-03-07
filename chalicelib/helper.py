# import datetime
# import json
# import os
# import re
#
# from dateutil.parser import isoparse, parser
#
import json
import os

from chalicelib.server import ServerType
#
#
# def query_param(app, param_name, default):
#     if app is not None and app.current_request is not None:
#         return app.current_request.query_params and app.current_request.query_params.get(param_name)
#     else:
#         return default
#
#
def empty(where):
    result = False
    if isinstance(where, dict) and where == {}:
        result = True
    elif isinstance(where, list) and len(where) == 0:
        result = True
    elif isinstance(where, str) and where == '':
        result = True
    elif isinstance(where, bytes) and len(where) == 0:
        result = True
    elif where is None:
        result = True
    return result
#
#
# def filter_sql_injection(value):
#     check_value = str(value).replace('-', '')
#     pattern = '(select|from|where)'
#     if re.search(pattern, check_value, re.I):
#         value = None
#     return value
#
#
# def filter_fields(fields):
#     filtered = None
#     if isinstance(fields, list):
#         filtered = []
#         for v in fields:
#             if v == '*':
#                 pass
#             else:
#                 filtered_value = filter_sql_injection(v)
#                 if not empty(filtered_value):
#                     filtered_value = filtered_value.strip()
#                     filtered.append(filtered_value)
#         if len(filtered) == 0:
#             filtered = None
#     return filtered
#
#
# def gt_zero(param, default):
#     # print('param', param, int(param))
#     try:
#         return int(param) if int(param) > 0 else default
#     except:
#         return default
#
#
def print_routes(app, logger):
    """

    :param logger:
    :param (chalice.Chalice) app:
    :return:
    """
    logger.info('List of routes:')
    if has_attr(app, 'get_routes'):
        routes = app.get_routes()
    elif has_attr(app, 'url_map'):
        routes = {rule.rule: dict.fromkeys(rule.methods, 0) for rule in app.url_map.iter_rules()}
    else:
        routes = app.routes
    for path, dict_route in routes.items():
        method = list(dict_route.keys()).pop()
        logger.info('Route: %s - %s', method, path)
        # print('Route: %s - %s' % (method, path))
#
#
# def validate_field(field, entity_fields):
#     filtered = None
#     if entity_fields and field in entity_fields:
#         filtered = field
#     return filtered
#
#
# def validate_fields(fields, entity_fields):
#     # print('fields', fields)
#     # print(entity_fields)
#     filtered = None
#     if isinstance(fields, list):
#         filtered = []
#         for field in fields:
#             validated = validate_field(field, entity_fields)
#             if validated:
#                 filtered.append(validated)
#     return filtered
#
#
def has_attr(object, attribute):
    try:
        if hasattr(object, attribute):
            return True
    except Exception as err:
        return False
#
#
# def get_current_datetime():
#     return datetime.datetime.utcnow()
#
#
# def get_datetime_interval(days):
#     interval = datetime.timedelta(days=days)
#     return datetime.datetime.utcnow() + interval
#
#
# def parse_string_date(str_date, iso_format=True):
#     # print('xxx', str_date)
#     if iso_format:
#         date = isoparse(str_date)
#     else:
#         date_parser = parser()
#         date = date_parser.parse(str_date, None)
#     return date
#
#
def get_logger():
    from chalicelib.logging import get_logger
    logger = get_logger()
    logger.info('Imported log locally')
    return logger
#
#
# def get_newrelic_logger():
#     from newrelic_api_log_handler.logging import get_logger
#     logger = get_logger()
#     return logger
#
#

def get_server_type(app):
    server_type = ServerType.CHALICE
    return server_type


def to_dict(obj, force_str=False):
    data = obj.__dict__
    if force_str:
        return {k: str(v) for k, v in data.items() if v is not None}
    else:
        # return {k: v for k, v in data.items() if v is not None}
        _dict = {}
        for k, v in data.items():
            if getattr(v, "to_dict", None):
                # recursivo
                _dict[k] = to_dict(v, force_str)
            else:
                _dict[k] = v
        return _dict


def to_json(obj):
    return json.dumps(obj)


def get_protocol():
    protocol = 'http://'
    if is_https():
        protocol = 'https://'
    return protocol


def is_https():
    result = False
    if 'HTTPS' in os.environ and str(os.getenv('HTTPS')).lower() == 'true':
        result = True
    return result
