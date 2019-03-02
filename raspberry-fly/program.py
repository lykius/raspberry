"""
program.py
Main program for Raspberry Fly project.
"""

import multiprocessing as mp
import signal
import sys
from time import sleep

from pubsub.pubsub_manager import pubsub_manager
from pubsub.topic import Topic
from data.altitude.MPL3115A2_reader import MPL3115A2_reader
from simulation.file_reader import file_reader
from filters.moving_average_filter import moving_average_filter
from calculators.derivative_calculator import derivative_calculator
from calculators.linreg_calculator import linreg_calculator
from output.console_writer import console_writer
from output.HD44780_writer import HD44780_writer
from output.network_writer import network_writer
from output.log_writer import log_writer
from output.bluetooth_server import bluetooth_server
from utility.exceptions import *


RWALT_TOPIC = 'raw-altitude'
FLTALT_TOPIC = 'filtered-altitude'
RWVS_TOPIC = 'raw-vertical-speed'
FLTVS_TOPIC = 'filtered-vertical-speed'

INITIAL_ALT = 50
ALT_SAMPLING_INTERVAL = 0.01
VS_CALC_DERIVATIVE = False
VS_DERIVATIVE_NSKIP = 10
VS_CALC_LINREG = True
VS_LINREG_BUFFER_SIZE = 300

SEND_OVER_NETWORK = False
ALT_SERVER_ADDRESS = ('192.168.1.77', 12345)
VS_SERVER_ADDRESS = ('192.168.1.77', 56789)

LOG_DATA = False
RWALT_LOG_FILE = './logs/raw_altitude.txt'
FLTALT_LOG_FILE = './logs/filtered_altitude.txt'
RWVS_LOG_FILE = './logs/raw_vspeed.txt'
FLTVS_LOG_FILE = './logs/filtered_vspeed.txt'

DEBUG = False
SIMULATION = False
RWALT_SIMULATION_FILE = './simulation/data/raw_altitude.txt'
RWALT_SIMULATION_SEP = ','
RWALT_SIMULATION_FIELD = 1

DISPLAY_WRITER_NSKIP = 20

ENABLE_BLUETOOTH_SERVER = True
BLUETOOTH_NSKIP = 100

processes = []


def sigint_handler(signal, frame):
    print('\nWaiting processes termination...')
    for p in processes:
        p.terminate()
        p.join()
    print('Exiting')
    sys.exit(0)


if __name__ == '__main__':
    try:
        mp.set_start_method('spawn')

        signal.signal(signal.SIGINT, signal.SIG_IGN)

        publishers_queue = mp.Queue()
        topics = {}

        rwalt_topic = Topic(tag='RA')
        fltalt_topic = Topic(tag='FA')
        rwvs_topic = Topic(tag='RV')
        fltvs_topic = Topic(tag='FV')

        if SIMULATION:
            rwalt_reader = mp.Process(target=file_reader,
                                      args=(publishers_queue, RWALT_TOPIC,
                                            RWALT_SIMULATION_FILE,
                                            RWALT_SIMULATION_SEPARATOR,
                                            RWALT_SIMULATION_FIELD,
                                            ALT_SAMPLING_INTERVAL))
        else:
            rwalt_reader = mp.Process(target=MPL3115A2_reader,
                                      args=(INITIAL_ALT, publishers_queue,
                                            RWALT_TOPIC,
                                            ALT_SAMPLING_INTERVAL))
        processes.append(rwalt_reader)

        alt_filter = mp.Process(target=moving_average_filter,
                                args=(rwalt_topic.add_subscription(),
                                      publishers_queue, FLTALT_TOPIC))
        processes.append(alt_filter)

        if VS_CALC_DERIVATIVE:
            vs_calculator = mp.Process(target=derivative_calculator,
                                       args=(fltalt_topic.add_subscription(),
                                             publishers_queue, RWVS_TOPIC,
                                             VS_DERIVATIVE_NSKIP))
        elif VS_CALC_LINREG:
            vs_calculator = mp.Process(target=linreg_calculator,
                                       args=(rwalt_topic.add_subscription(),
                                             publishers_queue, RWVS_TOPIC,
                                             VS_LINREG_BUFFER_SIZE))
        processes.append(vs_calculator)

        vs_filter = mp.Process(target=moving_average_filter,
                               args=(rwvs_topic.add_subscription(),
                                     publishers_queue, FLTVS_TOPIC))
        processes.append(vs_filter)

        alt_display_input = {
            'label': 'Alt',
            'queue': fltalt_topic.add_subscription(),
            'unit': 'm',
            'line': 1
        }
        vs_display_input = {
            'label': 'VS',
            'queue': fltvs_topic.add_subscription(),
            'unit': 'm/s',
            'line': 2
        }
        display_inputs = [alt_display_input, vs_display_input]
        display_writer = mp.Process(target=HD44780_writer,
                                    args=(display_inputs,
                                          DISPLAY_WRITER_NSKIP, DEBUG))
        processes.append(display_writer)

        if SEND_OVER_NETWORK:
            alt_network_inputs = [
                (RWALT_TOPIC, rwalt_topic.add_subscription()),
                (FLTALT_TOPIC, fltalt_topic.add_subscription())
            ]
            alt_network_writer = mp.Process(target=network_writer,
                                            args=(ALT_SERVER_ADDRESS,
                                                  alt_network_inputs))
            processes.append(alt_network_writer)

            vs_network_inputs = [
                (RWVS_TOPIC, rwvs_topic.add_subscription()),
                (FLTVS_TOPIC, fltvs_topic.add_subscription())
            ]
            vs_network_writer = mp.Process(target=network_writer,
                                           args=(VS_SERVER_ADDRESS,
                                                 vs_network_inputs))
            processes.append(vs_network_writer)

        if LOG_DATA:
            rwalt_log_input = {
                'queue': rwalt_topic.add_subscription(),
                'file': RWALT_LOG_FILE
            }

            fltalt_log_input = {
                'queue': fltalt_topic.add_subscription(),
                'file': FLTALT_LOG_FILE
            }

            rwvs_log_input = {
                'queue': rwvs_topic.add_subscription(),
                'file': RWVS_LOG_FILE
            }

            fltvs_log_input = {
                'queue': fltvs_topic.add_subscription(),
                'file': FLTVS_LOG_FILE
            }

            log_writer = mp.Process(target=log_writer,
                                    args=([rwalt_log_input, fltalt_log_input,
                                           rwvs_log_input, fltvs_log_input],))
            processes.append(log_writer)

        topics[RWALT_TOPIC] = rwalt_topic
        topics[FLTALT_TOPIC] = fltalt_topic
        topics[RWVS_TOPIC] = rwvs_topic
        topics[FLTVS_TOPIC] = fltvs_topic

        if DEBUG:
            console_writer_inputs = [topics[t].add_subscription()
                                     for t in topics]
            console_writer = mp.Process(target=console_writer,
                                        args=(console_writer_inputs,))
            processes.append(console_writer)

        if ENABLE_BLUETOOTH_SERVER:
            bluetooth_server_inputs = {
                'altitude': fltalt_topic.add_subscription(),
                'vspeed': fltvs_topic.add_subscription() 
            }
            bluetooth_server = mp.Process(target=bluetooth_server,
                                          args=(bluetooth_server_inputs,
                                                BLUETOOTH_NSKIP))
            processes.append(bluetooth_server)

        pubsub_manager = mp.Process(target=pubsub_manager,
                                    args=(publishers_queue, topics))
        processes.append(pubsub_manager)

        for p in processes:
            p.start()

        signal.signal(signal.SIGINT, sigint_handler)
        while True:
            sleep(100)
    except:
        print_exc_info(__name__)
