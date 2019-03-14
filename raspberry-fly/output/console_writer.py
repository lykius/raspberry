"""
output/console_writer.py
Process that writes inputs data on console (can be useful for debugging).
"""

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def console_writer(inputs, out_q):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')
        logger.log(__name__ + ' entering main loop')

        while True:
            for q in inputs:
                print(q.get())
    except:
        logger.log(format_current_exception(__name__))
