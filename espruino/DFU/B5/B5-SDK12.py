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
 'name' : "SMA B5 GPS smartwatch",
# 'link' :  [ "https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF52-DK" ],
# 'espruino_page_link' : 'nRF52832DK',
 'boardname' : 'SMAB5', # visible in process.env.BOARD
  # This is the PCA10036
 'default_console' : "EV_BLUETOOTH",
 'variables' : 2565, # *16//13 2565 SD5.0 0x200014B8 SD 3.0 0x200019C0  How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_SMAB5.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
#     'NET',
     'GRAPHICS',
#     'LCD_SPI',
#     'NFC',
#     'NEOPIXEL'
   ],
   'makefile' : [
#    'SAVE_ON_FLASH=1',
#     'DEFINES+=-DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'DEFINES += -DCONFIG_NFCT_PINS_AS_GPIOS', # Allow using NFC pins for gpio
#     'DEFINES+=-DNRF_BLE_GATT_MAX_MTU_SIZE=131 -DNRF_BLE_MAX_MTU_SIZE=131', # increase MTU from default of 23
     'DEFINES+=-DNRF_BLE_GATT_MAX_MTU_SIZE=53 -DNRF_BLE_MAX_MTU_SIZE=53', # increase MTU from default of 23
     'LDFLAGS += -Xlinker --defsym=LD_APP_RAM_BASE=0x2c40', # set RAM base to match MTU
     'DEFINES+=-DNO_DUMP_HARDWARE_INITIALISATION', # don't dump hardware init - not used and saves 1k of flash
#     'DEFINES+=-DJSVAR_FORCE_16_BYTE=1', # 16 byte variables
     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"B5"\'',
     'DEFINES+=-DUSE_FONT_6X8 -DBLE_HIDS_ENABLED=1 -DGRAPHICS_PALETTED_IMAGES=1 -DGRAPHICS_FAST_PATHS=1',
     'NRF_BL_DFU_INSECURE=1',
     'DEFINES+=-DBTN1_IS_TOUCH=1',
#     'LINKER_BOOTLOADER=targetlibs/nrf5x_12/nrf5x_linkers/banglejs_dfu.ld',
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0x8C,0x91',

   ]
 }
};


chip = {
  'part' : "NRF52832",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 64,
  'flash' : 512,
  'speed' : 64,
  'usart' : 1,
  'spi' : 1,
  'i2c' : 1,
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
    'page_size' : 4096,
    'address' : ((118 - 16) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
#    'address' : ((118 - 10) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    'pages' : 16, #10
#    'flash_available' : 512 - ((28 + 8 + 2 + 10)*4) # Softdevice 2.0 uses 28 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
    'flash_available' : 512 - ((31 + 8 + 2 + 16)*4) # Softdevice 3.0 uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
#    'flash_available' : 512 - ((35 + 8 + 10 + 10)*4) # Softdevice 5.0  uses 35 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
#    'flash_available' : 512 - ((38 + 8 + 2 +16)*4) # Softdevice 6.x  uses 38 pages of flash, bootloader 8, FS 2, no code. Each page is 4 kb.
  },
};

devices = {
  'BTN1' : { 'pin' : 'D9', 'pinstate' : 'IN_PULLDOWN' },
  'VIBRATE' : { 'pin' : 'D30' },
  'SPIFLASH' : {
            'pin_sck' : 'D14',
            'pin_mosi' : 'D13',
            'pin_miso' : 'D11',
            'pin_cs' : 'D12',
##            'pin_wp' : '',
##            'pin_hold' : '',
##            'pin_rst' : '', # no reset but this is HOLD pin for XENON, we want it set to 1
            'size' : 2048*1024, # 2MB
            'memmap_base' : 0x60000000 # map into the address space (in software)
 }
};


def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
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
  # Make buttons and LEDs negated
  pinutils.findpin(pins, "PD9", True)["functions"]["NEGATED"]=0;

  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
