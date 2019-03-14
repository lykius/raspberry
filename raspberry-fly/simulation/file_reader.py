"""
simulation/file_reader.py
Process that reads data from file and puts them on a queue.
"""

from time import sleep

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def file_reader(out_q, out_topic, filename, sep, field, interval):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        with open(filename, 'r') as f:
            logger.log(__name__ + ' entering main loop')

            while True:
                for line in f:
                    tokens = line.split(sep)
                    out_msg = Message(out_topic, float(tokens[field]))
                    out_q.put(out_msg)
                    sleep(interval)
    except:
        logger.log(format_current_exception(__name__))
