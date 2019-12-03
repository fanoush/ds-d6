F07 tracker uses SDK11 based Nordic dual bank bootloader so only half of flash is available for application.

#### Memory layout

```
0x00000-0x1bfff SoftDevice S132 2.x  
0x1c000-0x4afff first bank (size 0x2f000)  
0x4b000-0x79fff second bank (size 0x2f000)  
0x7a000-0x7bfff bootloader  
0x7e000 MBR parameters  
0x7f000 bootloader settigns
```

You can use this also for any generic device to get things started - determine HW pinout, bootloader location etc.
To get bootloader start address run this to read it from UICR
```
peek32(0x10001014).toString(16)
```
Bootloader backup can be then done like this:
```
var f=require("Flash")
for (a=peek32(0x10001014);a<0x7e000;a+=256) console.log(btoa(f.read(256,a)));
```
then copy paste those lines to text file and use base64 decode on that, e.g. in linux run
```
base64 -d file.base64 >file.bin
```
Once you have bootloader it can be patched to allow upgrade to higher versions.
