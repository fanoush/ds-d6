#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>

import pinutils;

info = {
 'name' : "G5",
 'link' :  [ "" ],
 'espruino_page_link' : 'G5',
 'default_console' : "EV_BLUETOOTH",
 'variables' : 14000-300, # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_g5.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
#     'NET',
     'GRAPHICS',
#     'NFC',
#     'NEOPIXEL'
     'JIT',
   ],
   'makefile' : [
#    'DEFINES += -DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'DEFINES += -DCONFIG_NFCT_PINS_AS_GPIOS', # NFC pins 9,10 as gpio
#     'CFLAGS += -D__STARTUP_CLEAR_BSS -D__START=main',
#     'LDFLAGS += -D__STARTUP_CLEAR_BSS -D__START=main -nostartfiles',
     'DEFINES += -DNRF_SDH_BLE_GATT_MAX_MTU_SIZE=131', #59 77 131 104
     'DEFINES+=-DUSE_FONT_6X8 -DGRAPHICS_PALETTED_IMAGES -DGRAPHICS_ANTIALIAS',
     'DEFINES += -DBLUETOOTH_NAME_PREFIX=\'"G5"\'',
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0xa9,0xae,0xb6', #S140 6.0.0
     'BOOTLOADER_SETTINGS_FAMILY=NRF52840',
     'DEFINES += -DNRF_BL_DFU_INSECURE=1 -DNRF_BOOTLOADER_NO_WRITE_PROTECT=1',
     'USE_LCD_SPI_UNBUF=1',
     'DEFINES+= -DSPISENDMANY_BUFFER_SIZE=120',
     'DEFINES += -DESPR_USE_SPI3 -DSPI0_USE_EASY_DMA=1',
     'ESPR_BLUETOOTH_ANCS=1', # Enable ANCS (Apple notifications) support
     'DEFINES += -DNRF_BL_DFU_INSECURE=1',
     'DEFINES += -DSAVE_ON_FLASH_SAVE  -DSAVE_ON_FLASH_SWSERIAL  -DSAVE_ON_FLASH_DUMP',
     'DEFINES += -DNO_DUMP_HARDWARE_INITIALISATION -DUSE_FONT_6X8',
     'NRF_SDK15=1'
   ]
 }
};

save_code_pages = 140; #96;
fstorage_pages = 2; # typically 2, 10 reduces risk of brick on first flash from stock FW
chip = {
  'part' : "NRF52840",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 256,
  'flash' : 1024,
  'speed' : 64,
  'usart' : 0, #2
  'spi' : 1, #3
  'i2c' : 1, #2
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
  'address' : ((0xf8 - fstorage_pages - save_code_pages) * 4096), # Bootloader at 0xF8000
  'page_size' : 4096,
  'pages' : save_code_pages,
  'flash_available' : 1024 - ((0x26 + (0x100-0xf8) + fstorage_pages + save_code_pages)*4), # Softdevice uses 38 pages of flash (0x26000/0x100), bootloader 0x100-0xe0=0x20, FS 2, code 96. Each page is 4 kb.
#   'address' : 0x60000000, # put this in external spiflash (see below) 
#  'pages' : 2048, # Entire 8MB of external flash
   },
};

devices = {
  'BTN1' : { 'pin' : 'D46', 'pinstate' : 'IN_PULLDOWN' },
  'BTN2' : { 'pin' : 'D45', 'pinstate' : 'IN_PULLDOWN' },

   'SPIFLASH' : {
            'pin_cs' : 'D20',
            'pin_sck' : 'D25',
            'pin_mosi' : 'D22',
            'pin_miso' : 'D23',
            'pin_wp' : 'D21',
            'pin_rst' : 'D24', # no reset but this is HOLD pin, we want it set to 1 like RST
            'size' : 8192*1024, # 8MB
            'memmap_base' : 0x60000000,
          },


};

# left-right, or top-bottom order
board = {
  'left' : [ 'VDD', 'VDD', 'RESET', 'VDD','5V','GND','GND','','','D3','D4','D28','D29','D30','D31'],
  'right' : [
     'D27', 'D26', 'D2', 'GND', 'D25','D24','D23', 'D22','D20','D19','',
     'D18','D17','D16','D15','D14','D13','D12','D11','',
     'D10','D9','D8','D7','D6','D5','D21','D1','D0'],
  '_notes' : {
    'D6' : "Serial console RX",
    'D8' : "Serial console TX"
  }
};
board["_css"] = """
#board {
  width: 528px;
  height: 800px;
  top: 0px;
  left : 200px;
  background-image: url(img/NRF528DK.jpg);
}
#boardcontainer {
  height: 900px;
}

#left {
    top: 219px;
    right: 466px;
}
#right {
    top: 150px;
    left: 466px;
}

.leftpin { height: 17px; }
.rightpin { height: 17px; }
""";

def get_pins():
  pins = pinutils.generate_pins(0,47) # 48 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD0", True)["functions"]["XL1"]=0;
  pinutils.findpin(pins, "PD1", True)["functions"]["XL2"]=0;
  pinutils.findpin(pins, "PD9", True)["functions"]["NFC1"]=0;
  pinutils.findpin(pins, "PD10", True)["functions"]["NFC2"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;

  pinutils.findpin(pins, "PD45", True)["functions"]["NEGATED"]=0;
  pinutils.findpin(pins, "PD46", True)["functions"]["NEGATED"]=0;
# everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
