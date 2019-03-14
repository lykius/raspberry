"""
utility/consts.py
Constants definitions.
"""

RWALT_TOPIC = 'raw-altitude'
FLTALT_TOPIC = 'filtered-altitude'
RWVS_TOPIC = 'raw-vertical-speed'
FLTVS_TOPIC = 'filtered-vertical-speed'
LOGS_TOPIC = 'logs-topic'

INITIAL_ALT = 50
ALT_SAMPLING_INTERVAL = 0.01
VS_CALC_DERIVATIVE = False
VS_DERIVATIVE_NSKIP = 10
VS_CALC_LINREG = True
VS_LINREG_BUFFER_SIZE = 300

SEND_OVER_NETWORK = True
ALT_SERVER_ADDRESS = ('192.168.1.7', 12345)
VS_SERVER_ADDRESS = ('192.168.1.7', 56789)

LOG_DATA = False
RWALT_LOG_FILE = './logs/raw_altitude.txt'
FLTALT_LOG_FILE = './logs/filtered_altitude.txt'
RWVS_LOG_FILE = './logs/raw_vspeed.txt'
FLTVS_LOG_FILE = './logs/filtered_vspeed.txt'

PROGRAM_LOG_FILE = './logs/log.txt'
PRINT_PROGRAM_LOGS = True

DEBUG = False
SIMULATION = False
RWALT_SIMULATION_FILE = './simulation/data/raw_altitude.txt'
RWALT_SIMULATION_SEP = ','
RWALT_SIMULATION_FIELD = 1

DISPLAY_WRITER_NSKIP = 20

ENABLE_BLUETOOTH_SERVER = False
BLUETOOTH_NSKIP = 100
