[SMA B5](https://www.smawatch.com/page411) is ([~$19](https://www.aliexpress.com/item/4000987225908.html)) fitness tracker with builtin GPS. What is most interesting is that it has SWD debug port on USB data pins so it is unbrickable with no need to open it.

Some initial demo code here https://gist.github.com/fanoush/505a6f44532e4fdaadef4da5777d7777

### Installation ###

The device is locked and firmware uses secure DFU with unknown signing key so the only way is to unlock it via SWD, for that you need debugger that can send direct commands to access custom debug access port ([CTRL-AP](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/dif.html?cp=4_2_0_15_1#concept_udr_mns_1s)) on nrf52 to trigger mass erase and unlock (=writing 1 to [ERASEALL](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/dif.html#register.ERASEALL) register). This cannot be done via generic $2 STlink V2 clone from ebay/aliexpress (unless you reflash it with [CMSIS-DAP](https://github.com/RadioOperator/STM32F103C8T6_CMSIS-DAP_SWO/tree/master/Doc/STLINK_V2A_V2B) or [BlackMagicProbe](https://github.com/blacksphere/blackmagic/tree/master/src/platforms/stlink) firmware). Perhaps easiest is to use Raspberry Pi, for more details see https://wiki.pine64.org/index.php/Reprogramming_the_PineTime#Unlocking_the_device

USB connector SWD wiring from one side to another is:

|black|green |white|red|
|-----|------|-----|---|
| GND |SWDCLK|SWDIO|5V |

After unlocking it can be flashed via openocd command `program <name of hex file>` and started via `reset run`. When running you should see B5 xxxx device on bluetooth and you should be able to connect to it via [Web IDE](https://www.espruino.com/ide/). Then copy demo code to right side of IDE, better enable pretokenzation in settings to reduce size and upload it to RAM. If there are no errors on upload touch the button and hopefully you will see something.

### Hardware ###

- ST7735 80x160 LCD
- GPS - one of
  - AT6558 (`MA=CASIC,IC=AT6558-5N-32-1C510800,SW=URANUS5,V5.1.0.0`), [datasheet](http://www.icofchina.com/d/file/xiazai/2016-12-05/b1be6f481cdf9d773b963ab30a2d11d8.pdf)
  - UBX-G7020 (`HW  UBX-G70xx   00070000, ROM CORE 1.00 (59842) Jun 27 2012 17:43:52,PROTVER 14.00`), datasheet [1](https://www.u-blox.com/sites/default/files/products/documents/UBX-G7020_ProductSummary_%28UBX-13003349%29.pdf),[2](http://innovictor.com/pdf/UBX-G7020-Kx_DataSheet_%28GPS%20G7-HW-12001%29_Confidential.pdf)
- KX022 accelerometer
- HRS3313 heartrate sensor
- SPI flash (2MB?)

### Pinout ###

| Pin No.  | Description |
| ------------- | ------------- |
| 02 | LCD CLK |
| 03 |LCD MOSI |
| 04 |analog battery voltage 4.20/0.320*analogRead(D4); |
| 05 |LCD CS |
| 06 |LCD CD |
| 07 |GPS enable (=1) |
| 08 |LCD RST |
| 09 |BUTTON (1=touch), needs [NFCPINS set as GPIO](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/uicr.html?cp=4_2_0_13_0_62#register.NFCPINS) |
| 10 |unused? (nfc pair with 9, affected by button too) |
| 11 |SPI FLASH MISO |
| 12 |SPI FLASH CS |
| 13 |SPI FLASH MOSI |
| 14 |SPI FLASH CLK |
| 15 |accel irq (?) |
| 16 |? set as output, in some code is set to 1 (while vibrating) |	
| 17 |accel i2c sda, address 0x1f, KX022 WHO_AM_I register gives 20=0x14 as per [this](https://kionixfs.azureedge.net/en/document/TN004-Power-On-Procedure.pdf) |
| 18 |accel i2c scl |
| 19 |hrs3313 i2c sda, address 0x44
| 20 |hrs3313 i2c scl |
| 21 |unused? (reset) |
| 22 |? low even with input pull up (some irg pin - HR?) |
| 23 |? follows pull, floating? |
| 24 |CHARGER input, pull up - 0=charging |
| 25 | GPS (TX? set as pullup with pin 26 in uart_230400_init, not set as TX!) |
| 26 | GPS RX (230400) - set as RX in uart_230400_init|
| 27 | GPS TX (9600) nmea |
| 28 | GPS RX (9600) nmea|
| 29 | LCD Backlight (1=on) |
| 30 | MOTOR |
| 31 | 1= enable hrs3313 i2c pins 19,20 |
