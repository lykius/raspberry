# Raspberry LCD Display test (via I2C)
Simple test to print some text on a 16X2 LCD Display.  
The display is an HD44780 from Hitachi, which provides a parallel interface for communication.  
To make things simpler (and to save some GPIOs on the Raspberry), it's possible to connect the HD44780 with a PCF8574, which converts the parallel interface to an I2C interface.  
Finally, the PCF8574 should work properly with a wide range of input voltage but, as the Raspberry GPIOs pins work at 3.3V, to avoid any kind of problems, the Raspberry is connected to the PCF8574 by the mean of a I2C Logic Level Adapter.

Code in `HD44780.py` is adapted from the several libraries available on the web (e.g. [this tutorial](http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/)).  

It took me some time to understand the way data are sent from Raspberry to the display, this is what I finally figured out:
* The HD44780 can be controlled either in 8 or 4 bits mode
* The PCF8574 is physically connected to all 16 pins of the HD44780 but, even if I didn't find any documentation about this, it is really connected only to 8 pins (4 data pins and 4 control pins)
* When you send a byte via I2C to the PCF8574, it is mapped on the HD44780 like this:  
```
D7 | D6 | D5 | D4 | BACKLIGHT | En | Rw | Rs
```

That said, the code in file `HD44780.py` is a simple implementation of what described in [HD44780 datasheet](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf).
