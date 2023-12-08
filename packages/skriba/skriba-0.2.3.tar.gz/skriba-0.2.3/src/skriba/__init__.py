import os

from importlib.metadata import version

__version__ = version('skriba')

from skriba import *

# This installs a slick, informational tracebacks
from rich.traceback import install

install(show_locals=True)

if not os.getenv("SKRIBA_LOGGER_NAME"):
    os.environ["SKRIBA_LOGGER_NAME"] = "skriba-logger"
