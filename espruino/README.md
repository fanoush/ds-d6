Build of Espruino for DS-D6

See DFU folder for installation packages.

You can flash this without opening the watch. There are currently 3 ways (for more info see [DFU procedure](https://github.com/fanoush/ds-d6/wiki/DFU-update))
- D6 Flasher Android app from your phone over bluetooth
- desay-dfu.py python flasher script from your bluetooth enabled linux computer (e.g. Raspberry Pi)
- nrfutil or adafruint-nrfutil command over TTL serial interface connected to USB data pins

To restore original fitness/clock app you can flash fwdump/D6-DS.zip via same procedure.

Use poke32(0x4000051c,1) in Espruino console to reboot to DFU bootloader to update Espruino or restore original app.

Espruino console should work both on USB data pins (as serial port, not usb, speed 38400) and over Blueetooth.

Currently no OLED or main DS-D6 module is included directly in the build as these are WIP. However this is not an issue since you can upload what you wish e.g. via [Espruino Web IDE](https://www.espruino.com/Web+IDE). Example you can use as a start is here https://gist.github.com/fanoush/ce461c73c299834bcb53a615721b5a2e

## How to rebuild
- clone espruino repo
- patch with DS-D6-espruinoXX.diff
- extract targetlibs_nrf5x_11.tgz to get working sdk11 for espruino sources
- download fonts listed in board file on lines JSMODULESOURCES+=libs/js/Font* from https://www.espruino.com/modules/ into libs/js/
- run `make -j BOARDNAME=DSD6 BOARD=DSD6 RELEASE=1 NRF_SDK11=1 USE_BOOTLADER=1 VERBOSE=1 DFU_UPDATE_BUILD=1`

**UPDATE** some version of my patch was merged in [this commit](https://github.com/espruino/Espruino/commit/f34cce8ea1e82715a16cd7895e6407f6ca914996) however the result does not build cleanly with my targetlibs_nrf5x_11.tgz listed above and needs few changes in either the sdk11 or Espruino. Let me know if you try and have some issue.
