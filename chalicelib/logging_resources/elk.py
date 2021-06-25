import datetime
import logging

import pytz
from elasticsearch import Elasticsearch
from pythonjsonlogger.jsonlogger import JsonFormatter


class ELKHandler(logging.Handler):
    def __init__(self, es_client: Elasticsearch = None, **kwargs):
        from chalicelib.aws.elasticsearch import get_elasticsearch_client
        super().__init__()
        self.setFormatter(JsonFormatter())
        self.es_client = None
        self.last_error = None

        self.default_index = 'logstash'
        self.error_index = self.default_index

        if 'default_index' in kwargs:
            self.default_index = kwargs['default_index']
            # use the same of default
            self.error_index = kwargs['default_index']

        if 'error_index' in kwargs:
            self.error_index = kwargs['error_index']

        if 'es_client' not in kwargs:
            self.es_client = get_elasticsearch_client()
        else:
            self.es_client = es_client

    def emit(self, record: logging.LogRecord) -> None:
        record_dict = record.__dict__
        date = str(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")) + "-03:00"
        body = [{"index": {"_index": self.get_index(record), "_type": "_doc"}}, {
            "date": date,
            "action": record_dict['action'] if 'action' in record_dict else '',
            "service_name": record.name,
            "type": record.levelname.lower(),
            "message": record.msg,
            "event_name": record_dict['event_name'] if 'event_name' in record_dict else '',
            "hash": record_dict['hash'] if 'hash' in record_dict else '',
            "system": record_dict['system'] if 'system' in record_dict else '',
            "system_name": record_dict['system_name'] if 'system_name' in record_dict else ''
        }]

        try:
            self.es_client.bulk(
                body=body
            )
        except Exception as err:
            self.last_error = err

    def get_index(self, record):
        if record.levelname == logging.ERROR:
            return self.error_index
        else:
            return self.default_index
