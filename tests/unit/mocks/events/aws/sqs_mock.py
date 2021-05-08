from unittest.mock import Mock

from chalicelib.events.aws.sqs import SQSEvents
from tests.unit.mocks.boto3_mocks import session_mock

_MESSAGE_SENT_MOCK = {
    'MD5OfMessageBody': '90b86613c1ace5217ec42cb79b87e5c8',
    'MessageId': '39af39a8-7c56-a0be-59b9-0f9b6341e453',
    'ResponseMetadata': {
        'RequestId': '53LHIU130912XHWZ3UEUZ85U1BTQCJKY9ELCEDPI0SAIX53FHEAN',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'content-type': 'text/html; charset=utf-8', 'content-length': '322',
            'x-amzn-requestid': '53LHIU130912XHWZ3UEUZ85U1BTQCJKY9ELCEDPI0SAIX53FHEAN',
            'x-amz-crc32': '2392011383', 'access-control-allow-origin': '*',
            'access-control-allow-methods': 'HEAD,GET,PUT,POST,DELETE,OPTIONS,PATCH',
            'access-control-allow-headers': 'authorization,content-type,content-length,content-md5,cache-control,'
                                            'x-amz-content-sha256,x-amz-date,x-amz-security-token,x-amz-user-agent,'
                                            'x-amz-target,x-amz-acl,x-amz-version-id,x-localstack-target,x-amz-tagging',
            'access-control-expose-headers': 'x-amz-version-id',
            'connection': 'close',
            'date': 'Sat, 01 May 2021 18:16:16 GMT',
            'server': 'hypercorn-h11'
        },
        'RetryAttempts': 0
    }
}


def connect():
    from chalicelib.config import get_config
    config = get_config()
    endpoint_url = config.SQS_ENDPOINT
    session = session_mock
    connection = session.resource(
        'sqs',
        endpoint_url=endpoint_url,
        region_name=config.REGION_NAME
    )

    return connection


sqs_events_mock = Mock(SQSEvents)
sqs_events_mock.connect.side_effect = connect
sqs_events_mock.send_message.return_value = _MESSAGE_SENT_MOCK
