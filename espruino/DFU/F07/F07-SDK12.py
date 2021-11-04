#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------

import pinutils;

info = {
 'name' : "F07 fitness tracker",
 'boardname' : 'F07', # visible in process.env.BOARD
 'default_console' : "EV_BLUETOOTH",
 'variables' : 2560*16//13, # 2600 SD5.0 0x200014B8 SD 3.0 0x200019C0  How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_F07_SDK12.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
#     'NET',
     'GRAPHICS',
#     'NFC',
#     'NEOPIXEL'
   ],
   'makefile' : [
#     'DEFINES+=-DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'CFLAGS += -D__STARTUP_CLEAR_BSS -D__START=main',
     'LDFLAGS += -D__STARTUP_CLEAR_BSS -D__START=main -nostartfiles',
     'DEFINES+=-DNO_DUMP_HARDWARE_INITIALISATION',
     'DEFINES+= -DUSE_FONT_6X8 -DBLE_HIDS_ENABLED=1 -DBLUETOOTH_NAME_PREFIX=\'"F07"\'',
     'DEFINES+=-DNRF_BLE_GATT_MAX_MTU_SIZE=53 -DNRF_BLE_MAX_MTU_SIZE=53', # increase MTU from default of 23
     'LDFLAGS += -Xlinker --defsym=LD_APP_RAM_BASE=0x2c40', # set RAM base to match MTU
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'NRF_BL_DFU_INSECURE=1',
     'DEFINES+=-DBTN1_IS_TOUCH=1',
     'DEFINES += -DSPIFLASH_SHARED_SPI',
     'DEFINES+= -DSAVE_ON_FLASH_SAVE -DSAVE_ON_FLASH_SWSERIAL',
     'LINKER_BOOTLOADER=targetlibs/nrf5x_12/nrf5x_linkers/banglejs_dfu.ld',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0x8C,0x91'
   ]
 }
};

saved_code_pages = 28;
chip = {
  'part' : "NRF52832",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 64,
  'flash' : 512,
  'speed' : 64,
  'usart' : 0,
  'spi' : 1,
  'i2c' : 1,
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
    'page_size' : 4096,
    'address' : ((0x7a - 2 - saved_code_pages) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    'pages' : saved_code_pages,
#    'address' : 0x601a3000, # font chip empty space 0x5D pages
#    'pages' : 0x5D,
    'flash_available' : 512 - ((0x1F + 6 + 2 + saved_code_pages)*4) # Softdevice 3.0 uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
#    'flash_available' : 512 - ((35 + 8 + 2 + 16)*4) # Softdevice 5.0  uses 35 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
  },
};

devices = {
 'BTN1' : { 'pin' : 'D26', 'pinstate' : 'IN_PULLDOWN' },
  'VIBRATE' : { 'pin' : 'D25' },
#
  'SPIFLASH' : {
            'pin_sck' : 'D19',
            'pin_mosi' : 'D20',
            'pin_miso' : 'D22',
            'pin_cs' : 'D23',
            'size' : 2048*1024, # 2MB
            'memmap_base' : 0x60000000 # map into the address space (in software)
  }
};

board = {
};

def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
#  pinutils.findpin(pins, "PD0", True)["functions"]["XL1"]=0;
#  pinutils.findpin(pins, "PD1", True)["functions"]["XL2"]=0;
#  pinutils.findpin(pins, "PD9", True)["functions"]["NFC1"]=0;
#  pinutils.findpin(pins, "PD10", True)["functions"]["NFC2"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;

  pinutils.findpin(pins, "PD26", True)["functions"]["NEGATED"]=0;

  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
