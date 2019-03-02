"""
output/network_writer.py
Process that sends data over the network.
"""

import socket
import json

from utility.exceptions import *

SOCKET_BUFFER_SIZE = 1024


def network_writer(address, inputs):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(address)
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
        print_exc_info(__name__)
