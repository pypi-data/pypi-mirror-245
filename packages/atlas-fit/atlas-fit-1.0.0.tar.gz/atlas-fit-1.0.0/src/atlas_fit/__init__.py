import logging

from .base.config import Config
from .comperator import Comperator


FORMAT = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Delete Jupyter notebook root logger handler, see https://github.com/ipython/ipython/issues/8282
logger = logging.getLogger()
logger.handlers = []

# Create root logger with default log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create console logging handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(FORMAT)
logger.addHandler(ch)
