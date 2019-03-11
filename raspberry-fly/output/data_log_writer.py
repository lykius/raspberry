"""
output/log_writer.py
Process that logs input data.
"""

from utility.exceptions import *
from pubsub.message import Message


def data_log_writer(inputs, out_q, logs_topic):
    try:
        for i in inputs:
            with open(i['file'], 'w'): pass
        while True:
            for i in inputs:
                in_msg = i['queue'].get()
                with open(i['file'], 'a') as f:
                    f.write('{0},{1},{2}\n'.format(in_msg.timestamp,
                                                   in_msg.data,
                                                   in_msg.tag))
    except:
        s = format_current_exception(__name__)
        print(s)
        out_q.put(Message(logs_topic, s))
