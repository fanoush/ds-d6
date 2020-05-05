P8 watch is one of many smartwatched supported by DaFit app (including [PineTime](https://www.pine64.org/pinetime/)). It is quite cheap (~$17 USD on aliexpress) and has full touchscreen, button and 240x240 color display.

Fortunately DaFit designers decided to not to use Nordic secure DFU bootloader and implemented their own with no fw signing via private keys :-) So thanks to atc1441's reverse engineering efforts ([video](https://youtu.be/gUVEz-pxhgg), [DaFlasher](https://play.google.com/store/apps/details?id=com.atcnetz.paatc.patc), [github](https://github.com/atc1441/DaFlasherFiles))
we now have easy way to update many of these watches without taking apart!

Also it looks like the hw/sw design of [all those watches](https://gist.github.com/atc1441/d0a3c1f5ee69ab901bccba4eb47a6e4e) is very similar:
- 4MB SPI memory (pinout: CLK=2,MOSI=3,MISO=4,CS=5) with images/fonts 
- SoftDevice S132 5.0.0
- custom bootloader at 0x78000 that can update application from SPI flash

### Choices

There are multiple ways to run your custom firmware:

1. Directly upload you application built for Nordic SDK14 with Softdevice 5.0 as a bin file (by DaFlasher)
  * most advanced but most flexible option, 'easiest' way to restore to stock, best for backups of original state including bootloader and UICR area
  * there is a size limit, app size can be 0x10000 to 0x2f0000 (~185KB)
  * to provide updates you must implement updating procedure yourself = accept new binary and store it to SPI flash and reboot to DaFit bootloader
2. Upload app that installs standard nordic DFU bootloader first and then make DFU packages for SDK14/SD5.0 via nrfutil
  * easier update via nordic tools
  * app can be larger (0x23000 to 0x78000)
  * S132 5.0 = Bluetooth 5.0
3. Upload also DFU package to upgrade/downgrade SoftDevice + DFU bootloader to move to other Nordic SDK
  * SDK12 with Softdevice S132 3.0 is default for Espruino
  * SDK11 with S132 2.0 is default for atc1441's Arduino (less bluetooth features but good enough and with most flash and RAM memory available)
  
  
### Espruino

For option 1. use `espruino-xxx-DaFit.bin` bin file and upload via DaFlasher. This allows you to backup what you want or
restore original firmware or update to DFU bootlader by hand. See below for backup/restore scripts (TODO, WIP gist [here](https://gist.github.com/fanoush/c65d0de750a87262fcdd1d91d2cdd43d))

For option 2. first use DaFlasher + atc1441's bootloader .bin and then use `espruino-xx-SDK14-SD50.zip` package - again via
DaFlasher or Nordic DFU tools. For advanced way you can also use -DaFit.bin first to install bootloader yourself via Espruino code and then use this option.

For option 3. there is now SDK11 build if you downgrade via FitBootloaderDFU2.0.1.zip to SoftDevice 2.x  
TODO - P8 espruino package for SDK12 with Espruino bootloader
