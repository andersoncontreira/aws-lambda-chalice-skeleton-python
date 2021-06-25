import os
import boto3
from elasticsearch import Elasticsearch

from chalicelib.helper import get_protocol


def elk_is_https():
    result = False
    if 'ELASTIC_HTTPS' in os.environ and str(os.getenv('ELASTIC_HTTPS')).lower() == 'true':
        result = True
    return result


def get_elasticsearch_client(with_params=False):
    host = os.environ["ELASTIC_URL"] if "ELASTIC_URL" in os.environ else "localhost"
    port = os.environ["ELASTIC_PORT"] if "ELASTIC_PORT" in os.environ else 9200

    if with_params:
        return Elasticsearch([host],
                             use_ssl=elk_is_https(),
                             verify_certs=True,
                             scheme=get_protocol(),
                             port=port,
                             timeout=30
                             )
    else:
        return Elasticsearch([host],
                             use_ssl=elk_is_https(),
                             timeout=30
                             )
