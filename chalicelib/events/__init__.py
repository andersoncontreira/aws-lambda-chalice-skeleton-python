from chalicelib.helper import get_logger


class BaseEventHandler:
    def __init__(self, event):
        self.event = event
        self.logger = get_logger()

    def handle(self):
        pass


