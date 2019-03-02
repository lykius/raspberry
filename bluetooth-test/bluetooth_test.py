"""
bluetooth_test.py
Simple test for bluetooth communication.
"""

import bluetooth
import signal
import sys

sockets = []


def on_exit():
    print('Closing sockets...')
    for socket in sockets:
        socket.close()
    print('Bye!\n')


def sigint_handler(signal, frame):
    print('\nCTRL+C pressed...')
    on_exit()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(('', bluetooth.PORT_ANY))
server_socket.listen(1)
print('\nSocket setup completed')
sockets.append(server_socket)

print('Waiting connection...')
client_socket, client_address = server_socket.accept()
print('Accepted connection from ' + client_address[0] + '\n')
sockets.append(client_socket)

exit = False
while not exit:
    data = client_socket.recv(1024)
    data_str = data.decode()
    print('Received: ' + data_str, flush=True)
    if data_str.upper() == 'quit'.upper():
        exit = True
    else:
        client_socket.send('Echo: ' + data_str)

print('\nQuitting...')
on_exit()

