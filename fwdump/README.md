## noanim bootloader version

There are two bootloader versions for DS-D6 found in the field.
One with moving arrows when doing the update and one with static image.
First it was not clear which one is newer/better but now it is clear the one with moving arrows is unstable,
so it is preferred to **get the one with no animation** to have stable DFU update procedure.
Looks like the animation is too heavy so sometimes the update breaks in the middle with timeout or cause some unexpected delays.
It is still possible to retry so you probably cannot brick your device with this booloader, it is just annoying.


## desay_dfu.py flasher

This is python bluetooth DFU flasher for linux. It works by scripting [`gatttool`](https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/attrib) command from [bluez](http://www.bluez.org/) so no python bluetooth library is used. It needs [pexpect package](https://pexpect.readthedocs.io/en/stable/index.html) to be installed via pip.

Original project https://github.com/dingari/ota-dfu-python

I have added support for Desay bootloader, some recovery retry code, ability to flash also bootloader and softdevice combinations and ability to switch to bootloader from stock DS-D6 app, espruino and micropython.

### usage
```
sudo ./desay_dfu.py -a D2:72:54:EA:16:1E -z DS-D6-desay-bootloader-noanim-fix-with-sd132v201.zip 
```



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
