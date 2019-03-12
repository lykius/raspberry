"""
calculators/derivative_calculator.py
Process that calculates derivative of input data.
"""

from time import time

from utility.exceptions import *
from pubsub.message import Message


def derivative_calculator(in_q, out_q, out_topic, nskip):
    try:
        result = 0.0
        in_msg = in_q.get()
        last_value, last_t = in_msg.data, time()
        while True:
            in_msg = in_q.get()
            new_value, new_t = in_msg.data, time()
            result = (new_value - last_value) / (new_t - last_t)
            last_value, last_t = new_value, new_t
            out_msg = Message(out_topic, round(result, 2))
            out_q.put(out_msg)
            for n in range(nskip):
                in_q.get()
                out_q.put(out_msg)
    except:
        handle_process_exception(__name__, out_q)
