[ID130 Color Plus HR](https://fccid.io/2AHFTID130PLUSCOLOR) is NRF52832 based fitness tracker made by  Shenzhen DO Intelligent Technology Co., Ltd.

There are many similar devices by same company and the firmware of all 52832 based ones are based on SDK11 so can be update without taking apart.
 
For initial demo code see code.js

### Installation ###

Bootloader can be triggered by writing 0x01,0x01 to 0x0AF6 characteristics e.g. via nRF connect android app (same as most other devices by same company) then reconnect and upload espruino zip file.

Bootloader is located at 0x79000, device ID is 616 so DFU package must be built with `--dev-type 616 --dev-revision 616`.
Bootloader starts watchdog (20s interval) so your FW must ping it or device reboots.

### Hardware ###

- ST7735 80x160 LCD (SPI)
- KX022 accelerometer (SPI), WHOAMI gives 0x14
- Si1142 heartrate sensor (I2C, 0x5a), gives partid 66 = Si1142, seqid 9 = Si114x-A11
- SPI flash (2MB?)

### Pinout ###

| Pin No.  | Description |
| ------------- | ------------- |
| 02 | LCD Backlight |
| 03 |analog battery voltage 4.20/0.207*analogRead(D4); |
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