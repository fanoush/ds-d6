# HX03W

Lenovo HX03W is made by same Desay company as DS-D6 and internal pinout is identical to DS-D6.

Curerntly the only difference between Espruino build for DS-D6 and HX03W is board name
(shown in `process.env.BOARD` and advertised on bluetooth). That's why I am rarely updating this. You can use DS-D6 build or let me know and I can make fresh build for HX03W.

As for hardware the difference from DS-D6 is that HR sensor is HRS3300 and charger voltage is digital, not analog (battery voltage is still analog).
Also display is 128x64 with slightly different command set from standard SSD1306, notably using the page mode is needed, direct/linear mode does not work.
Demo code is here https://gist.github.com/fanoush/56db50bd2392abedc15039bc6e7e5f06
