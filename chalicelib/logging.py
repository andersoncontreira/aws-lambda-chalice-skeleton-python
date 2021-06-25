import os
import logging
import logstash

from chalicelib import APP_NAME
from chalicelib.logging_resources.elk import ELKHandler

_LOGGER = None


class LoggerProfile:
    CONSOLE = 'console'
    ELK = 'elk'
    LOGSTASH = 'logstash'


_LOGGER_PROFILE = LoggerProfile.CONSOLE


def set_profile(profile: LoggerProfile):
    global _LOGGER_PROFILE
    _LOGGER_PROFILE = profile


def get_logger_profile():
    global _LOGGER_PROFILE
    return _LOGGER_PROFILE


def reset():
    global _LOGGER
    _LOGGER = None


def get_log_level():
    log_level = os.app_env = logging.getLevelName(
        os.getenv("LOG_LEVEL").upper()) if 'LOG_LEVEL' in os.environ else logging.INFO
    return log_level


def get_logger(profile: LoggerProfile = None, **kwargs):
    global _LOGGER
    log_level = get_log_level()
    if not _LOGGER:
        log_name = APP_NAME
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
        logger = logging.getLogger(log_name)

        # define the profile
        if profile:
            set_profile(profile)

        # handlers by profile
        set_handler_by_profile(logger, **kwargs)

        # add log level for all
        for handler in logger.handlers:
            handler.setLevel(log_level)

        # force log level
        logger.setLevel(log_level)

        _LOGGER = logger
    else:
        logger = _LOGGER

    return logger


def set_handler_by_profile(logger: logging.Logger, **kwargs):
    global _LOGGER_PROFILE
    if _LOGGER_PROFILE != LoggerProfile.CONSOLE:
        # Remove all handlers
        logger.handlers = []
        logger.parent.handlers = []

    add_handler_by_profile(logger, **kwargs)


def add_handler_by_profile(logger: logging.Logger, **kwargs):
    global _LOGGER_PROFILE
    if _LOGGER_PROFILE == LoggerProfile.LOGSTASH:
        host = os.environ["ELASTIC_URL"] if "ELASTIC_URL" in os.environ else "localhost"
        port = int(os.environ["ELASTIC_PORT"]) if "ELASTIC_PORT" in os.environ else 9200
        version = 1

        if 'host' in kwargs:
            host = kwargs['host']

        if 'port' in kwargs:
            port = int(kwargs['port'])

        # host treat
        host = host.replace("https://", "").replace("http://", "")

        # handler = logstash.TCPLogstashHandler(host, port, version=version)
        handler = logstash.LogstashHandler(host, port, version=version)
        handler.setLevel(logger.level)
        logger.addHandler(handler)

    if _LOGGER_PROFILE == LoggerProfile.ELK:
        handler = ELKHandler(**kwargs)
        handler.setLevel(logger.level)
        logger.addHandler(handler)


def remove_handler(logger: logging.Logger, class_name):

    # parent logger
    for handler in logger.parent.handlers:
        if isinstance(handler, class_name):
            logger.parent.removeHandler(handler)

    # logger
    for handler in logger.handlers:
        if isinstance(handler, class_name):
            logger.removeHandler(handler)

