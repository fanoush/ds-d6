### Espruino build for DK08 smartwatch

DK08 is nrf52832 watch with always on sunlight readable display (176x176, 64 colors - RGB222). Typical price on aliexpress is/was ~$29, then for some time it went down to $18-$14 ([here](https://www.aliexpress.com/item/4001256048750.html) or [here](https://www.aliexpress.com/item/4001224081207.html) - both stores are owned by same (Kospet?) company)

The hardware is designed by same Manridy manufacturer as F07 or F10 fitness trackers and all use IBand android app so upgrade guide is similar/same to [F07](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU/F07).

Steps to update new DK08 watch to Espruino:

1. Optionally install IBand app and try firmware update. Hopefully this will download firmware file DFU zip into IBand folder on your storage card. This is useful for recovery to original firmware.
2. Install minimal espruino build zip from [F07 folder](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU/F07) e.g. via nrfConnect android app
3. backup and update bootloader via copy pasting prepared code and data into left side of Espruino Web IDE. More details and explanations also here https://github.com/fanoush/ds-d6/wiki/Replacing-Nordic-DFU-bootloader but here is quick step by step guide:
    - backup whole UICR - just in case
      ```
      var f=require("Flash")
      for (a=0x10001000;a<0x10001400;a+=256) console.log(btoa(f.read(256,a)));
      ```
      then copy paste output lines (4 lines of mostly ///) to text file named `UICR.base64` and use base64 decode on that, e.g. in linux run `base64 -d UICR.base64 >UICR.bin`
    - erase whole UICR - to disable old bootloader to be safe for next step
      ```
      NRF.onRestart=function(){
      poke32(0x4001e504,2);while(!peek32(0x4001e400)); // enable flash erase
      poke32(0x4001e514,1);while(!peek32(0x4001e400)); // erase whole uicr
      poke32(0x4001e504,0);while(!peek32(0x4001e400)); // disable flash writing
      }
      NRF.restart(); // will schedule SoftDevice restart after you disconnect
      ```
      To run the code you must temporarily disconnect from the device to allow bluetooth and SoftDevice restart. After reconnecting you may try to check via `peek32(0x10001014).toString(16);` that the UICR is cleared to all FFs.
    
    - upload new bootloader from DK08-bootloader.txt - first paste flashing code, then base64 encoded bootloader binary
    - verify bootloader (run `f=verify` and paste bootloader again)
    - erase last flash page to clear data stored by old bootloader
      ```
      E.setFlags({unsafeFlash:1});
      var f=require("Flash");
      f.erasePage(0x7f000);
      ```
    - set UICR bootloader start and bootloader settings address - will enable new bootloader, again this needs disconnect and reconnect
      ```
      NRF.onRestart=function(){
      poke32(0x4001e504,1);while(!peek32(0x4001e400)); // enable flash writing
      poke32(0x10001014,0x7A000);while(!peek32(0x4001e400)); // set bootloader address 
      poke32(0x10001018,0x7E000);while(!peek32(0x4001e400)); // set mbr settings
      poke32(0x4001e504, 0);while(!peek32(0x4001e400)); // disable flash writing
      }
      NRF.restart();
      ```
    - reboot to newly flashed bootloder, it will stay in DFU mode, check for `DfuTarg` device
      ```
      E.reboot();
      ```
    
4. install full size Espruino from this folder (or possibly original firmware)
5. try example code https://gist.github.com/fanoush/f91dc52e76e8281a127cce86d8313ec9

### Hardware ###

- LCD  always on 176x176 64 colors (RGB222) ST7301
- HR sensor EM7028 (detasheet linked [here](https://lcsc.com/product-detail/Specialized-Sensors_Epticore-Microelectronics-Shanghai-EM7028_C91478.html))
- accelerometer Bosch BMA253 (?)
- 2MB SPI flash / fontchip [GT24L24A2Y](https://github.com/RichardBsolut/GT24L24A2Y)

### Pinout ###
| Pin No.  | Description |
| ------------- | ------------- |
| 02 |accel CS |
| 03 |accel int 2? |
| 04 |accel int 1?|
| 05 | battery analog |
| 06 |MOTOR |
| 07 |accel power |
| 08 |BUTTON |
| 09 |unused? |
| 10 |unused? (nfc pair with 9) |
| 11 | LCD PWR |
| 12 | ? |
| 13 |LCD backlight |
| 14 |HR power |
| 15 |LCD RST |
| 16 |LCD MOSI|	
| 17 |LCD CLK|
| 18 |LCD CS |
| 19 |LCD D/C|
| 20 |HR SCL - EM7028, address 0x24 |
| 21 |unused? (reset) |
| 22 |HR SDA - EM7028, address 0x24 |
| 23 |battery something, changes after charged fully, then disconnected, then reattached - full battery signal? |
| 24 |CHARGER connected |
| 25 |? |
| 26 | ? |
| 27 | SPI Flash CS |
| 28 | ? |
| 29 | Flash/accel SPI CLK |
| 30 | Flash/accel SPI MOSI |
| 31 | Flash/accel SPI MISO |
