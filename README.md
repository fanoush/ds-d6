# DS-D6
Custom Espruino/Arduino/Micropython firmware for Desay/MPow DS-D6 nRF52832 bracelet

Also works on [Mpow DS-D9/Lenovo HW02](https://github.com/fanoush/ds-d6/wiki/DS-D9), [Lenovo HX03W](https://github.com/fanoush/ds-d6#hx03-hx03w-hx03f-aka-ds-d1010w10f) and also on couple of generic fitness trackers with color screen available on ebay/aliexpress like F07, F07Plus, F10, see below.

## Where to get the device

I got it from GearBest however it now appears to be out of stock on their website (however currently their mobile app lists it as available). Sometimes it can be also found on ebay but the prices vary and can be relatively high so it may make sense to get some other device mentioned below (e.g. F07/F10, or HX03W if you need gpio on usb data pins). If you would still desperately need DS-D6 and cannot get it elsewhere then PM me on gitter or ask in the Lobby. I guess I could part with few from my private stock and maybe others could too.

## HW reference
DS-D6 FCC info https://fccid.io/2AEMN-D6/

Direct links to internal photos
- https://fccid.io/png.php?id=3414019&page=0 
- https://fccid.io/png.php?id=3414019&page=1 battery, HR sensor
- https://fccid.io/png.php?id=3414019&page=2 SWD test points (CLK,DIO), USB data pins marked as TX,RX (serial UART)
- https://fccid.io/png.php?id=3414019&page=3 CPU N52832

## Status

- all/most hardware [known and documented](https://github.com/fanoush/ds-d6/wiki/Hardware) (HR sensor somehow works but I don't use it)
- it is possible to [update and restore device via bluetooth or TTL serial](https://github.com/fanoush/ds-d6/wiki/DFU-update) without opening it as long as your app is developed with Nordic SDK11 and SoftDevice 2.0.x
- recent build of Espruino works with all hardware with no issues, flashable DFU package [here](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU)
- it is also possible to update device to newer version of SDK, bootloader and SoftDevice without opening it (and also restore it back) so porting SW that requires higher SDK and SoftDevice versions is now possible too (e.g. micropython). This involves flashing patched original bootloader first as there was [bootloader bug](https://devzone.nordicsemi.com/f/nordic-q-a/16774/updating-from-s132-v2-0-x-to-s132-v3-0-0-with-dual-bank-bootloader-from-sdk-v11-0-0-does-not-work) preventing the upgrade to newer SoftDevices.
- [build](https://github.com/fanoush/ds-d6/tree/master/micropython) of [Adafruit bootloader](https://github.com/adafruit/Adafruit_nRF52_Bootloader) available with latest version of S132 softdevice so both latest Micropython and [Adafruit Arduino Core](https://github.com/adafruit/Adafruit_nRF52_Arduino) for nrf52 is easy to use. See micropython folder.


All stuff documented in WIKI **https://github.com/fanoush/ds-d6/wiki**

For contact use either github issues here or join **https://gitter.im/nRF51822-Arduino-Mbed-smart-watch/Lobby** or [Espruino forum](http://forum.espruino.com/conversations/280747/).

## Other  devices made by Desay

### ~~HX-06~~

There is similar bracelet without HR sensor - Lenovo HX06 https://www.gearbest.com/smart-watches/pp_1830584.html?wid=1433363 (lowest so far for $11.99). It is made by same manufacturer and shares app and the watch UI look&feel is the same. Also the FCC info seems promising https://fccid.io/2AEMN-D16/ - CPU marking is unreadable but board looks very similar to DS-D6 and there are SWD test points (= ARM Cortex M architecture) so I ordered that one too. **UPDATE 7.12.2018 sadly after receiving it I found HX06 is not Nordic based but has Dialog [DA14585/6](https://www.dialog-semiconductor.com/products/connectivity/bluetooth-low-energy/smartbond-da14585-and-da14586) chip** There is SDK available from Dialog however the chip architecture is not suitable for large codebase like Espruino.  There is 96KB of SRAM for both data and code, code is mirrored at poweron from SPI FLASH to SRAM, there is no XIP (execute in place) for flash memory like there is e.g. for ESP8266 or NRF52840 so everything (code,data,bss) must fit into that 96KB SRAM.  However for Arduino C coding it should be good enough and the device is quite hackable. USB data pins have serial port too and DA14585 documentation says the device could boot directly from serial port just like from SPI flash so it may be in a way unbrickable. I have atached SWD debugger and dumped SRAM so there is plenty of information how to proceed. If you would like to continue with this let me know. The OTP memory is empty so it runs in developer mode with nothing locked.

### HX03, HX03W, HX03F (a.k.a. DS-D10,10W,10F)
These are three similar nRF52832 based models with same [HX03 FCC ID](https://fccid.io/2AOYQ-HX03) duplicated also as [DS10](https://fccid.io/2AEMN-D10). HX03W and F are available e.g. on Gearbest ($21, $17) or Banggood (had flash sale of HX03W for $9.99). Bangood has also the third HX03 device (with no W or F). This looks almost like HX03W but has only 128x32 LCD like DS-D6 so it is the worst of those three, so make sure you are not getting this one by mistake.

I have ordered couple of HX03W ones. Will update once I receive it. According to Desay DS-10(W/F) firmware DFU zips these are also SDK11 based so everything should be very similar to DS-D6. **UPDATE 31.05.2019** I got it and almost all stuff is same (button, motor, serial on USB data pins, charging voltage, KX023) as DS-D6 except display and HR sensor being [HRS3300](http://www.tianyihexin.com/pic/file/20170627/20170627154877337733.pdf). However same DS-D6 Espruino build runs just fine. Also DS-D10W unbranded firmware runs on this HW (but have less functionality than Lenovo branded one).

### DS-D9 (a.k.a. Lenovo HW02)
HW is very similar to DS-D6 to the point that D9 firmware runs on D6 only with garbled display (clock digits are cut off). FCC info https://fccid.io/2AEMN-D9/ I have ordered one from Aliexpress for $11 (search for "mpow fitness"). This one has smaller OLED positioned horizontally and is charged via cable so it should be thinner. There are still 4 pins including serial port. I hope the same Espruino binary for DS-D6 will run 'as is' on D9. **UPDATE 4.3.2019** I got it and it is indeed exactly the same except the display which is 72x40. All the pins seems to be wired in same way (motor, spi display, battery, serial) and flashing same DS-D6 espruino binary over serial worked just fine. So while DS-D9 is even harder to get and the OLED has poor visiblility and resolution, I still like its minimalistic design a bit more than DS-D6. See also [wiki page](https://github.com/fanoush/ds-d6/wiki/DS-D9).

### Lenovo [HW01](https://fccid.io/2AEMN-HW01) ([Desay B521](https://fccid.io/2AEMN-B521))
This one is very similar to DS-D6. I managed to get firmware file for HW01, flashed it to DS-D6 and it works except display being unreadable. This means it is same architecture as others and should be usable too. If you have one and want to experiment with custom firmware, let me know.

### Other nrf52832 Desay models

Devices mentioned above, while still being sold, are no longer manufactured by [Desay](https://www.globalsources.com/si/AS/Desay-Infor/6008849906089/Homepage.htm) OEM manufacturer, however there are more current models they offer. They are suppored by MPOW android app and we have links to beta firmware downloads. They still look like newer iterations of same SW and HW design. Names are [DS-D15F](https://www.globalsources.com/si/AS/Desay-Infor/6008849906089/pdtl/smart-bracelet/1167004882.htm), [DS-D20F](https://www.globalsources.com/si/AS/Desay-Infor/6008849906089/pdtl/activity-tracker/1167004827.htm) (also [FCC ID](https://fccid.io/2AEMN-D20)), [DS-Z10F](https://www.globalsources.com/si/AS/Desay-Infor/6008849906089/pdtl/Smart-bracelet/1167004825.htm) So far I didn't find them available for sale via some brand like Lenovo or MPow. **EDIT:** Lenovo HX11 ([Gearbest](https://www.gearbest.com/smart-wristband/pp_009500201679.html?wid=1349303)) seems to be DS-D20F, however the price is a bit high (for no real reason IMO).

### Other nrf52832 devices

There are also many other devices by other manufacturers. Most are using newer Nordic SDKs than SDK11 -> have signed firmware -> cannot be updated without taking each one apart. Also most have no GPIOs on usb data pins like devices made by Desay. Ideal device is using nrf52832, firmware is compiled with SDK11 (=is unsigned) and there is firmware update available so one can reflash it back to restore original functionality. As a bonus GPIOs on USB data pins are nice as is color display and low price since at least two devices are good to have.  Below is some list of known devices suitable for hacking. 

- F07,F07plus - [FCC info](https://fccid.io/2AONX-F07) ,~$14-$17 on aliexpress, also on Gearbest [here](https://www.gearbest.com/smart-watches/pp_1231729.html?wid=1433363) and [here](https://www.gearbest.com/smart-watches/pp_009307252051.html), beware that there is also cheaper similar variant on aliexpress with different pictures on screen sometimes named F07MAX, this one may not be nrf52 so make sure the pictures on screen looks same and listing says it uses iband app and has nrf52832. I got it and I am working on bootloader fixes and Espruino port. Stock bootloader is unsigned but dual banked so only half of flash is available so Espruino doesn't fit. I am working on suitable single bank bootloader replacement.

- F10 - this is slimmer and sligtly more expensive (~$16-$19) version of F07, Aliexpress examples [here](https://www.aliexpress.com/item/32864537037.html) or [here](https://www.aliexpress.com/item/32867894249.html), again make sure pictures on screen looks exactly the same as F07

- some other untested devices supported by [iband app](https://play.google.com/store/apps/details?id=com.manridy.iband&hl=en), details [here](http://forum.espruino.com/comments/14746917/)

- ID1xx devices made by [Shenzhen DO Intelligent Technology Co., Ltd](https://fccid.io/2AHFT) details [here](http://forum.espruino.com/comments/14731598/)

- [iWOWNfit Fitness Tracker I6HRC](https://fccid.io/2AKPH-I6HRC/) this is great and now relatively cheap device (~$17 on aliexpress like F07) sadly **the firmware is signed so each device must be taken apart** however the procedure is relatively easy and reversible without damage, see video [here](https://www.youtube.com/watch?v=0Fu-VSuKHEg) so it may be worth it if you like the dual touch areas that allow interaction by swiping (I got one too)
