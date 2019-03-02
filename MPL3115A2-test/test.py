"""
test.py
Simple test for MPL3115A2 barometric sensor driver.
"""

from MPL3115A2 import MPL3115A2
from time import sleep
import signal
import sys


def sigint_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

sensor = MPL3115A2()

while True:
    altitude = sensor.read_altitude()
    temperature = sensor.read_temperature()
    print("Altitude: {0} meters".format(altitude))
    print("Temperature: {0} °C".format(temperature))
    print("")
    sleep(1)

