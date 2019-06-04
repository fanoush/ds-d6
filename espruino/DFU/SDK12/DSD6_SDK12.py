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
 'name' : "DS-D6",
 'link' :  [ "http://www.espruino.com/MDBT42Q" ],
 'espruino_page_link' : 'MDBT42Q', 
 'default_console' : "EV_SERIAL1",
 'default_console_tx' : "D23",
 'default_console_rx' : "D22",
 'default_console_baudrate' : "38400",
 'variables' : 2500, # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_dsd6_sdk12.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
     #'NET',
     'GRAPHICS',
     #'CRYPTO','SHA256','SHA512',
     #'AES',
     #'NFC',
     #'NEOPIXEL'
     #'FILESYSTEM'
     #'TLS'
   ],
   'makefile' : [
     'DEFINES+=-DHAL_NFC_ENGINEERING_BC_FTPAN_WORKAROUND=1', # Looks like proper production nRF52s had this issue
#     'DEFINES+=-DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"DS-D6"\'',
     'JSMODULESOURCES+=libs/js/Font4x4.min.js',
     'JSMODULESOURCES+=libs/js/Font4x8Numeric.min.js',
     'JSMODULESOURCES+=libs/js/Font4x4Numeric.min.js',
     'JSMODULESOURCES+=libs/js/Font6x8.min.js',
     'JSMODULESOURCES+=libs/js/Font6x12.min.js',
     'JSMODULESOURCES+=libs/js/Font8x12.min.js',
     'JSMODULESOURCES+=libs/js/Font8x16.min.js',
     'JSMODULESOURCES+=libs/js/FontDennis8.min.js',
#     'JSMODULESOURCES+=libs/js/SSD1306.min.js', # this watch has SPI OLED - SCK 6 MOSI 5 RST 4 DC 28 CS 29
#     'JSMODULESOURCES+=libs/js/DSD6.js',
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
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
    'address' : ((118 - 10) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    'page_size' : 4096,
    'pages' : 10,
    'flash_available' : 512 - ((31 + 8 + 2 + 10)*4) # Softdevice uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
  },
};

devices = {
  'BTN1' : { 'pin' : 'D30', 'pinstate' : 'IN_PULLDOWN' },
};


def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD5", True)["functions"]["SPI1_SCK"]=0;
  pinutils.findpin(pins, "PD6", True)["functions"]["SPI1_MOSI"]=0;
  pinutils.findpin(pins, "PD7", True)["functions"]["I2C1_SCL"]=0;
  pinutils.findpin(pins, "PD8", True)["functions"]["I2C1_SDA"]=0;
#only 1 I2C available in Espruino
#  pinutils.findpin(pins, "PD13", True)["functions"]["I2C2_SCL"]=0;
#  pinutils.findpin(pins, "PD14", True)["functions"]["I2C2_SDA"]=0;
  pinutils.findpin(pins, "PD22", True)["functions"]["USART1_RX"]=0;
  pinutils.findpin(pins, "PD23", True)["functions"]["USART1_TX"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["NEGATED"]=0; # button goes low when pressed, negate
# hardwired NRF52 analog inputs
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

# left-right, or top-bottom order
board_module = {
  'left' : [ 'GND','','','','D25','D26','D27','D28','D29','D30','D31','DEC4','DCC','VDD'],
  'right2' : [ 'D24', '', 'D23'],
  'right' : [ 'GND','D22','SWDIO','SWDCLK','D21','D20','D19','D18','D17','D16','D15','D14','D13','D12','D11' ],
  'bottom' : [ 'GND','D0','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','GND' ],
  '_notes' : {
    'D21' : "Also NRST if configured"
  }
};

board_module["_css"] = """
""";

board_breakout = {
  'left' : [ 'D25','D26','D27','D28','D29','D30','D31','D3','D4','D5','D11' ],
  'right' : [ 'D22','D20','D19','D18','D17','D16','D15','D14','3.3','Vin','GND'],
  'bottom' : [ 'D6','D8','D7','Vin','GND' ],
  'top' : [ 'D9','D10' ], 
  '_hide_not_on_connectors' : True,
  '_class' : "board_breakout",
  '_notes' : {
    'D22' : "Serial Console RX when Bluetooth disconnected",
    'D23' : "Serial Console TX when Bluetooth disconnected",
  }
};

board_breakout["_css"] = """
""";

boards = [board_module, board_breakout];
