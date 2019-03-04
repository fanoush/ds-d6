# DS-D6
Custom firmware for Desay/MPow DS-D6  nRF52832 bracelet

Also works on [Mpow DS-D9/Lenovo HW02](https://fccid.io/2AEMN-D9/)

## Where to get the device

Sold in various places like  ebay. I got it from GearBest https://www.gearbest.com/smart-watches/pp_1232618.html?wid=1433363 In recent months it is quite often on sale for $9.99 (lowest so far was 7.99). The price changes often (sometimes even multiple times per day) so if it is for full price you may try to wait few days (or hours). Sometimes the discount is only valid in their mobile app. **UPDATE 26.02.2019** looks like Gearbest is out of stock already for some time so there are just random sellers on ebay/aliexpress with price that is no longer interesting. 

## HW reference
DS-D6 FCC info https://fccid.io/2AEMN-D6/

Direct links to internal photos
- https://fccid.io/png.php?id=3414019&page=0 
- https://fccid.io/png.php?id=3414019&page=1 battery, HR sensor
- https://fccid.io/png.php?id=3414019&page=2 SWD test points (CLK,DIO), USB data pins marked as TX,RX (serial UART)
- https://fccid.io/png.php?id=3414019&page=3 CPU N53832

#### my findings about HW documented here https://github.com/fanoush/ds-d6/wiki/Hardware

## Status

- all/most hardware known and documented
- it is possible to [update and restore device via serial DFU](https://github.com/fanoush/ds-d6/wiki/DFU-update) without opening it as long as you app is developed with Nordic SDK11 and SoftDevice 2.0.x
- recent build of Espruino (2.01) works with all hardware with no issues, flashable DFU package [here](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU)


All stuff documented in WIKI **https://github.com/fanoush/ds-d6/wiki**

Initial progress (for historic reasons) here
https://gitter.im/nRF51822-Arduino-Mbed-smart-watch/Lobby?at=5be3fbf36b9822140df92510


Firmware in fwdump folder was dumped via gdb over SWD as seen below (using bluepill board flashed with blackmagic probe firmware). Restoring over SWD works.

```gdb
(gdb) info mem
Using memory regions provided by the target.
Num Enb Low Addr   High Addr  Attrs 
0   y      0x00000000 0x00080000 flash blocksize 0x1000 nocache 
1   y      0x10001000 0x10001100 flash blocksize 0x100 nocache 
2   y      0x20000000 0x20010000 rw nocache 

(gdb) dump memory dsd6-flash.bin 0x00000000 0x00080000
(gdb) dump memory d6d6-uicr.bin 0x10001000 0x10001100
```


## Other  devices made by Desay

### HX-06

There is similar bracelet without HR sensor - Lenovo HX06 https://www.gearbest.com/smart-watches/pp_1830584.html?wid=1433363 (lowest so far for $11.99). It is made by same manufacturer and shares app and the screen looks the same. Also the FCC info seems promising https://fccid.io/2AEMN-D16/ - CPU marking is unreadable but board looks very similar to DS-D6 and there are SWD test points (= ARM Cortex M architecture) so I ordered that one too, still waiting. **UPDATE 7.12.2018 sadly after receiving it I found HX06 is not Nordic based but has Dialog [14585/6](https://www.dialog-semiconductor.com/products/connectivity/bluetooth-low-energy/smartbond-da14585-and-da14586) chip** There is SDK available from Dialog however the chip architecture is not suitable for large codebase e.g. for Espruino.  There is 96KB of SRAM for both data and code, code is mirrored at poweron from SPI FLASH to SRAM, there is no XIP (execute in place) for flash memory like there is e.g. for ESP8266 or NRF52840 so everything executable must fit into SRAM.  However for Arduino C coding it should be good enough and the device is quite hackable. USB data pins have serial port too and 14585 documentation says the device could boot directly from serial port just like from SPI flash so it may be in a way unbrickable. I have atached SWD and dumped SRAM so there is plenty of information how to proceed. If you would like to continue with this let me know.

### HX-03 F/W
Also a bit more expensive is HX-03F (with color LCD) and HX03W both https://fccid.io/2AOYQ-HX03, these are [nRF52832 based](https://fccid.io/png.php?id=3779556&page=2) however SWD test points are unmarked (possibly the ones near top of lcd?)

### DS-D9 (a.k.a. Lenovo HW02)
HW is very similar to DS-D6 to the point that D9 firmware runs on D6 only with garbled display (clock digits are cut off). FCC info https://fccid.io/2AEMN-D9/ I have ordered one from Aliexpress for $11 (search for "mpow fitness"). This one has smaller OLED positioned hrozontally and is charged via cable so it should be thinner. There are still 4 pins including serial port. I hope the same Espruino binary for DS-D6 will run 'as is' on D9. **UPDATE 4.3.2019** I got it and it is indeed exactly the same except the display which is 64x32. All the pins seems to be wired in same way (motor, spi display, battery, serial) and flashing same DS-D6 espruino binary over serial worked just fine. So while DS-D9 is even harder to get (I got black one from [this seller](https://www.aliexpress.com/item/Mpow-Fitness-Activity-Tracker-IP67-Heart-Rate-Monitor-Smartband-Sleep-Monitor-Wristband-Call-Message-Reminder-Bracelet/32955082325.html) but it is already out of stock and price went up) and the OLED has poor visiblility and resolution, I still like its minimalistic design a bit more than DS-D6.
