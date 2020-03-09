from chalicelib.events import BaseEventHandler
from chalicelib.helper import get_logger
from chalicelib.services.v1.quotation import QuotationService


class QuotationEventHandler(BaseEventHandler):

    def __call__(self, event, context):
        self.event = event
        return self.handle()

    def handle(self):
        # call service here
        self.logger.info('executing quotation command')
        service = QuotationService()
        result = service.quote(self.event)
        return result
