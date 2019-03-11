"""
output/console_writer.py
Process that writes inputs data on console (can be useful for debugging).
"""

from utility.exceptions import *
from pubsub.message import Message


def console_writer(inputs, out_q, logs_topic):
    try:
        while True:
            for q in inputs:
                print(q.get())
    except:
        s = format_current_exception(__name__)
        print(s)
        out_q.put(Message(logs_topic, s))
