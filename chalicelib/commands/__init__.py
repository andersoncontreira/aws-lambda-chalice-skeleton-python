from chalicelib.helper import get_logger
from chalicelib.services.v1.quotation import QuotationService


class BaseCommand:
    def __init__(self):
        pass

    def handle(self):
        raise NotImplementedError('Base commands are not invokable by default')

    def invoke(self, ctx):
        raise NotImplementedError('Base commands are not invokable by default')


class QuotationCommand(BaseCommand):
    def invoke(self, ctx):
        pass

    def __init__(self, event):
        super().__init__()
        self.event = event
        self.logger = get_logger()
        pass

    def __call__(self, event, context):
        self.event = event
        return self.handle()

    def handle(self):
        # call service here
        self.logger.info('executing quotation command')
        service = QuotationService()
        result = service.quote(self.event)
        return result
