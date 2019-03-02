"""
output/bluetooth_server.py
Process that implements a server which sends data
to a client over a Bluetooth connection.

Data format:
"$LK8EX1,pressure,altitude,vspeed,temperature,battery,*checksum"
"""

import bluetooth

from utility.exceptions import *


def checksum(s):
    result = 0
    for c in s.encode():
        result ^= c
    return '{0:02X}'.format(result)


def bluetooth_server(inputs, nskip):
    try:
        data_types = [
            'pressure',
            'altitude',
            'vspeed',
            'temperature',
            'battery'
        ]

        data_converters = {
            'vspeed': 100
        }

        unavailable_data = {
            'pressure': '999999',
            'altitude': '99999',
            'vspeed': '9999',
            'temperature': '99',
            'battery': '999'
        }

        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_socket.bind(('', bluetooth.PORT_ANY))
        server_socket.listen(1)

        while True:
            print('waiting bluetooth connection...')
            client_socket, client_address = server_socket.accept()
            print('connected')
            for i in inputs:
                while not inputs[i].empty():
                    inputs[i].get_nowait()

            while True:
                try:
                    message = 'LK8EX1'
                    for t in data_types:
                        message += ','
                        if t in inputs:
                            value = inputs[t].get().data
                            value = value * data_converters.get(t, 1)
                            message += '{0:.2f}'.format(value)
                        else:
                            message += unavailable_data[t]
                    message = '$' + message + ',*' + checksum(message)
                    client_socket.sendall(message)

                    for n in range(nskip):
                        for i in inputs:
                            inputs[i].get()

                except bluetooth.BluetoothError:
                    break
    except:
        print_exc_info(__name__)
