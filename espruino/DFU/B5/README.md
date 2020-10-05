SMA B5 is ~$19 fitness tracker with builtin GPS. What is most interesting is that it has SWD debug port on USB data pins so it is unbrickable with no need to open it.


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
| 16 |? set as output, in some code, set to 1 (while vibrating) |	
| 17 |accel i2c sda 0x1f  KX123? WHO_AM_I gives 0x20 as per https://d10bqar0tuhard.cloudfront.net/en/document/TN004-Power-On-Procedure.pdf |
| 18 |accel i2c scl |
| 19 |hrs3313lp i2c sda(19+20) address 0x44, reading 6 bytes from reg a0,a6
| 20 |hrs3313lp i2c scl |
| 21 |unused? (reset) |
| 22 |? low even with input pull up (some irg pin?) |
| 23 |? follows pull, floating? |
| 24 |CHARGER input, pull up - 0=charging |
| 25 |? follows pull, floating? |
| 26 | ? set as input, pull down in code (value follows pull) |
| 27 | GPS TX (9600) |
| 28 | GPS RX |
| 29 | LCD Backlight (1=on) |
| 30 | MOTOR |
| 31 | 1= enable hrs3313lp i2c pins 19,20 |
