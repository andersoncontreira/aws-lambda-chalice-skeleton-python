from chalicelib.commands import QuotationCommand
from chalicelib.enums.events import EventType
from chalicelib.events.sqs import SQSEventHandler


class EventProvider:
    # Registre aqui os tipos de eventos/commandos a serem executados
    PROVIDERS = {
        EventType.QUOTATION: QuotationCommand
    }

    @staticmethod
    def boot():
        SQSEventHandler.register_provider(EventProvider.PROVIDERS)

    @staticmethod
    def register(command_name, command_function):
        EventProvider.PROVIDERS[command_name] = command_function
