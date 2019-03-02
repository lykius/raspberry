"""
HD44780.py
Driver for HD44780 LCD display.
"""

from smbus2 import SMBus
from time import sleep
from enum import Enum

# commands
CLEAR_DISPLAY = 0x01
RETURN_HOME = 0x02
ENTRY_MODE_SET = 0x04
DISPLAY_CONTROL = 0x08
CURSOR_SHIFT = 0x10
FUNCTION_SET = 0x20
SET_CGRAM_ADDR = 0x40
SET_DDRAM_ADDR = 0x80

# flags for display entry mode
ENTRY_RIGHT = 0x00
ENTRY_LEFT = 0x02
ENTRY_SHIFT_INCREMENT = 0x01
ENTRY_SHIFT_DECREMENT = 0x00

# flags for display control
DISPLAY_ON = 0x04
DISPLAY_OFF = 0x00
CURSOR_ON = 0x02
CURSOR_OFF = 0x00
BLINK_ON = 0x01
BLINK_OFF = 0x00

# flags for display/cursor shift
DISPLAY_MOVE = 0x08
CURSOR_MOVE = 0x00
MOVE_RIGHT = 0x04
MOVE_LEFT = 0x00

# flags for function set
EIGHT_BITS_MODE = 0x10
FOUR_BITS_MODE = 0x00
TWO_LINES = 0x08
ONE_LINE = 0x00
FIVE_TEN_DOTS = 0x04
FIVE_EIGHT_DOTS = 0x00

# flags for backlight control
BACKLIGHT_ON = 0x08
BACKLIGHT_OFF = 0x00

# line selectors
LINE_1 = 0x80
LINE_2 = 0xC0

En = 0b00000100  # enable bit
Rw = 0b00000010  # read/write bit
Rs = 0b00000001  # register select bit

I2C_DEFAULT_CHANNEL = 1
HD44780_DEFAULT_ADDRESS = 0x3F
MAX_LINE_LENGTH = 16


class BacklightMode(Enum):
    ON = 0
    OFF = 1


class AlignMode(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class HD44780:
    def __init__(self, addr=HD44780_DEFAULT_ADDRESS, channel=I2C_DEFAULT_CHANNEL):
        self.__addr = addr
        self.__bus = SMBus(channel)

        # initialization
        self.__write(0x03)
        self.__write(0x03)
        self.__write(0x03)
        self.__write(0x02)

        self.__write(FUNCTION_SET | FOUR_BITS_MODE | TWO_LINES | FIVE_EIGHT_DOTS)
        self.__write(DISPLAY_CONTROL | DISPLAY_ON | CURSOR_OFF)
        self.__write(CLEAR_DISPLAY)
        self.__write(ENTRY_MODE_SET | ENTRY_LEFT)
        sleep(0.2)

    def __write_four_bits(self, data):
        self.__bus.write_byte(self.__addr, data | BACKLIGHT_ON)
        sleep(0.0002)
        self.__bus.write_byte(self.__addr, data | En | BACKLIGHT_ON)
        sleep(0.0006)
        self.__bus.write_byte(self.__addr, data | BACKLIGHT_ON)
        sleep(0.0002)

    def __write(self, data, RwRs=0b00):
        self.__write_four_bits((data & 0xF0) | RwRs)
        self.__write_four_bits(((data << 4) & 0xF0) | RwRs)

    def backlight(self, state=BacklightMode.ON):
        if state == BacklightMode.OFF:
            self.__bus.write_byte(self.__addr, BACKLIGHT_OFF)
        else:
            self.__bus.write_byte(self.__addr, BACKLIGHT_ON)

    def clear(self):
        self.__write(CLEAR_DISPLAY)
        self.__write(RETURN_HOME)

    def print(self, string, line=1, align_mode=AlignMode.LEFT):
        if len(string) > 0:
            if line == 2:
                self.__write(LINE_2)
            else:
                self.__write(LINE_1)

            if len(string) > MAX_LINE_LENGTH:
                string_to_be_printed = string[:MAX_LINE_LENGTH]
            else:
                if align_mode == AlignMode.CENTER:
                    string_to_be_printed = string.center(MAX_LINE_LENGTH)
                elif align_mode == AlignMode.RIGHT:
                    string_to_be_printed = string.rjust(MAX_LINE_LENGTH)
                else:
                    string_to_be_printed = string.ljust(MAX_LINE_LENGTH)

            for char in string_to_be_printed:
                self.__write(ord(char), Rs)

