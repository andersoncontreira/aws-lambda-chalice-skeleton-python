import datetime

import chalicelib.http_resources.request
from chalicelib.enums.events import EventType
from chalicelib.vos import AbstractVO
from chalicelib.http_resources.request import ApiRequest
from chalicelib.helper import datetime_now_with_timezone, generate_hash, empty


class EventVO(AbstractVO):
    def __init__(self, event_type, request: ApiRequest):
        """

        :param event_type:
        :param (chalicelib.http_resources.request.ApiRequest) request:
        """
        self.type = event_type
        self.data = request.where
        self.date = datetime_now_with_timezone().isoformat()
        self.hash = None


_DEFAULT_EMPTY_SALE_EVENT_DATA = {
    "order_id": None,
    "products": None
}


class SaleEventVO(AbstractVO):
    def __init__(self, event_data):
        if not isinstance(event_data, dict):
            event_data = event_data.to_dict()
        self.event_type = EventType.SALE_EVENT
        self.data = event_data['data'] if 'data' in event_data else _DEFAULT_EMPTY_SALE_EVENT_DATA
        self.date = event_data['date'] if 'date' in event_data else datetime_now_with_timezone().isoformat()
        self.hash = event_data['hash'] if 'hash' in event_data else generate_hash(self.data)


_DEFAULT_EMPTY_SHARE_UPDATE_DATA = {
    "sku": None,
    "is_multisource": False,
    "multisourcing": None
}


class ShareUpdateEventVO(AbstractVO):
    def __init__(self, event_data):
        if not isinstance(event_data, dict):
            event_data = event_data.to_dict()
        self.event_type = EventType.SHARE_UPDATE
        self.data = event_data['data'] if 'data' in event_data else _DEFAULT_EMPTY_SHARE_UPDATE_DATA
        self.date = event_data['date'] if 'date' in event_data else datetime_now_with_timezone().isoformat()
        self.hash = event_data['hash'] if 'hash' in event_data else generate_hash(self.data)


class RulesEventVO(AbstractVO):
    def __init__(self, event_data):
        if not isinstance(event_data, dict):
            event_data = event_data.to_dict()
        event_type = event_data['type'] if 'type' in event_data else EventType.UNKNOWN
        data = event_data['data'] if 'data' in event_data else {}
        skus = []
        try:
            exception = None
            if EventType.from_value(event_type) == EventType.SALE_EVENT:
                if not isinstance(data['products'], list):
                    data['products'] = [data['products']]
                skus = [v['sku'] for k, v in enumerate(data['products'])]
            elif EventType.from_value(event_type) == EventType.SHARE_UPDATE:
                skus = [k for k, v in data['multisourcing'].items()]
        except Exception as err:
            exception = str(err)

        self.event_type_origin = event_type
        self.order_id = data['order_id'] if 'order_id' in data else None
        self.success = not empty(skus)
        self.skus = skus
        self.hash = event_data['hash'] if 'hash' in event_data else generate_hash(data)
        self.exception = exception
