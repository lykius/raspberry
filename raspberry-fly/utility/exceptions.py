"""
utility/exceptions.py
Exceptions utility.
"""

import sys


def format_current_exception(caller):
    return '### Exception in {0}: {1} - {2}'.format(caller,
                                                    sys.exc_info()[0],
                                                    sys.exc_info()[1])
