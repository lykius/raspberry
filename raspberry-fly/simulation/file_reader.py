"""
simulation/file_reader.py
Process that reads data from file and puts them on a queue.
"""

from utility.exceptions import *
from time import sleep
from pubsub.message import Message


def file_reader(output_q, output_topic_name, filename, sep, field, interval):
    try:
        with open(filename, 'r') as f:
            while True:
                for line in f:
                    tokens = line.split(sep)
                    out_msg = Message(output_topic_name, float(tokens[field]))
                    output_q.put(out_msg)
                    sleep(interval)
    except:
        print_exc_info(__name__)
