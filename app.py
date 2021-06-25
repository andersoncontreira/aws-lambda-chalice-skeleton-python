#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import logging
import os
# execute before other codes of app
from chalicelib.boot import register_vendor
register_vendor()

from chalicelib.openapi import generate_openapi_yml, spec, get_doc, api_schemas
from chalicelib.helper import open_vendor_file
from chalicelib.http_helper import CUSTOM_DEFAULT_HEADERS
from chalicelib.config import get_config
from chalicelib.logging import get_logger, get_log_level
from chalicelib import APP_NAME, helper, http_helper, APP_VERSION
from chalice import Chalice, CustomAuthorizer

# config
config = get_config()
# debug
debug = helper.debug_mode()
# chalice app
app = Chalice(app_name=APP_NAME, debug=debug)
# logger
logger = get_logger()
# override the log instance
app.log = logger
# log if debug mode is active
logger.info("Debug Mode: {}".format(debug))
# override the log configs
if debug:
    # override to the level desired
    logger.level = logging.INFO


# general vars
APP_QUEUE = config.APP_QUEUE


@app.route('/', cors=True)
def index():
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    logger.info('Env: {} App Info: {}'.format(config.APP_ENV, body))
    return http_helper.create_response(body=body, status_code=200)


@app.route('/alive', cors=True)
def alive():
    """

    :return:

    ---

        get:
            summary: Service Health Method
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: AliveSchema
        """
    body = {"app": "I'm alive!"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/favicon-32x32.png', cors=True)
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjoWNUYYOEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKijpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaCMBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M88CWCPERr+8fLZodJ5M8QJbjbGL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWMnwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZVYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29IYwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg==')
    return http_helper.create_response(body=data, status_code=200, headers=headers)


@app.route('/docs', cors=True)
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/openapi.yml', cors=True)
def openapi():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


# @app.route('/quotation')
# def list_quotation():
#     return quotation_controller.list(app)
#
#
# @app.on_sqs_message(queue=get_config().APP_QUEUE, batch_size=1)
# def handle_sqs_message(event):
#     return QuotationEventHandler(event).handle()


# doc
spec.path(view=alive, path="/alive", operations=get_doc(alive))
# spec.path(view=event_list, path="/v1/event/{event_type}", operations=get_doc(event_list))
# spec.path(view=event_create, path="/v1/event/{event_type}", operations=get_doc(event_create))

helper.print_routes(app, logger)
logger.info('Running at {}'.format(os.environ['APP_ENV']))

# generate de openapi.yml
generate_openapi_yml(spec, logger)
