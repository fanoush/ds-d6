F07 tracker uses SDK11 based Nordic dual bank bootloader so by default only half of flash is available for application. 

#### Memory layout

```
0x00000-0x1bfff SoftDevice S132 2.x  
0x1c000-0x4afff first bank (size 0x2f000)  
0x4b000-0x79fff second bank (size 0x2f000)  
0x7a000-0x7bfff bootloader  
0x7e000 MBR parameters  (missing in UICR at 0x10001018 location !!!)
0x7f000 bootloader settings
```

To use more space for larger application (like full build of Espruino) the bootloader needs to be changed to single bank variant. Unfortunately bootloader cannot be updated directly via DFU because the MBR settings address in UICR area is not set so by updating bootlader or softdevice the device will be bricked! This is probably common for all iBAND devices as I managed to brick DK08 watch by trying to update bootloader before knowing this. So the way to update bootloader is to first use stripped down minimal Espruino build that fits into single bank and use it to set UICR properly to allow DFU or even also rewrite the bootloader. So the steps are as follows:

- Upload minimal stripped down build of Epruino via standard Nordic DFU (via nrfConnect or DaFlasher)
- Backup existing bootloader and UICR (just in case)
- Fix UICR at 0x10001018 to point to 0x7e000 so that bootloader or softdevice DFU update works
- Upload new single bank bootloader via DFU or directly from minimal Espruino
- Upload full size SDK11 based Espruino

#### Backing up bootloader and UICR

You can copy paste code below via CTRL+V into espruino console - left side of [WebIDE](https://www.espruino.com/ide/). 

Bootloader location can be checked via 
```
peek32(0x10001014).toString(16)
```
Bootloader backup can be then done like this:
```
var f=require("Flash");
for (a=peek32(0x10001014);a<0x7e000;a+=256) console.log(btoa(f.read(256,a)));
```
then copy paste those lines to text file and use base64 decode on that, e.g. in linux run
```
base64 -d file.base64 >file.bin
```

Same procedure can be used for [UICR](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/uicr.html?cp=4_2_0_13#concept_rnp_grp_xr)

```
var f=require("Flash")
for (a=0x10001000;a<0x10001400;a+=256) console.log(btoa(f.read(256,a)));
```

#### Fixing UICR

This is a bit tricky because normally UICR cannot be erased or written while SoftDevice is enabled and bluetooth connection is working. However I have patched Espruino to run short piece of javascript while SoftDevice is temporarily disabled so it can be done like this:
1. set code that will be run while softdevice and bluetooth is stopped
```
NRF.onRestart=function(){
poke32(0x4001e504,1);while(!peek32(0x4001e400));
poke32(0x10001018,0x7E000);while(!peek32(0x4001e400));
poke32(0x4001e504,0);while(!peek32(0x4001e400));
}
```
2. schedule restart Softdevice and disconnect from device so it is executed
```
NRF.restart()
BLE Connected, queueing BLE restart for later
=undefined
>
```

3. connect again and verify that UICR was indeed updated to 0x7e000

```
>peek32(0x10001018).toString(16)
="7e000"
```

Beware that flash memory can be only written few times between erasing and it is only possible to change ones to zeroes so the procedure above works only if initial value of `0x10001018` was `"ffffffff"`. It is also possible to clear UICR area completely and reset both values again but this should not be needed. However it can be done like this:
```
NRF.onRestart=function(){
poke32(0x4001e504,2);while(!peek32(0x4001e400)); // enable flash erase
poke32(0x4001e514,1);while(!peek32(0x4001e400)); // erase whole uicr
poke32(0x4001e504,1);while(!peek32(0x4001e400)); // enable flash writing
poke32(0x10001014,0x7A000);while(!peek32(0x4001e400)); // set bootloader
poke32(0x10001018,0x7E000);while(!peek32(0x4001e400)); // set mbr settings
//poke32(0x10001200,21);while(!peek32(0x4001e400)); // enable reset pin 21
//poke32(0x10001204,21);while(!peek32(0x4001e400)); // confirm reset pin
//poke32(0x1000120c,0);while(!peek32(0x4001e400)); // NFC pins as GPIO
poke32(0x4001e504, 0);while(!peek32(0x4001e400)); // disable flash writing
}
```
Enabling reset pin or NFC pins as GPIO is not needed in this case.

#### Updating bootloader
TODO

#### Entering DFU by clearing Espruino

If you did not update bootloader to allow enntering it via `poke32(0x4000051c,1)` then easiest way to get out of  Espruino environment is to make it invalid by erasing bootloader settings page and reboot, see below. After reboot this should stay in bootloader and wait for flashing valid DFU package (new Espruino or stock firmware).

```
E.setFlags({unsafeFlash:1})
var f=require("Flash")
f.erasePage(0x7f000)
E.reboot()
```
