from chalicelib.helper import get_logger
from chalicelib.services.v1 import AbstractService


class QuotationService(AbstractService):

    def __init__(self):
        super().__init__(get_logger())

    def quote(self, event):
        self.logger.info('quote')
        return 0