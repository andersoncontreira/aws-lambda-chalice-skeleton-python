import json

from chalice.app import SQSEvent
from chalice.app import SQSRecord

from tests.unit.helpers.aws.sqs_helper import get_sqs_event_stub, get_sqs_message_stub


def create_chalice_sqs_record(event_dict, context=None):
    event = event_dict
    if event_dict[0]:
        event = event_dict[0]
    else:
        if not 'body' in event_dict and not 'messageId' in event_dict:
            event = get_sqs_event_stub()
            event['body'] = event_dict
    sqs_record = SQSRecord(event, context)
    return sqs_record


def create_chalice_sqs_event(event_dict, context=None):
    sqs_event = event_dict
    if 'Records' not in event_dict:
        sqs_message_stub = get_sqs_message_stub()
        sqs_message_stub['body'] = json.dumps(event_dict)
        sqs_event = get_sqs_event_stub()
        records = sqs_event['Records']
        records.append(sqs_message_stub)

    return SQSEvent(sqs_event, context)
