import unittest

from chalicelib.config import get_config
from chalicelib.logging import get_logger
from tests.component.componenttestutils import BaseComponentTestCase
import app
import json

# chalice app
from unittest_data_provider import data_provider

from tests.component.helpers.events.aws.sqs_helper import SQSHelper
from tests.unit.helpers.sourcing_service_events_api_helper import get_rule_event_sample, \
    get_rule_event_sample_error, get_sqs_event_exemplo
from tests.unit.mocks.aws_mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import get_function_name

chalice_app = app.app


def get_sqs_event_sample():
    event = get_rule_event_sample()
    return (event,)


def get_queue_message():

    event = SQSHelper.get_message()
    return (event,)

def get_json_sqs_event_exemplo():
    event = get_sqs_event_exemplo()
    return (event,)

def get_multiple_queue_message():
    return (SQSHelper.get_message(),), (SQSHelper.get_message(),),  (SQSHelper.get_message(),),  (SQSHelper.get_message(),)

class AppTestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()

            queue_url = cls.CONFIG.APP_QUEUE
            queue_name = SQSHelper.get_queue_name(queue_url)
            deleted = SQSHelper.delete_queue(queue_url)
            if deleted:
                logger.info(f'Deleting queue name: {queue_name}')

            attributes = {'DelaySeconds': '1'}
            result = SQSHelper.create_queue(queue_url, attributes)
            if result is not None:
                logger.info(f'queue {queue_name} created')
            else:
                logger.error(f'queue {queue_name} not created')

            event = get_sqs_event_sample()[0]

            SQSHelper.create_message(event)
            json_list = get_json_sqs_event_exemplo()[0]

            for json_exemplo in json_list:
                SQSHelper.create_message(json.loads(json_exemplo))

            logger.info('created message: {}'.format(event))

    @data_provider(get_queue_message)
    def test_index(self, event):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.logger.info('Event: {}'.format(event))

        lambda_context = FakeLambdaContext()
        response = app.index(event=event, context=lambda_context)

        self.assertTrue(response)

    @data_provider(get_multiple_queue_message)
    def test_index_multiple(self, event):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.logger.info('Event: {}'.format(event))

        lambda_context = FakeLambdaContext()
        response = app.index(event=event, context=lambda_context)

        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
