Build of Espruino with DS-D6 board.

See DFU folder for installation packages.

You can flash this via serial [DFU procedure](https://github.com/fanoush/ds-d6/wiki/DFU-update) without opening the watch.

To restore original fitness/clock app you can flash fwdump/D6-DS.zip via same procedure.

Use poke32(0x4000051c,1) in Espruino console to reboot to DFU bootloader to update Espruino or restore original app.

Espruino console should work both on USB data pins (as serial port, not usb, speed 38400) and over Blueetooth.

Currently no OLED or main DS-D6 module is included directly in the build as these are WIP. However this is not an issue since you can upload what you wish e.g. via [Espruino Web IDE](https://www.espruino.com/Web+IDE). Example you can use as a start is here https://gist.github.com/fanoush/ce461c73c299834bcb53a615721b5a2e

## How to rebuild
clone espruino repo
patch with DS-D6-espruinoXX.diff
extract targetlibs_nrf5x_11.tgz to get working sdk11 for espruino sources
make -j BOARDNAME=DSD6 BOARD=DSD6 RELEASE=1 NRF_SDK11=1 USE_BOOTLADER=1 VERBOSE=1 DFU_UPDATE_BUILD=1


