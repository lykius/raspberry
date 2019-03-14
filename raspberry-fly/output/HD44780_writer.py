"""
output/HD44780_writer.py
Process that writes data on HD44780 LCD display.
"""

from drivers.HD44780 import *
from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger


def HD44780_writer(inputs, out_q, nskip, debug):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        display = HD44780()

        logger.log(__name__ + ' entering main loop')

        while True:
            for i in inputs:
                in_msg = i['queue'].get()
                if debug:
                    s = '{0} {1}'.format(in_msg.tag, in_msg.data)
                else:
                    s = '{0}: {1:7.1f} {2}'.format(i['label'],
                                                   in_msg.data,
                                                   i['unit'])
                display.print(s, i['line'], AlignMode.LEFT)

            for n in range(nskip):
                for i in inputs:
                    i['queue'].get()
    except:
        logger.log(format_current_exception(__name__))
