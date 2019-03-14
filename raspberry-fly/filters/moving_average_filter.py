"""
filters/moving_average_filter.py
Process that filters input data using moving average.
"""

from collections import deque

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def moving_average_filter(in_q, out_q, out_topic):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        buffer_size = 100
        in_msg = in_q.get()
        first_value = in_msg.data
        buffer = deque([first_value for _ in range(buffer_size)], buffer_size)

        logger.log(__name__ + ' entering main loop')

        while True:
            in_msg = in_q.get()
            new_value = in_msg.data
            buffer.append(new_value)
            filtered_value = sum(buffer) / buffer_size
            out_msg = Message(out_topic, round(filtered_value, 2))
            out_q.put(out_msg)
    except:
        logger.log(format_current_exception(__name__))
