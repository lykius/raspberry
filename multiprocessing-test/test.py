"""
test.py
Simple test for multiprocessing.
"""

import multiprocessing as mp
from datetime import datetime
from time import sleep
import signal
import sys

processes = []


def sigint_handler(signal, frame):
    print('Waiting processes termination...')
    for p in processes:
        p.terminate()
        p.join()
    print('Exiting')
    sys.exit(0)


def time_checker(q):
    while True:
        q.put(datetime.today())
        sleep(2)


def printer(q):
    while True:
        print('Received: ' + str(q.get()))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    print('Press CTRL+C to exit')

    mp.set_start_method('spawn')
    q = mp.Queue()
    p1 = mp.Process(target=time_checker, args=(q,))
    p2 = mp.Process(target=printer, args=(q,))
    processes.append(p1)
    processes.append(p2)
    for p in processes:
        p.start()
    while True:
        sleep(10)

