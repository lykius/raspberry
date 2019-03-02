"""
output/console_writer.py
Process that writes inputs data on console (can be useful for debugging).
"""

from utility.exceptions import *


def console_writer(inputs):
    try:
        while True:
            for q in inputs:
                print(q.get())
    except:
        print_exc_info(__name__)
