from chalicelib.helper import get_logger
from chalicelib.services.v1 import AbstractService


class QuotationService(AbstractService):

    def __init__(self, logger=None):
        if not logger:
            logger = get_logger()
        super().__init__(logger)

    def quote(self, data):
        self.logger.info('quote', data)
        return 0

    def list(self, api_request):
        data = [{
          "quotation": '1'
        }]
        return data