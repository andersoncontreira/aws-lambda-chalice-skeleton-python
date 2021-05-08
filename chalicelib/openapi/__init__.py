import os

import yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from chalicelib import APP_NAME, APP_VERSION
# Create an APISpec
from chalicelib.config import get_config
from chalicelib.helper import open_vendor_file
from chalicelib.logging import get_logger

servers = [
    {
        "url": os.environ["API_SERVER"] if "API_SERVER" in os.environ else None,
        "description": os.environ["API_SERVER_DESCRIPTION"] if "API_SERVER_DESCRIPTION" in os.environ else None
    }
]

if get_config().APP_ENV == "development":
    try:
        import chalicelib
        APP_TYPE = 'Chalice'
    except Exception as err:
        APP_TYPE = 'Flask'

    if APP_TYPE == 'Flask':
        dev_server = "http://localhost:5000"
    else:
        dev_server = "http://localhost:8000"

    servers.append({
        "url": os.environ["LOCAL_API_SERVER"] if "LOCAL_API_SERVER" in os.environ else dev_server,
        "description": os.environ["LOCAL_API_SERVER_DESCRIPTION"] \
            if "LOCAL_API_SERVER_DESCRIPTION" in os.environ \
            else "Development server "
    })

spec = APISpec(
    title=APP_NAME,
    openapi_version='3.0.2',
    version=APP_VERSION,
    plugins=[
        MarshmallowPlugin()
    ],
    servers=servers

)


def generate_openapi_yml(spec_object, logger, force=False):
    openapi_data = spec_object.to_yaml()

    if os.environ['APP_ENV'] == 'development' or force:
        stream = open_vendor_file("./public/swagger/openapi.yml", "w")

        if stream:
            stream.write(openapi_data)
            stream.close()


# doc
def get_doc(fn):
    logger = get_logger()
    doc_yml = ''
    try:

        fn_doc = fn.__doc__
        fn_doc = fn_doc.split('---')[-1]
        doc_yml = yaml.safe_load(fn_doc)
    except Exception as err:
        logger.error(err)
    return doc_yml
