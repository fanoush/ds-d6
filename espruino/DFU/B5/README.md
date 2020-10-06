[SMA B5](https://www.smawatch.com/page411) is ([~$19](https://www.aliexpress.com/item/4000987225908.html) fitness tracker with builtin GPS. What is most interesting is that it has SWD debug port on USB data pins so it is unbrickable with no need to open it.

Some initial demo code here https://gist.github.com/fanoush/505a6f44532e4fdaadef4da5777d7777

### Hardware ###

- ST7789 80x160 OLED
- AT6558 GPS (MA=CASIC,IC=AT6558-5N-32-1C510800,SW=URANUS5,V5.1.0.0), [datasheet](http://www.icofchina.com/d/file/xiazai/2016-12-05/b1be6f481cdf9d773b963ab30a2d11d8.pdf)
- KX123 accelerometer (?)
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
| 09 |BUTTON (1=touch) |
| 10 |unused? (nfc pair with 9, affected by button too) |
| 11 |SPI FLASH MISO |
| 12 |SPI FLASH CS |
| 13 |SPI FLASH MOSI |
| 14 |SPI FLASH CLK |
| 15 |accel irq (?) |
| 16 |? set as output, in some code is set to 1 (while vibrating) |	
| 17 |accel i2c sda, address 0x1f  KX123? WHO_AM_I register gives 0x20 as per [this](https://d10bqar0tuhard.cloudfront.net/en/document/TN004-Power-On-Procedure.pdf) |
| 18 |accel i2c scl |
| 19 |hrs3313 i2c sda, address 0x44
| 20 |hrs3313 i2c scl |
| 21 |unused? (reset) |
| 22 |? low even with input pull up (some irg pin - HR?) |
| 23 |? follows pull, floating? |
| 24 |CHARGER input, pull up - 0=charging |
| 25 |? follows pull, floating? |
| 26 | ? set as input with pull down in code (value follows pull - floating?) |
| 27 | GPS TX (9600) |
| 28 | GPS RX |
| 29 | LCD Backlight (1=on) |
| 30 | MOTOR |
| 31 | 1= enable hrs3313 i2c pins 19,20 |
