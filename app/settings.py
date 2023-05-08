import os
import json

import structlog
import uvicorn
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

try:
    ENV = os.environ['ENV']
except KeyError:
    raise Exception("You must have a .env file in your project root "
                    "in order to run the server in your local machine. "
                    "This specifies some necessary environment variables. ")

shared_processors = (
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(),
        structlog.processors.UnicodeDecoder(),
    )


LOG_VERBOSE_FORMAT = ' '.join(['%(asctime)s [%(levelname)s]', '%(name)s.%(funcName)s %(process)d',
                               '%(thread)d %(message)s'])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': LOG_VERBOSE_FORMAT,
        },
        'json_verbose': {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            'format': LOG_VERBOSE_FORMAT,
            "foreign_pre_chain": shared_processors,
        },
    },
    'handlers': {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "json": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json_verbose",
        },
    },
    'loggers': {
        "": {
            "handlers": ["default"],
            "level": "INFO",
        },
        "uvicorn.error": {
            "handlers": ["json"],
            "level": "INFO",
        },
    }
}


SENTRY_DSN = os.environ.get('SENTRY_DSN') or ''

