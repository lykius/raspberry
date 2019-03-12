"""
utility/exceptions.py
Exceptions utility.
"""

import sys

from pubsub.message import Message
from utility.consts import *


def format_current_exception(caller):
    return '### Exception in {0}: {1} - {2}'.format(caller,
                                                    sys.exc_info()[0],
                                                    sys.exc_info()[1])


def handle_process_exception(caller, q):
    s = format_current_exception(caller)
    print(s)
    q.put(Message(LOGS_TOPIC, s))
