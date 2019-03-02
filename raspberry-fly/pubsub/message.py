"""
pubsub/message.py
Definition of Message class.
"""

from time import time


class Message():
    def __init__(self, topic, data, tag='', timestamp=None):
        self.__topic = topic
        self.__data = data
        self.__tag = tag
        self.__timestamp = timestamp or time()

    @property
    def topic(self):
        return self.__topic

    @property
    def data(self):
        return self.__data

    @property
    def tag(self):
        return self.__tag

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        tag = ('(' + self.__tag + ')') if len(self.__tag) > 0 else ''
        return '{0}: {1} {2}'.format(self.__topic, self.__data, tag)
