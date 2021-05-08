from chalicelib.config import get_config
from chalicelib.helper import get_logger


class QuotationService:

    def __init__(self, logger=None, config=None,):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()

    def quote(self, data):
        self.logger.info('quote', data)
        return 0

    def list(self):
        data = [{
          "quotation": '1'
        }]
        return data