"""
output/program_log_writer.py
Process that logs messages received on the input queue.
"""

import logging
from utility.exceptions import *
from utility.consts import *


def program_log_writer(filename, in_q):
    try:
        logging.basicConfig(filename=filename,
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

        logging.info(__name__ + ' started')
        logging.info(__name__ + ' entering main loop')

        while True:
            s = in_q.get().data
            logging.info(s)
            if PRINT_PROGRAM_LOGS:
                print(s)
    except:
        s = format_current_exception(__name__)
        print(s)
        logging.info(s)
