import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.DEBUG
)


def logger_info(msg: object):
    logging.info(msg)


def logger_error(msg: object):
    logging.error(msg)


def logger_warn(msg: object):
    logging.warn(msg)
