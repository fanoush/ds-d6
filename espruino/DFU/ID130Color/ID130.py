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
 'name' : "ID130",
 'link' :  [ "https://github.com/abhigkar/ID107-HR-Plus-Reverse-Engineering" ],
 'espruino_page_link' : 'MDBT42Q',
  # This is the PCA10036
 'default_console' : "EV_BLUETOOTH",
# 'default_console_tx' : "D6",
 #'default_console_rx' : "D8",
 'default_console_baudrate' : "9600",
 'variables' : 2250, # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1, 
 'binary_name' : 'espruino_%v_ID130.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
     'GRAPHICS',
   ],
   'makefile' : [
     #'DEFINES+=-DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"ID130"\'',
     'DEFINES+=-DUSE_FONT_6X8 -DBLE_HIDS_ENABLED=1',
#     'JSMODULESOURCES+=libs/js/Font4x4.min.js',
#     'JSMODULESOURCES+=libs/js/Font4x8Numeric.min.js',
#     'JSMODULESOURCES+=libs/js/Font4x4Numeric.min.js',
#     'JSMODULESOURCES+=libs/js/Font6x8.min.js',
#     'JSMODULESOURCES+=libs/js/Font6x12.min.js',
#     'JSMODULESOURCES+=libs/js/Font8x12.min.js',
#     'JSMODULESOURCES+=libs/js/Font8x16.min.js',
#     'JSMODULESOURCES+=libs/js/FontDennis8.min.js',
#     'INCLUDE += -I$(ROOT)/libs/id107hp',
     'WRAPPERSOURCES += boards/jswrap_ID130.c',
     'DFU_SETTINGS=--sd-req 129,136 --dev-type 616 --dev-revision 616', ## TODO change for ID107 HR plus
     'NRF_SDK11=1'
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
    'address' : ((121 - 2 - 21) * 4096), # Bootloader takes pages 121-127, FS takes 119-120
    'page_size' : 4096,
    'pages' : 21,
    'flash_available' : 512 - ((28 + 7 + 2 + 21)*4) # Softdevice uses 28 pages of flash, bootloader 7, FS 2, code 21. Each page is 4 kb.
  },
};

devices = {
  'BTN1' : { 'pin' : 'D7', 'pinstate' : 'IN' }, #also needs D6 to be set low
};

#};

# left-right, or top-bottom order
board = {
};

board["_css"] = """
""";

def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD0", True)["functions"]["XL1"]=0;
  pinutils.findpin(pins, "PD1", True)["functions"]["XL2"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;

  pinutils.findpin(pins, "PD7", True)["functions"]["NEGATED"]=0; # button goes low when pressed, negate
  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
