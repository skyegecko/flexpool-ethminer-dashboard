import logging
import sys

__version__ = '0.1.0'


def setup_logging():
    formatter = logging.Formatter(fmt="[%(asctime)s %(levelname)s]: %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    rootlogger = logging.getLogger(__name__)
    rootlogger.addHandler(handler)
    rootlogger.setLevel(logging.DEBUG)
    rootlogger.propagate = False


setup_logging()
