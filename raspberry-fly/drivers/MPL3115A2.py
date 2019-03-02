"""
drivers/MPL3115A2.py
Driver for MPL3115A2 barometric sensor.
"""

from smbus2 import SMBus
from time import sleep

# registers
STATUS = 0x00  # status
OUT_P_MSB = 0x01  # pressure/altitude[19:12]
OUT_P_CSB = 0x02  # pressure/altitude[11:4]
OUT_P_LSB = 0x03  # pressure/altitude[3:0]
OUT_T_MSB = 0x04  # temperature[11:4]
OUT_T_LSB = 0x05  # temperature[3:0]
PT_DATA_CFG = 0x13  # data event flag configuration
CTRL_REG1 = 0x26  # control register 1
OFF_H = 0x2D  # altitude offset

# STATUS masks
PTDR = 0b00001000  # pressure/altitude or temperature data available
PDR = 0b00000100  # pressure/altitude data available
TDR = 0b00000010  # temperature data available

# PT_DATA_CFG masks
DREM = 0b00000100  # data ready event mode
PDEFE = 0b00000010  # data event flag enable on new pressure/altitude
TDEFE = 0b00000001  # data event flag enable on new temperature data

# CTRL_REG1 masks
ALT = 0b10000000  # sets sensor in altimeter mode
OST = 0b00000010  # initiates a measurement immediately
SBYB = 0b00000001  # sets sensor in ACTIVE mode

I2C_DEFAULT_CHANNEL = 1
MPL3115A2_DEFAULT_ADDRESS = 0x60


class MPL3115A2:
    def __init__(self, addr=MPL3115A2_DEFAULT_ADDRESS,
                 channel=I2C_DEFAULT_CHANNEL):
        self.__addr = addr
        self.__bus = SMBus(channel)
        self.__bus.write_byte_data(self.__addr, PT_DATA_CFG,
                                   DREM | PDEFE | TDEFE)

    def __altitude_data_ready(self):
        status = self.__bus.read_byte_data(self.__addr, STATUS)
        return (status & PDR) == PDR

    def __temperature_data_ready(self):
        status = self.__bus.read_byte_data(self.__addr, STATUS)
        return (status & TDR) == TDR

    def set_altitude(self, altitude):
        while self.__altitude_data_ready():
            self.__bus.read_i2c_block_data(self.__addr, OUT_P_MSB, 3)
        self.__bus.write_byte_data(self.__addr, OFF_H, 0)

        altitude_offset = round(altitude - self.read_altitude())
        altitude_offset = -128 if altitude_offset < -128 else altitude_offset
        altitude_offset = 127 if altitude_offset > 127 else altitude_offset
        altitude_offset_b = altitude_offset.to_bytes(1, 'big', signed=True)[0]
        self.__bus.write_byte_data(self.__addr, OFF_H, altitude_offset_b)

    def read_altitude(self):
        self.__bus.write_byte_data(self.__addr, CTRL_REG1, ALT | OST)

        while not self.__altitude_data_ready():
            pass

        alt_data = self.__bus.read_i2c_block_data(self.__addr, OUT_P_MSB, 3)
        alt_int = int.from_bytes([alt_data[0], alt_data[1]],
                                 byteorder='big', signed=True)
        alt_fract = alt_data[2] >> 4
        altitude = alt_int + (alt_fract / 16)
        return altitude

    def read_temperature(self):
        self.__bus.write_byte_data(self.__addr, CTRL_REG1, ALT | OST)

        while not self.__temperature_data_ready():
            pass

        t_data = self.__bus.read_i2c_block_data(self.__addr, OUT_T_MSB, 2)
        t_int = int.from_bytes([t_data[0]], byteorder='big', signed=True)
        t_fract = t_data[1] >> 4
        t = t_int + (t_fract / 16)
        return t
