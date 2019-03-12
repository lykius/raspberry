"""
data/altitude/MPL3115A2.py
Process that reads altitude data from MPL3115A2 barometric sensor.
"""

from time import sleep

from drivers.MPL3115A2 import *
from utility.exceptions import *
from pubsub.message import Message


def MPL3115A2_reader(initial_altitude, out_q, out_topic, interval):
    try:
        sensor = MPL3115A2()
        sensor.set_altitude(initial_altitude)
        while True:
            altitude = sensor.read_altitude()
            msg = Message(out_topic, altitude)
            out_q.put(msg)
            sleep(interval)
    except:
        handle_process_exception(__name__, out_q)
