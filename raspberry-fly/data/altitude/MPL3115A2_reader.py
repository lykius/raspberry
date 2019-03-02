"""
data/altitude/MPL3115A2.py
Process that reads altitude data from MPL3115A2 barometric sensor.
"""

from time import sleep

from drivers.MPL3115A2 import *
from utility.exceptions import *
from pubsub.message import Message


def MPL3115A2_reader(initial_altitude, output_q, output_topic_name, interval):
    try:
        sensor = MPL3115A2()
        sensor.set_altitude(initial_altitude)
        while True:
            altitude = sensor.read_altitude()
            msg = Message(output_topic_name, altitude)
            output_q.put(msg)
            sleep(interval)
    except:
        print_exc_info(__name__)
