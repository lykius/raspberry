"""
output/console_writer.py
Process that writes inputs data on console (can be useful for debugging).
"""

from utility.exceptions import *
from pubsub.message import Message


def console_writer(inputs, out_q):
    try:
        while True:
            for q in inputs:
                print(q.get())
    except:
        handle_process_exception(__name__, out_q)
