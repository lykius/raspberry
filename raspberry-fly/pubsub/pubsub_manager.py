"""
pubsub/pubsub_manager.py
Process that manages all subscriptions to existing topics.
"""

import multiprocessing as mp
import sys

from pubsub.message import Message
from utility.exceptions import *



def pubsub_manager(publishers_q, topics):
    indexes = {}
    for t in topics:
        indexes[t] = 0
    try:
        while True:
            in_msg = publishers_q.get()
            t, data, timestamp = in_msg.topic, in_msg.data, in_msg.timestamp
            if t in topics:
                tag = '{0}.{1}'.format(topics[t].tag, indexes[t])
                out_msg = Message(t, data, tag, timestamp)
                indexes[t] += 1
                for q in topics[t].subscriptions:
                    q.put(out_msg)
    except:
        print_exc_info(__name__)
