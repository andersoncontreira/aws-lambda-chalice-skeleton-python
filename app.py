from chalicelib.boot import init, register_vendor, print_env

# execute before other codes of app
register_vendor()
init()

from chalicelib.http.controllers.api import ApiController
from chalicelib.logging import get_logger
from chalicelib import APP_NAME, helper
from chalice import Chalice

# chalice app
app = Chalice(app_name=APP_NAME)

# logger
logger = get_logger()

# Controllers
api_controller = ApiController(logger)

@app.route('/', cors=True)
def index():
    return api_controller.index(app)

@app.route('/ping', cors=True)
def ping():
    return api_controller.ping(app)

@app.route('/alive')
def alive():
    return api_controller.alive(app)

# environment
print_env(app, app.log)

# print the registered routes
helper.print_routes(app, app.log)