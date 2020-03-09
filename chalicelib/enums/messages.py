from enum import IntEnum


class MessagesEnum(IntEnum):

    def __new__(cls, value, label, message=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.code = value
        obj.label = label
        obj.message = message
        return obj

    # Common messages 1-10
    OK = 1, 'common.success', 'Success'
    NOK = 2, 'common.error.nok', 'Error: %s'
    REQUEST_ERROR = 3, 'common.error.request_error', 'Error: %s'
    UNSUPPORTED_MEDIA_TYPE_ERROR = 4, 'common.error.unsupported_media_type_error', \
                                   'Unsupported media type: %s, supported types are (%s)'

    # Request errors 11 - 30
    LIST_ERROR = 11, 'common.error.list_error', 'Error: Unable to return the list data, please review your request'
    FILTERS_ERROR = 12, 'common.error.filters_error', 'Error: Filters must be informed'
    PARAM_REQUIRED_ERROR = 13, 'common.error.param_required_error', 'Error: Parameter %s is required'
    FIND_ERROR = 14, 'common.error.find_error', 'Error: Unable to find the specified data'
    INVALID_FILTER_ERROR = 15, 'common.error.invalid_filter_error', 'Error: Invalid filter in request'
    INVALID_FIELD_FILTER_ERROR = 16, 'common.error.invalid_filter_error', \
                                 'Error: Invalid filter value (%s) for filter (%s). Expected (%s)'

    # validation 31 - 50
    VALIDATION_ERROR = 31, 'common.error.validation_error', 'Validation error, please review your params: value (%s) for param (%s)'
    INVALID_ISO_DATE_ERROR = 32, 'common.error.invalid_iso_date', 'Invalid iso date value (%s) for param (%s)'

    # Database errors 51 - 100
    QUERY_ERROR = 51, 'common.error.query_error', 'Error: Unable to execute the query'

    # Events 101 - 200
    EVENT_NOT_REGISTERED_ERROR = 101, 'common.error.event_not_registered_error', 'Error: Event nor registered'

    # Others 201 - 300