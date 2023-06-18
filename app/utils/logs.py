import logging
import json

class CustomFormatter(logging.Formatter):
    def format(self, record):
        super(CustomFormatter, self).format(record)
        fields = ['levelname', 'pathname', 'lineno', 'message']
        output = {k: str(record.__dict__.get(k)) for k in fields}
        return json.dumps(output)

def set_logger(name):
    LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR
    }
    logging_formatter = CustomFormatter()
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(logging_formatter)
    logger = logging.getLogger(name)
    logger.setLevel(LEVELS["INFO"])
    logger.addHandler(logging_handler)
    return logger