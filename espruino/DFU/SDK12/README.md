Beware that to use this you **first need to flash [fixed bootloader](https://github.com/fanoush/ds-d6/tree/master/fwdump)** that can upgrade to >=3.0 versions of SoftDevice.
Stock Desay bootloader with no fix will corrupt SoftDevice area and brick your device!

This is build of vanilla SDK12 based Espruino including its bootloader for best compatibility.
You get a bit more features thanks to SDK12 and SoftDevice S132 v3.x (like e.g secure connections).
You also get slightly less available RAM and flash memory.

The bootloader is derived from standard Nordic secure one. To get back to DFU mode from Espruino you can hold touch button while executing `E.reboot()` . However if you hold if over 3 seconds it will reboot back to espruino and do not run any startup code. Or you can use same `poke32(0x40000000+0x51c,1)` command as with Desay SDK11 bootloader.


### How to build

Copy DSD6_SDK12.py board file to boards/ folder and run
```
make -j BOARDNAME=DSD6 BOARD=DSD6_SDK12 RELEASE=1 NRF_SDK12=1 VERBOSE=1 USE_BOOTLOADER=1 DFU_UPDATE_BUILD=1
```

