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
 'name' : "DK08 fitness tracker",
# 'link' :  [ "https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF52-DK" ],
# 'espruino_page_link' : 'nRF52832DK',
 'boardname' : 'DK08', # visible in process.env.BOARD
 'default_console' : "EV_BLUETOOTH",
 'variables' : 2565, # 2600 SD5.0 0x200014B8 SD 3.0 0x200019C0  How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_DK08_SDK12.hex',
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
     'DEFINES+= -DUSE_FONT_6X8 -DBLE_HIDS_ENABLED=1 -DBLUETOOTH_NAME_PREFIX=\'"DK08"\'',
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'NRF_BL_DFU_INSECURE=1',
     'DEFINES+=-DBTN1_IS_TOUCH=1',
     'LINKER_BOOTLOADER=targetlibs/nrf5x_12/nrf5x_linkers/banglejs_dfu.ld',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0x8C,0x91'
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
    'address' : ((0x7a - 2 - 24) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    'pages' : 24,
#    'address' : 0x60380000, # Bootloader takes pages 120-127, FS takes 118-119
#    'pages' : 32,
    'flash_available' : 512 - ((0x1F + 6 + 2 + 24)*4) # Softdevice 2.0 uses 28 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
#    'flash_available' : 512 - ((0x1F + 8 + 2 + 10)*4) # Softdevice 3.0 uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
#    'flash_available' : 512 - ((35 + 8 + 2 + 16)*4) # Softdevice 5.0  uses 35 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
  },
};

devices = {
 'BTN1' : { 'pin' : 'D8', 'pinstate' : 'IN_PULLDOWN' },
  # Pin D22 is used for clock when driving neopixels - as not specifying a pin seems to break things
  'VIBRATE' : { 'pin' : 'D6' },
  'BAT' : {
            'pin_charging' : 'D24',
            'pin_voltage' : 'D5'
          },
#
  'SPIFLASH' : {
            'pin_sck' : 'D29',
            'pin_mosi' : 'D30',
            'pin_miso' : 'D31',
            'pin_cs' : 'D27',
            'size' : 2048*1024, # 4MB
            'memmap_base' : 0x60000000 # map into the address space (in software)
  }
};

board = {
#  'left' : [ 'VDD', 'VDD', 'RESET', 'VDD','5V','GND','GND','','','D3','D4','D28','D29','D30','D31'],
#  'right' : [
#     'D27', 'D26', 'D2', 'GND', 'D25','D24','D23', 'D22','D20','D19','',
#     'D18','D17','D16','D15','D14','D13','D12','D11','',
#     'D10','D9','D8','D7','D6','D5','D21','D1','D0'],
#  '_notes' : {
#    'D6' : "Serial console RX",
#    'D8' : "Serial console TX"
#  }
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

  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
