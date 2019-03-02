"""
calculators/derivative_calculator.py
Process that calculates derivative of input data.
"""

from time import time

from utility.exceptions import *
from pubsub.message import Message


def derivative_calculator(input_q, output_q, output_topic_name, nskip):
    try:
        result = 0.0
        in_msg = input_q.get()
        last_value, last_t = in_msg.data, time()
        while True:
            in_msg = input_q.get()
            new_value, new_t = in_msg.data, time()
            result = (new_value - last_value) / (new_t - last_t)
            last_value, last_t = new_value, new_t
            out_msg = Message(output_topic_name, round(result, 2))
            output_q.put(out_msg)
            for n in range(nskip):
                input_q.get()
                output_q.put(out_msg)
    except:
        print_exc_info(__name__)
