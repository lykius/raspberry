"""
output/log_writer.py
Process that logs input data.
"""

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def data_log_writer(inputs, out_q):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        for i in inputs:
            with open(i['file'], 'w'): pass

        logger.log(__name__ + ' entering main loop')

        while True:
            for i in inputs:
                in_msg = i['queue'].get()
                with open(i['file'], 'a') as f:
                    f.write('{0},{1},{2}\n'.format(in_msg.timestamp,
                                                   in_msg.data,
                                                   in_msg.tag))
    except:
        logger.log(format_current_exception(__name__))
