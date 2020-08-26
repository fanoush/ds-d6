### Espruino build for DK08 smartwatch

DK08 is nrf52832 watch with always on sunlight readable display (176x176, 64 colors - RGB222). Typical price on aliexpress is/was ~$29, then for some time it went down to $18-$14 ([here](https://www.aliexpress.com/item/4001256048750.html) or [here](https://www.aliexpress.com/item/4001224081207.html) - both stores are owned by same (Kospet?) company)

The hardware is designed by same Manridy manufacturer as F07 or F10 fitness trackers and all use IBand android app so upgrade guide is similar/same to [F07](https://github.com/fanoush/ds-d6/tree/master/espruino/DFU/F07).

Steps to update new DK08 watch to Espruino:

1. Optionally install IBand app and try firmware update. Hopefully this will download firmware file DFU zip into IBand folder on your storage card. This is useful for recovery to original firmware.
2. Install minimal espruino build e.g. via nrfConnect android app
3. backup and update bootloader via copy pasting prepared code and data into left side of Espruino Web IDE
4. clear old bootloader leftovers and minimal espruino, reboot to new bootloader and install full size Espruino from this folder (or possibly original firmware)
5. try example code https://gist.github.com/fanoush/f91dc52e76e8281a127cce86d8313ec9
