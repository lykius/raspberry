"""
pubsub/pubsub_manager.py
Process that manages all subscriptions to existing topics.
"""

import multiprocessing as mp
import sys

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def pubsub_manager(in_q, topics, out_q):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        indexes = {}
        for t in topics:
            indexes[t] = 0

        logger.log(__name__ + ' entering main loop')

        while True:
            in_msg = in_q.get()
            t, data, timestamp = in_msg.topic, in_msg.data, in_msg.timestamp
            if t in topics:
                tag = '{0}.{1}'.format(topics[t].tag, indexes[t])
                out_msg = Message(t, data, tag, timestamp)
                indexes[t] += 1
                for q in topics[t].subscriptions:
                    q.put(out_msg)
    except:
        logger.log(format_current_exception(__name__))
