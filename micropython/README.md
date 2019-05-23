# Experimental build of micropython for DS-D6

This build is experimental. No guarantee that it is useful or stable enough for device you don't want to take apart.

There are two versions:
- uartrepl has interactive console on TTL serial port available on USB data pins (faster, more stable choice)
- blerepl has interactive console via NUS service over bluetooth, accessible e.g. via https://aykevl.nl/apps/nus/ (a bit slow and less stable, connect to "mpus" device name)

Unlike with Espruino it cannot be switched at runtime.

# How to install

This needs newer version of bootloader and SoftDevice so the installation is more involved than SDK11 based Espruino build.
You need to install 3 following packages in that order

- [patched Desay bootloader](https://github.com/fanoush/ds-d6/blob/master/fwdump/DS-D6-desay-bootloader-fix.zip) that allows upgrading to newer major verisons of SoftDevice, if you skip this part next update package will brick your device and you will needto take it apart and restore firmware via SWD debugger
- [adafruit bootloader](https://github.com/fanoush/ds-d6/blob/master/micropython/DS-D6-adafruit-bootloader-sd132v611.zip) with SoftDevice S132 6.1.1
- micropython for SoftDevice S132 6.1.1 - in this folder

Easiest way to install is via [D6Flasher](https://play.google.com/store/apps/details?id=com.atcnetz.ble.readwrite) for more details and other ways see [DFU-update](https://github.com/fanoush/ds-d6/wiki/DFU-update).
