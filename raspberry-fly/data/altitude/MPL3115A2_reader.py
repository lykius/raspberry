"""
data/altitude/MPL3115A2.py
Process that reads altitude data from MPL3115A2 barometric sensor.
"""

from time import sleep

from drivers.MPL3115A2 import *
from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def MPL3115A2_reader(initial_altitude, out_q, out_topic, interval):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        sensor = MPL3115A2()
        sensor.set_altitude(initial_altitude)

        logger.log(__name__ + ' entering main loop')

        while True:
            altitude = sensor.read_altitude()
            msg = Message(out_topic, altitude)
            out_q.put(msg)

            sleep(interval)
    except:
        logger.log(format_current_exception(__name__))
