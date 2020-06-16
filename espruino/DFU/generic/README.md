These are generic SDK11 builds of espruino with UART console over bluetooth and no pins or buttons defined.
The minimal build is useful for dual banked bootloader which keeps two copies of your application so it can be only half of size.
So first try to flash full sized one and if it fails try the minimal one.

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

#### Updating bootloader or clearing/fixing UICR
See WIKI [here](https://github.com/fanoush/ds-d6/wiki/Replacing-Nordic-DFU-bootloader)


#### Entering DFU by clearing Espruino

The easiest way to get out of Espruino environment is to make application invalid by erasing bootloader settings page and reboot, see below. After reboot this should stay in bootloader and wait for flashing valid DFU package (new Espruino or stock firmware).

```
E.setFlags({unsafeFlash:1})
var f=require("Flash")
f.erasePage(0x7f000)
E.reboot()
```
