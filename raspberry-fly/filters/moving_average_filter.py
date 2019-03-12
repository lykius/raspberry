"""
filters/moving_average_filter.py
Process that filters input data using moving average.
"""

from collections import deque

from utility.exceptions import *
from pubsub.message import Message


def moving_average_filter(in_q, out_q, out_topic):
    try:
        buffer_size = 100
        in_msg = in_q.get()
        first_value = in_msg.data
        buffer = deque([first_value for _ in range(buffer_size)], buffer_size)
        while True:
            in_msg = in_q.get()
            new_value = in_msg.data
            buffer.append(new_value)
            filtered_value = sum(buffer) / buffer_size
            out_msg = Message(out_topic, round(filtered_value, 2))
            out_q.put(out_msg)
    except:
        handle_process_exception(__name__, out_q)
