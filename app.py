from chalicelib.boot import init, register_vendor, print_env

# execute before other codes of app
register_vendor()
init()

# imports
from chalicelib.events.v1.quotation import QuotationEventHandler
from chalicelib.http.controllers.v1.quotation import QuotationController
from chalicelib.http.controllers.api import ApiController
from chalicelib.logging import get_logger
from chalicelib import APP_NAME, helper
from chalicelib.config import get_config
from chalice import Chalice

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
    return QuotationEventHandler(event).handle()

# environment
print_env(app, app.log)

# print the registered routes
helper.print_routes(app, app.log)
