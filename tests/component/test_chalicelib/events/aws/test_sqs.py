import os
import unittest

from unittest_data_provider import data_provider

from chalicelib.config import get_config
from chalicelib.events.aws.sqs import SQSEvents
from chalicelib.logging import get_logger
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.events.aws.sqs_helper import SQSHelper
from tests.unit.helpers.api_mock_helper import get_rule_event_sample, get_rule_event_sample_error
from tests.unit.testutils import get_function_name


def get_sqs_event_sample():
    event = get_rule_event_sample()
    return (event,),


def get_sqs_event_sample_error():
    event = get_rule_event_sample_error()
    return (event,),


class SQSEventsTestCase(BaseComponentTestCase):
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

            result = SQSHelper.create_queue(queue_url)
            if result is not None:
                logger.info(f'queue {queue_name} created')
            else:
                logger.error(f'queue {queue_name} not created')

    def test_connect(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        sqs = SQSEvents()
        connection = sqs.connect()
        self.assertIsNotNone(connection)

    @data_provider(get_sqs_event_sample)
    def test_send_message(self, message):
        self.logger.info('Running test: %s', get_function_name(__name__))
        sqs = SQSEvents()
        queue_url = self.CONFIG.APP_QUEUE
        response = sqs.send_message(message, queue_url)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertTrue('MD5OfMessageBody' in response)
        self.assertTrue('MessageId' in response)


if __name__ == '__main__':
    unittest.main()
