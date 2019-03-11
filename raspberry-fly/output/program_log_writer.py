"""
output/program_log_writer.py
Process that logs messages from other processes.
"""

import logging
from utility.exceptions import *


def program_log_writer(filename, in_q):
    try:
        logging.basicConfig(filename=filename,
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')
        while True:
            logging.info(in_q.get().data)
    except:
        s = format_current_exception(__name__)
        print(s)
        logging.info(s)
