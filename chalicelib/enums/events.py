from chalicelib.enums import CustomStringEnum


class EventType(CustomStringEnum):
    UNKNOWN = 'unknown'
    SALE_EVENT = 'sale-event'
    SHARE_UPDATE = 'share-update'
    RULE = 'rule'

    @classmethod
    def get_public_events(cls):
        return [cls.SALE_EVENT, cls.SHARE_UPDATE]
