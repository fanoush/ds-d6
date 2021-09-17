[ID130 Color Plus HR](https://fccid.io/2AHFTID130PLUSCOLOR) is NRF52832 based fitness tracker made by  Shenzhen DO Intelligent Technology Co., Ltd.
It is quite old now (2017) so may be hard to get. I got few of them in 2021 in some sale for ~6EUR each. Sometimes it can be found on aliexpress/ebay, e.g. [here](https://www.aliexpress.com/item/32907244187.html)

There are many similar devices by same company and the firmware of all 52832 based ones are based on SDK11 so can be updated without taking apart. Most of them are even based on same hardware. Later I got [ID133 Color HR](https://fccid.io/2AHFT646) (rebranded as Yamay SW350) which looks different from outside however the hardware and pinout is same as ID130 with id 645 mentioned below.
 
### Installation ###

Bootloader can be triggered by writing 0x01,0x01 to 0x0AF6 characteristics e.g. via nRF connect Android app (same procedure as with most other devices by same IDOO company - ID107, ID115, ...) then reconnect and upload espruino zip via DFU button.


Unfortunately there are several variants of this 'ID130 Plus Color HR' device that looks identical from the outside but differs by internal wiring of the pins or maybe also some components(?). Device ID for the device I received initially is 616.  DFU package for each variant must be built with its specific ID, for `adafruit-nrfutil` the relevant parameters look like `--dev-type 616 --dev-revision 616`. Bootloader will not accept package for other device variant.

So far  I know there are at least 5 device ids for ID130 Color - 598,603,616,645,646. Currently I got variants 598,616 and 645.

It is important to discover ID of your variant in advance before attempting to install custom firmware. For that install VeryFit Pro Android application and then use some file manager app on the phone (e.g. Ghost Commander) and navigate to `/storage/emulated/0/Android/data/com.veryfit2hr.second/files/VeryfitPro/log/device_update` folder and examine log files there for 'firmware id'. If you are lucky you may even find download link to firmware update for your version if you have older version then latest or attempted the upgrade earlier. If you are not lucky there are known download links for IDs 603,616,645,646.

Bootloader is located at 0x79000 - similar to other IDxx devices and unlike iBand devices (0x7a000) or Desay or DaFit devices (0x78000), this means softdevice/bootloader upgrade packages for those are not usable here.
Please note that bootloader starts watchdog (with 20s interval) so your FW must ping it or device reboots, Espruino build is patched to enable automatic watchdog pinging at boot time.

For initial demo code see code.js

### Hardware ###

- ST7735 80x160 LCD (SPI)
- KX022 accelerometer (SPI), WHOAMI register gives 0x14
- Si1142 heartrate sensor (I2C, 0x5a), gives partid 66 = Si1142, seqid 9 = Si114x-A11
- SPI flash (2MB?)
- single touch button
- charging red LED (hardwired to power)

### Pinout for ID130Plus with device id 616 ###

| Pin No.  | Description |
| ------------- | ------------- |
| 02 | LCD Backlight |
| 03 |analog battery voltage 4.20/0.207*analogRead(D3); |
| 04 | KX022 CS |
| 05 |LCD Power |
| 06 | touch button enable when set low |
| 07 |touch button, goes low when touched (and pin 6 is low!) |
| 08 |KX022 IRQ1 |
| 09 |charger detect |
| 10 |unused? (nfc pair with 9, affected by charger too) |
| 11 |LCD RST|
| 12 |LCD CS |
| 13 |HR IRQ (?) |
| 14 |HR SCL |
| 15 |HR SDA |
| 16 |LCD D/C |	
| 17 |motor |
| 18 |?? |
| 19 |LCD SCK|
| 20 |LCD MOSI |
| 21 |unused? (reset) |
| 22 |UART debug log 115200 |
| 23 |HR POWER |
| 24 |?? |
| 25 |FLASH MOSI|
| 26 |FLASH SCK|
| 27 |FLASH MISO |
| 28 |FLASH CS|
| 29 |KX022 MOSI |
| 30 |KX022 MISO |
| 31 |KX022 SCK |

### Pinout for ID130Plus with device id 645 (also ID133 Color with id 630)###

| Pin No.  | Description |
| ------------- | ------------- |
| 02 | KX022 MOSI|
| 03 |analog battery? |
| 04 | KX022 MISO|
| 05 | LCD BACKLIGHT|
| 06 | KX022 CS|
| 07 | KX022 SCK|
| 08 | KX022 IRQ?|
| 09 | charger|
| 10 |unused? (nfc pair with 9, affected by charger too) |
| 11 |LCD CS|
| 12 |LCD RST |
| 13 |HR SDA|
| 14 |HR SCL|
| 15 |HR IRQ?|
| 16 | |	
| 17 |motor|
| 18 ||
| 19 |BUTTON|
| 20 ||
| 21 |unused? (reset) |
| 22 | |
| 23 | LCD POWER|
| 24 | |
| 25 |FLASH MOSI|
| 26 |FLASH SCK|
| 27 |FLASH CS|
| 28 |FLASH MISO|
| 29 |LCD MOSI |
| 30 |LCD SCK|
| 31 |LCD D/C|
