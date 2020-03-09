from chalicelib.enums import CustomStringEnum


class EventType(CustomStringEnum):
    QUOTATION = 'quotation'
    CRON = 'cron'

    def __new__(cls, description):
        obj = object.__new__(cls)
        obj.description = description

        return obj


class EventSource(CustomStringEnum):
    CW = 'cloudwatch'
    S3 = 's3'
    SQS = 'sqs'
    SNS = 'sns'

    def __new__(cls, description):
        obj = object.__new__(cls)
        obj.description = description

        return obj