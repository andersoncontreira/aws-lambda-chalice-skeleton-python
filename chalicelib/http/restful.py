import datetime
import json
import re

from chalicelib import helper


class MetaRel:
    VIEW = 'view'
    LIST = 'list'
    CREATE = 'create'
    UPDATE = 'update'
    UPDATE_FIELD = 'update_field'
    DELETE = 'delete'


def transform_data(data):
    """

    :param data:
    :param (Hypermedia) hypermedia:
    :return:
    """
    transformed_data = {}

    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    if isinstance(data, dict) and len(data) > 0:
        for k, v in data.items():
            if isinstance(v, (datetime.date, datetime.datetime)):
                # Data pattern: ISO 8856-1
                utc = datetime.datetime.utcnow()
                v = utc.isoformat()
                # v = utc.replace(tzinfo=datetime.timezone.utc).isoformat() # 2020-01-13T20:08:44.881022+00:00
            transformed_data[k] = v

    return transformed_data


def transform_list_data(items):
    transform_list = []
    if isinstance(items, dict):
        return transform_data(items)
    for item in items:
        transform_list.append(transform_data(item))
    return transform_list


def create_href(api_request, identifier=None, href=None):
    if href is None:
        if api_request:
            host = api_request.host
            path = api_request.path
            if host and path:
                href = api_request.protocol + host + path
        else:
            href = 'unknown'
    if identifier:
        href += '/' + str(identifier)
    return href


def create_http_method(api_request, method=None):
    if api_request:
        if not method:
            method = api_request.method
    else:
        if not method:
            method = 'GET'
    return method


def create_rel(rel, identifier=None):
    if rel is None:
        rel = 'list'
        if identifier is not None:
            rel = 'get'
    return rel


class HypermediaMeta:
    def __init__(self, api_request=None):
        """

        :param (ApiRequest) api_request:
        """
        self.api_request = api_request
        self.notation = 'hypermedia_meta'

    def create(self, identifier=None, method=None, rel=None, href=None):
        return {
            'href': create_href(self.api_request, identifier, href),
            'rel': create_rel(rel),
            'method': create_http_method(self.api_request, method)
        }

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))


def href_replace_params(href, item):
    if href:
        # print(href)
        gp = re.search('(\{\w+\})', href)
        if gp:
            # print(gp.groups())
            # print(len(gp.groups()) > 0)
            if len(gp.groups()) > 0:
                for m in gp.groups():
                    key = m.replace('{', '').replace('}', '')
                    # print(key)
                    if key in item:
                        value = item[key]
                        href = href.replace(m, str(value))
        #   print(href)
    return href


class Hypermedia:
    def __init__(self, api_request=None):
        """

        :param (ApiRequest) api_request:
        """
        self.api_request = api_request
        self.meta = HypermediaMeta(api_request)

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

    def create_previous(self):
        return None

    def create_next(self):
        return None

    def create_first(self):
        return None

    def create_last(self):
        return None

    def set_api_request(self, api_request):
        self.api_request = api_request
        self.meta.api_request = api_request

    def create_links(self, identifier):
        links = [
            self.create_link(identifier, 'PATCH', MetaRel.UPDATE_FIELD),
            self.create_link(identifier, 'PUT', MetaRel.UPDATE),
            self.create_link(identifier, 'DELETE', MetaRel.DELETE)
        ]

        return links

    def create_link(self, identifier, method=None, rel=None):
        return {
            'href': create_href(self.api_request, identifier),
            'rel': create_rel(rel),
            'method': create_http_method(self.api_request, method)
        }

    def create_hypermedia_for_data(self, api_request, data, pk, href=None):

        self.set_api_request(api_request)

        if isinstance(data, list):
            for item in data:
                identifier = None
                if pk in item:
                    identifier = item[pk]

                href = href_replace_params(href, item)
                item['meta'] = self.meta.create(identifier, method='GET', rel=MetaRel.VIEW, href=href)
        elif isinstance(data, dict):
            identifier = None
            # Quando é um item unico não precisa incluir o id, pois já foi filtrado
            href = href_replace_params(href, data)
            data['meta'] = self.meta.create(identifier, method='GET', rel=MetaRel.VIEW, href=href)
        return data

    def create_hypermedia_links(self, api_request, data, pk):
        self.set_api_request(api_request)
        links = None

        if isinstance(data, list):
            for item in data:
                identifier = None
                if pk in item:
                    identifier = item[pk]
                links = self.create_links(identifier)
        elif isinstance(data, dict):
            identifier = None
            # Quando é um item unico não precisa incluir o id, pois já foi filtrado
            links = self.create_links(identifier)

        return links
