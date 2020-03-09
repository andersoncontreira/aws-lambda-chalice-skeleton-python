from chalicelib.enums import EventSource, EventType
from chalicelib.events.sqs import SQSEventHandler


class EventHandler:

    @staticmethod
    def process(event_source, event_type, event):
        """

        :param EventSource event_source:
        :param EventType event_type:
        :param event:
        :return:
        """

        if event_source == EventSource.SQS:
            return SQSEventHandler().process(event_type, event)
        else:
            raise NotImplemented("Source event not implemented yet")

    @classmethod
    def cw(cls, event_type, event):
        return cls.process(EventSource.CW, event_type, event)

    @classmethod
    def s3(cls, event_type, event):
        return cls.process(EventSource.S3, event_type, event)

    @classmethod
    def sqs(cls, event_type, event):
        return cls.process(EventSource.SQS, event_type, event)

    @classmethod
    def sns(cls, event_type, event):
        return cls.process(EventSource.SQS, event_type, event)


