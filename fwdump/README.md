## noanim bootloader version

There are two bootloader versions for DS-D6 found in the field.
One with moving arrows when doing the update and one with static image.
First it was not clear which one is newer/better but now it is clear the one with moving arrows is unstable,
so it is preferred to **get the one with no animation** to have stable DFU update procedure.
Looks like the animation is too heavy so sometimes the update breaks in the middle with timeout or cause some unexpected delays.
It is still possible to retry so you probably cannot brick your device with this booloader, it is just annoying.


## firmware dumps 

ds-d6 bin firmware was dumped via gdb over SWD as seen below (using bluepill board flashed with blackmagic probe firmware). 

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

For OpenOCD example see https://gist.github.com/fanoush/06eee6344a2e59f7b12707b25d87edda
