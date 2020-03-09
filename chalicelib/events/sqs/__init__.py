import json

from chalicelib.commands import BaseCommand
from chalicelib.enums.messages import MessagesEnum
from chalicelib.exceptions import EventException
from chalicelib.helper import get_logger


class SQSEventHandler:
    EVENT_MAP = {}

    def __init__(self):
        self.logger = get_logger()

    @staticmethod
    def register(command_name, command_function):
        SQSEventHandler.EVENT_MAP[command_name] = command_function

    @staticmethod
    def register_provider(providers):
        SQSEventHandler.EVENT_MAP.update(providers)

    def process(self, event_type, event):
        """

        :param event_type:
        :param event:
        :return:
        """
        if isinstance(event, dict):
            if 'Records' in event:
                records = event['Records']
                for record in records:
                    return self._dispatch(event_type, record)
            else:
                return self._dispatch(event_type, event)

    def _dispatch(self, event_type, record):
        """

        :param dict record:
        :return:
        """

        if not isinstance(record, dict):
            if isinstance(record, tuple):
                record = dict((y, x) for x, y in record)
            elif isinstance(record, str):
                record = json.loads(record)
        if 'body' in record:
            if event_type in SQSEventHandler.EVENT_MAP:
                self.logger.error('invoking command: %s' % event_type)
                # :type BaseCommand command
                command: BaseCommand = SQSEventHandler.EVENT_MAP[event_type](record)
                return command.handle()

            else:
                self.logger.error('event type not registered')
                raise EventException(MessagesEnum.EVENT_NOT_REGISTERED_ERROR)
        pass
