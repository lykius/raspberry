"""
output/network_writer.py
Process that sends data over the network.
"""

import socket
import json

from pubsub.message import Message
from utility.exceptions import *
from utility.logger import Logger

SOCKET_BUFFER_SIZE = 1024


def network_writer(address, inputs, out_q):
    logger = Logger(out_q)

    try:
        logger.log(__name__ + ' started')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(address)

            logger.log(__name__ + ' entering main loop')

            while True:
                for label, queue in inputs:
                    in_msg = queue.get()
                    out_msg = {
                        'label': label,
                        'value': in_msg.data,
                        'tag': in_msg.tag
                    }
                    json_msg = json.dumps(out_msg)
                    s.send(json_msg.encode())
                    ack = s.recv(SOCKET_BUFFER_SIZE)
    except:
        logger.log(format_current_exception(__name__))
