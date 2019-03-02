"""
filters/moving_average_filter.py
Process that filters input data using moving average.
"""

from collections import deque

from utility.exceptions import *
from pubsub.message import Message


def moving_average_filter(input_q, output_q, output_topic_name):
    try:
        buffer_size = 100
        in_msg = input_q.get()
        first_value = in_msg.data
        buffer = deque([first_value for _ in range(buffer_size)], buffer_size)
        while True:
            in_msg = input_q.get()
            new_value = in_msg.data
            buffer.append(new_value)
            filtered_value = sum(buffer) / buffer_size
            out_msg = Message(output_topic_name, round(filtered_value, 2))
            output_q.put(out_msg)
    except:
        print_exc_info(__name__)
