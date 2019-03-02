# Rasperry Pi Bluetooth test

Simple test for bluetooth communication with Raspberry Pi.

## Initial setup
In order to execute `bluetooth_test.py`, you need first to execute the following steps on Raspberry.

### Install bluetooth dev libraries
```
sudo apt-get install libbluetooth-dev
```

### Install python3 PyBluez library
```
sudo pip3 install PyBluez
```

### Enable SPP serial profile (reboot required)
```
sudo nano /etc/systemd/system/dbus-org.bluez.service
```
In this file (`/etc/systemd/system/dbus-org.bluez.service`), there's already a `ExecStart` line.  
Edit that one and add a `ExecStartPost` line, in order to get the two following lines:
```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```
Reboot to apply changes.

## Pairing from command line
Bluetooth classic requires to pair the devices before being able to communicate.  
You can use `bluetoothctl` (part of the `bluez-utils` package) as follows:
```
sudo bluetoothctl
power on
discoverable on
agent on
default-agent
pairable on
scan
pair XX:XX:XX:XX:XX:XX
```
`XX:XX:XX:XX:XX:XX` is the mac address of the device you want to pair with (get it from `scan` output).
