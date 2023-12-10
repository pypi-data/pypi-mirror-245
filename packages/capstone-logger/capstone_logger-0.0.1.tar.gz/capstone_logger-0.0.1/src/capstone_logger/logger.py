import os
import sys
import logging
from logging.handlers import RotatingFileHandler

import logstash
from pythonjsonlogger import jsonlogger


class CustomJSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJSONFormatter, self).add_fields(log_record, record, message_dict)
        if log_record.get('severity'):
            log_record['severity'] = log_record.get('severity').upper()
        else:
            log_record['severity'] = record.levelname


def add_rotating_file_handler(logger, formatter):
    if os.environ.get('ENABLE_FILE_LOGGING', 'False').lower() in ['true', '1']:
        file_handler = RotatingFileHandler(f'{logger.name}.log', maxBytes=10000, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger.info('File logging is disabled')


def add_logstash_handler(logger, formatter):
    try:
        logstash_host = os.environ.get('LOGSTASH_HOST', 'logstash')
        logstash_port = int(os.environ.get('LOGSTASH_PORT', '5000'))
        handler = logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1)
        logger.addHandler(handler)
    except Exception as e:
        logger.error(f"Error connecting to Logstash: {e}")


def add_stdout_handler(logger, formatter):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)


def get_logger(name):

    logger = logging.getLogger(name)
    formatter = CustomJSONFormatter('%(asctime)s %(severity)s %(name)s %(lineno)s %(funcName)s %(message)s')

    handlers = {
        'stdout': add_stdout_handler,
        'file': add_rotating_file_handler,
        'logstash': add_logstash_handler,
    }

    for handler in handlers.values():
        handler(logger, formatter)

    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(getattr(logging, log_level))

    propagate = os.environ.get('LOG_PROPAGATE', 'False')
    logger.propagate = propagate.lower() in ['true', '1']

    return logger
