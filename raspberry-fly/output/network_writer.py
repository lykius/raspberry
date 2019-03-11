"""
output/network_writer.py
Process that sends data over the network.
"""

import socket
import json

from utility.exceptions import *
from pubsub.message import Message


SOCKET_BUFFER_SIZE = 1024


def network_writer(address, inputs, out_q, logs_topic):
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
        s = format_current_exception(__name__)
        print(s)
        out_q.put(Message(logs_topic, s))
