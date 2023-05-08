import sys

import sentry_sdk
from sentry_sdk.utils import event_from_exception


def sentry_processor(logger, method_name, d):
    """
    A custom processor to intercept log events that should be sent to sentry
    and adding necessary data to make it compliant with the log record
    expectations that sentry has.

    :param logger: logger instance
    :type logger: Object
    :param method_name: the log method, like info()/warning(), etc
    :type method_name: str
    :param d: context dictionary
    :type d: dict
    :return:
    :rtype: dict
    """
    try:
        event = {}
        hint = None

        if method_name not in {'exception', 'error', 'warning', 'warn'}:
            return d

        if method_name == 'exception' or 'exception' in d:
            event, hint = event_from_exception(sys.exc_info())

        if 'exc_info' in d:
            exc_info = d['exc_info']
            if exc_info is True:
                exc_info = sys.exc_info()
            event, hint = event_from_exception(exc_info)

        event.update({
            "logentry": {
                "message": d['event'],
                "params": d.get('positional_args')
            },
            "level": method_name,
            'extra': {"structlog-event": d}
        })

        sentry_sdk.capture_event(event, hint=hint)
    except Exception as e:
        print("Error in sentry_processor: {}".format(e))

    return d
