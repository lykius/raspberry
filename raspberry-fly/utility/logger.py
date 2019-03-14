"""
utility/logger.py
Logger class definition.
"""

from pubsub.message import Message
from utility.consts import *


class Logger:
    def __init__(self, q):
        self.__q = q

    def log(self, s):
        self.__q.put(Message(LOGS_TOPIC, s))
