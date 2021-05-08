import json
from os import path
from random import randrange

from tests import ROOT_DIR


def generate_rule_event_sample():
    event = get_rule_event_sample()
    products_range = randrange(2, 5)
    share = {
        1: [100],
        2: [70, 30],
        3: [50, 30, 20],
        4: [40, 30, 20, 10],
        5: [35, 30, 20, 10, 5]
    }
    event['sku'] = 174021
    products = [{str(event['sku']) + str(value): {
        "supplier_id": value, "share": share[products_range - 1][value - 1], "sales_share": 50, "sales_count": 5,
        "enabled": 1, "quotation_enabled": 1}
    } for key, value in enumerate(range(1, products_range))]

    event['products'] = products
    return event


def get_rule_event_sample():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/api-mock/sample.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')


def get_rule_event_sample_error():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/api-mock/error.sample.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')


def get_sqs_event_exemplo():
    result = []
    with open(path.join(ROOT_DIR, 'tests/datasources/events/api-mock/sample_one.json')) as f:
        event_str = f.read()
        result.append(event_str)
    with open(path.join(ROOT_DIR, 'tests/datasources/events/api-mock/sample_two.json')) as f:
        event_str = f.read()
        result.append(event_str)
    with open(path.join(ROOT_DIR, 'tests/datasources/events/api-mock/sample_three.json')) as f:
        event_str = f.read()
        result.append(event_str)
    try:
        return result
    except:
        raise Exception('Invalid lista')


def get_staging_sqs_event_example():
    with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/sqs.staging.sample.json')) as f:
        event_str = f.read()
    try:
        return json.loads(event_str)
    except:
        raise Exception('Invalid JSON')
