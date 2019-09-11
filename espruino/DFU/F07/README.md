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
