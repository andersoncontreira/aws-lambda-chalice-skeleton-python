import json
import unittest

from unittest_data_provider import data_provider

from chalicelib.enums import EventType
from chalicelib.events import EventHandler
from tests.functional.functionaltestutils import ROOT_DIR
from tests.unit.testutils import BaseUnitTest


def get_sqs_fifo_event_sample():
    with open(ROOT_DIR + '/../datasources/events/sqs/fifo.json') as f:
        event_str = f.read()
    fifo = json.loads(event_str)
    return (fifo,),


def get_sqs_standard_event_sample():
    with open(ROOT_DIR + '/../datasources/events/sqs/standard.json') as f:
        event_str = f.read()
    fifo = json.loads(event_str)
    return (fifo,),


class EventHandlerTestCase(BaseUnitTest):

    @data_provider(get_sqs_fifo_event_sample)
    def test_fifo_handle_event(self, event):
        result = EventHandler.sqs(EventType.QUOTATION, event)
        self.logger.info(result)
        self.assertIsNotNone(result)

    @data_provider(get_sqs_standard_event_sample)
    def test_standard_handle_event(self, event):
        result = EventHandler.sqs(EventType.QUOTATION, event)
        self.logger.info(result)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
