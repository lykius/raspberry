"""
simulation/file_reader.py
Process that reads data from file and puts them on a queue.
"""

from utility.exceptions import *
from time import sleep
from pubsub.message import Message


def file_reader(out_q, out_topic, logs_topic, filename, sep, field, interval):
    try:
        with open(filename, 'r') as f:
            while True:
                for line in f:
                    tokens = line.split(sep)
                    out_msg = Message(out_topic, float(tokens[field]))
                    out_q.put(out_msg)
                    sleep(interval)
    except:
        s = format_current_exception(__name__)
        print(s)
        out_q.put(Message(logs_topic, s))
