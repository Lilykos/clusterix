import logging
import clusterix
from colorlog import ColoredFormatter
"""Clusterix logging with color."""

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOG_FORMAT)

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)

log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


def log_info(message):
    clusterix.update_msg = message
    log.info(message)


def log_debug(message):
    log.debug(message)


def log_warn(message):
    log.warn(message)