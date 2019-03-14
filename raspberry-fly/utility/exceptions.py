"""
utility/exceptions.py
Exceptions utility.
"""

import sys

from pubsub.message import Message
from utility.consts import *


def format_current_exception(caller):
    e = '### Exception in {0}: {1} - {2}'
    return e.format(caller, sys.exc_info()[0], sys.exc_info()[1])
