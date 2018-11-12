# DS-D6
Stuff for Desay/MPow DS-D6  nRF52832 bracelet 

Sold in various places like  ebay. I got it from GearBest, they are often on sale for $9.99 https://www.gearbest.com/smart-watches/pp_1232618.html?wid=1433363

DS-D6 FCC info https://fccid.io/2AEMN-D6/
Direct links to internal photos
- https://fccid.io/png.php?id=3414019&page=0 
- https://fccid.io/png.php?id=3414019&page=1 battery, HR sensor
- https://fccid.io/png.php?id=3414019&page=2 SWD test points (CLK,DIO), USB data pins marked a TX,RX maybe serial?
- https://fccid.io/png.php?id=3414019&page=3 CPU N53832

Also there is similar bracelet without HR sensor - Lenovo HX06 https://www.gearbest.com/smart-watches/pp_1830584.html?wid=1433363 , that is made by same manufacturer and shares app and the screen looks the same. Also the FCC info seems promising so I ordered that one too, still waiting.

Lenovo HX06 FCC info https://fccid.io/2AEMN-D16/ - CPU marking is unreadable but board looks very similar to DS-D6


Firmware in fwdump folder was dumped via gdb over SWD using bluepill board flashed with blackmagic probe firmware

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

see also some initial progress here
https://gitter.im/nRF51822-Arduino-Mbed-smart-watch/Lobby?at=5be3fbf36b9822140df92510

I am also putting more stuff to WIKI https://github.com/fanoush/ds-d6/wiki
