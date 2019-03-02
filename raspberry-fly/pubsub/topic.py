"""
pubsub/topic.py
Definition of Topic class.
"""

import multiprocessing as mp


class Topic:
    def __init__(self, tag):
        self.__subscriptions = []
        self.__tag = tag

    @property
    def tag(self):
        return self.__tag

    @property
    def subscriptions(self):
        return self.__subscriptions

    def add_subscription(self):
        q = mp.Queue()
        self.__subscriptions.append(q)
        return q
