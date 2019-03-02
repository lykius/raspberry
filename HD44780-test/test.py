"""
test.py
Simple test for HD44780 LCD display driver.
"""

from HD44780 import *
import signal
import sys
from time import time, sleep


def sigint_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

display = HD44780()

display.print("Elapsed time:", 1, AlignMode.CENTER)

t_start = time()
while True:
    display.print("{0:.3f}".format(time() - t_start), 2, AlignMode.CENTER)
    sleep(0.1)

