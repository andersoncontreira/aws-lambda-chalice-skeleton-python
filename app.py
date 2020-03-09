from chalicelib.boot import init, register_vendor, print_env, load_providers

# execute before other codes of app
from chalicelib.http.controllers.v1.quotation import QuotationController

register_vendor()
init()
load_providers()

# imports
from chalicelib.events import EventHandler
from chalicelib.enums.events import EventType
from chalicelib.http.controllers.api import ApiController
from chalicelib.logging import get_logger
from chalicelib import APP_NAME, helper
from chalicelib.config import get_config
from chalice import Chalice, Rate

# chalice app
app = Chalice(app_name=APP_NAME)

# logger
logger = get_logger()

# Controllers
api_controller = ApiController(logger)
quotation_controller = QuotationController(logger)


@app.route('/', cors=True)
def index():
    return api_controller.index(app)


@app.route('/ping', cors=True)
def ping():
    return api_controller.ping(app)


@app.route('/alive')
def alive():
    return api_controller.alive(app)


@app.route('/quotation')
def list_quotation():
    return quotation_controller.list(app)


@app.on_sqs_message(queue=get_config().APP_QUEUE, batch_size=1)
def handle_sqs_message(event):
    return EventHandler.sqs(EventType.QUOTATION, event)


# @app.schedule(Rate(1, unit=Rate.HOURS))
# def every_hour(event):
#     return EventHandler.cw(EventType.QUOTATION, event)


# environment
print_env(app, app.log)

# print the registered routes
helper.print_routes(app, app.log)
