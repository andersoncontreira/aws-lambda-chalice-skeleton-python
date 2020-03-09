from chalicelib.exceptions import ValidationException
from chalicelib.enums.messages import MessagesEnum
from chalicelib.validators.rules import DateTimeRule


class Validator:
    def __init__(self, logger=None):
        self.logger = logger
        self.exception = None
        self.exception_rule = None

    def validate(self, **kwargs):
        return False


class RequestValidator(Validator):
    def __init__(self):
        super().__init__()

    def validate(self, request):
        result = True

        fields = {
            'start_date': DateTimeRule,
            'end_date': DateTimeRule,
        }

        if isinstance(request, dict) and 'where' in request:
            where = request['where']
            for field, rule_class in fields.items():
                # print(field, rule_class)
                if field in where:
                    value = where[field]
                    rule = rule_class(value)
                    try:
                        rule.validate()
                    except Exception as err:
                        ex = ValidationException(MessagesEnum.VALIDATION_ERROR, err)
                        ex.set_message_params([value, field])
                        self.exception = ex
                        self.exception_rule = rule
                        result = False

                        if self.logger:
                            self.logger.error(ex)

        return result


class EventValidator(Validator):
    def __init__(self):
        super().__init__()

    def validate(self, fields, valid_fields):
        return False


class FieldValidator(Validator):
    def __init__(self):
        super().__init__()

    def validate(self, fields, valid_fields):
        return False
