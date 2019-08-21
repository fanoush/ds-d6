# Experimental build of micropython for DS-D6

This build is experimental. No guarantee that it is useful or stable enough for device you don't want to take apart.

There are two versions:
- uartrepl has interactive console on TTL serial port available on USB data pins (faster, more stable choice)
- blerepl has interactive console via NUS service over bluetooth, accessible e.g. via https://aykevl.nl/apps/nus/ (a bit slow and less stable, connect to "mpus" device name)

Unlike with Espruino it cannot be switched at runtime.

# How to install

This needs newer version of bootloader and SoftDevice so the installation is more involved than SDK11 based Espruino build.
You need to install following 3 packages in that order

- [patched Desay bootloader](https://github.com/fanoush/ds-d6/blob/master/fwdump/DS-D6-desay-bootloader-noanim-fix.zip) that allows upgrading to newer major versions of SoftDevice, you must not skip this part otherwise next update package below [will brick](https://devzone.nordicsemi.com/f/nordic-q-a/16774/updating-from-s132-v2-0-x-to-s132-v3-0-0-with-dual-bank-bootloader-from-sdk-v11-0-0-does-not-work) your device and you will need to take it apart and restore firmware via SWD debugger
- [adafruit bootloader](https://github.com/fanoush/ds-d6/blob/master/micropython/DS-D6-adafruit-bootloader-sd132v611.zip) with SoftDevice S132 6.1.1
- micropython for SoftDevice S132 6.1.1 - in this folder

Easiest way to install is via [D6Flasher](https://play.google.com/store/apps/details?id=com.atcnetz.ble.readwrite) for more details and other ways see [DFU-update](https://github.com/fanoush/ds-d6/wiki/DFU-update).

# How to use

To enter bootloader for bluetooth/OTA update you can type 
```
import machine
machine.enter_ota_dfu()
```
To enter bootloader for  serial DFU update you can type 
```
import machine
machine.enter_serial_dfu()
```
