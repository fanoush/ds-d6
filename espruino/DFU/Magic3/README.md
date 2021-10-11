### Espruino for Kospet Magic3 smartwatch

Magic3 is 2nd generation DaFit watch based on NRF52840 chip  (256KB RAM, 1MB internal flash) with 240x280 LCD, full touch display and button.
For first generation (NRF52832) see [P8 or P22](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU/P8)

#### Steps to update new Magic3 watch to Espruino and install Nordic DFU bootloader:

Beware that there is no way back and **you may brick your watch** during this process!

1. Check watch firmware version, this should work for devices with firmware MOY-NBC5, also was verified with Kospet Rock with MOY-NAX3.
2. Put your watch on charger or make sure it is charged, if battery dies during the process you may have a brick.
3. Install `espruino_2v10.102_magic3-dafit.bin` via [DaFlasher](https://play.google.com/store/apps/details?id=com.atcnetz.paatc.patc&hl=en&gl=US) (as of October 2021 you need update to  latest version, v2 protocol was added only recently)
4. If you were lucky you should now see bluetooth device 'Magic3 xxxx' and can connect to it via [Espruino Web IDE](https://www.espruino.com/ide/).

At this point there is no way back but you already have full Espruino installed and can start experimenting with it (e.g. upload `code.js` as metioned below).
You can postpone next steps however without DFU bootloader it is not easy to upgrade it so when you are ready follow with steps below.

5. backup UICR and bootloader via copy pasting (CTRL+V) prepared code and data into left side of Espruino Web IDE. More details and explanations also here https://github.com/fanoush/ds-d6/wiki/Replacing-Nordic-DFU-bootloader but here is quick step by step guide:
    - backup whole UICR - just in case
      ```
      var f=require("Flash")
      for (a=0x10001000;a<0x10001400;a+=256) console.log(btoa(f.read(256,a)));
      ```
      then copy paste output lines (4 lines of mostly ///) to text file named `UICR.base64` and use base64 decode on that, e.g. in linux run `base64 -d UICR.base64 >UICR.bin`. There is also WebIDE plugin that can record all console output to file, that may be easier for larger blocks, enable via Setting->General->Terminal Log Icon.

    - backup existing bootloader - just in case
      ```
      var f=require("Flash")
      for (a=0xFC000;a<0xFE000;a+=256) console.log(btoa(f.read(256,a)));
      ```
      then copy output lines to text file named `bootloader.base64` and use base64 decode on that, e.g. in linux run `base64 -d bootloader.base64 >bootloader.bin`
5. install new bootloader, from this point **it is dangerous to reboot or crash/reset the watch or let the battery die** without finishing all steps
    - flash new bootloader (and overwrite old) by copy paste from `Magic3-bootloader.txt` - first paste flashing code , then paste base64 encoded bootloader binary
    - verify bootloader (run `f=verify` and paste bootloader again) - you should see only V-OK lines for all addresses.
    - set correct bootloader start and bootloader settings address - will enable new bootloader, copy paste whole block

      ```
      NRF.onRestart=function(){
      poke32(0x4001e504,1);while(!peek32(0x4001e400)); // enable flash writing
      poke32(0x1000-8,0xF8000);while(!peek32(0x4001e400)); // set bootloader address 
      poke32(0x1000-4,0xFE000);while(!peek32(0x4001e400)); // set mbr settings
      poke32(0x10001014,0xF8000);while(!peek32(0x4001e400)); // set bootloader address 
      poke32(0x10001018,0xFE000);while(!peek32(0x4001e400)); // set mbr settings
      poke32(0x4001e504, 0);while(!peek32(0x4001e400)); // disable flash writing
      }
      NRF.restart();
      ```
      As mentioned in the output to run the code you must temporarily disconnect from the device to allow bluetooth and SoftDevice restart.
      After reconnecting check via `peek32(0x10001014).toString(16);` and `peek32(0x1000-8).toString(16);` that code was run and both values are really `F8000`.
      Do not reset/reboot the watch or let battery die if you see all FFs or F**C**000. retry step 6 until you see both as F8000.
      If watch reboots with new bootloader flashed but bootloader start still pointing to FC000 (=middle of new bootloader) you just bricked your device.
      It may happen that due to radio noise WebIDE may disconnect, in such case just reconnect and continue or redo previous step.

    - erase last two flash pages to clear data for new bootloader (MBR and bootloader settings pages)
      ```
      E.setFlags({unsafeFlash:1});
      var f=require("Flash");
      f.erasePage(0xfe000);
      f.erasePage(0xff000);
      ```

    - now the botloader is installed, to test it and reboot to newly flashed bootloader run `poke32(0x4000051c,1)` or hold the button, run `E.reboot()` and quickly release the button (less than 3 seconds).
      If this worked you should see DfuTarg device that waits for 90 seconds for connecting an uploading DFU zip package
    
6. install newer version of  Espruino from this folder or use different package to downgrade/upgrade softdevice and install other custom software. Firmware with **SPIFLASH** in name has file storage in external 8MB flash. The one without SPIFLASH has storage in internal nRF52840 1MB flash (600KB free), external flash is still accessible via Flash module API but is unused, this is useful for doing initial SPI flash backup or if 600KB is enough for you.
7. try example `code.js` from this folder (copy to right side of WebIDE and upload to RAM, enable minification and pretokenization to reduce size)

### Hardware ###

- LCD  240x280 16bit color display
- HR sensor?,  I2C 0x44
- accelerometer sc7a20, I2C 0x18
- touchscreen CST816, I2C 0x15, reports coordinates before you lift finger
- 8 MB SPI flash 

### Pinout ###
| Pin No.  | Description |
| ------------- | ------------- |
| 02 | LCD RST  |
| 03 | LCD CS  |
| |  |
| 06 | motor 0=on, works when 07 is 1 |
| 07 | 1 = turns red led off and motor works |
| 08 | charger, 0=attached  |
| |  |
| 12 | backlight |
| |  |
| 14 | I2C SCL |
| 15 | I2C SDA - devices on bus 0x15 (touch) ,0x18 (accel) ,0x44 (hr sensor?) |
| |  |
| 17 | SPI Flash CS |
| 18 | unused - 52840 reset pin |
| 19 | SPI Flash SCK |
| 20 | MOSI/IO0 |
| 21 | MISO/IO1 |
| 22 | WP/IO2 |
| 23 | RS/HOLD/IO3 |
| |  |
| 26 | button, 0=pressed (inverted in Espruino so that BTN1 pressed gives true) |
| |  |
| 30 | battery voltage, 4.20/0.60 * analogRead(D30) |
| |  |
| 32 | touch IRQ |
| |  |
| 44 | LCD MOSI |
| 45 | LCD SCK |
| 46 | button 2 on Kospet Rock MOY-NAX3 , needs pull down , 1 when pressed|
| 47 | LCD D/C |
