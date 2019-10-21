#!/usr/bin/env python

import os.path
import zipfile
import tempfile
import random
import string
import shutil
import re

from os.path  import basename

verbose = False
gatttool= "gatttool" # -i hci1

class Unpacker(object):
   def entropy(self, length):
       return ''.join(random.choice(string.lowercase) for i in range (length))

   def unpack_zipfile(self, file):

        if not os.path.isfile(file):
            raise Exception("Error: file, not found!")

        # Create unique working direction into which the zip file is expanded
        self.unzip_dir = "{0}/{1}_{2}".format(tempfile.gettempdir(), os.path.splitext(basename(file))[0], self.entropy(6))

        datfilename = ""
        binfilename = ""
        manfilename = ""

        with zipfile.ZipFile(file, 'r') as zip:
            files = [item.filename for item in zip.infolist()]
            datfilename = [m.group(0) for f in files for m in [re.search('.*\.dat', f)] if m].pop()
            binfilename = [m.group(0) for f in files for m in [re.search('.*\.bin', f)] if m].pop()
            manfilename = [m.group(0) for f in files for m in [re.search('.*\.json', f)] if m].pop()

            zip.extractall(r'{0}'.format(self.unzip_dir))

        datfile = "{0}/{1}".format(self.unzip_dir, datfilename)
        binfile = "{0}/{1}".format(self.unzip_dir, binfilename)
        manfile = "{0}/{1}".format(self.unzip_dir, manfilename)

        # print "DAT file: " + datfile
        # print "BIN file: " + binfile

        return binfile, datfile, manfile

   def delete(self):
       # delete self.unzip_dir and its contents
       shutil.rmtree(self.unzip_dir)

import sys
import binascii
import re

def bytes_to_uint32_le(bytes):
    return  (int(bytes[3], 16) << 24) | (int(bytes[2], 16) << 16) | (int(bytes[1], 16) <<  8) | (int(bytes[0], 16) <<  0)

def uint32_to_bytes_le(uint32):
    return [(uint32 >> 0)  & 0xff, 
            (uint32 >> 8)  & 0xff, 
            (uint32 >> 16) & 0xff, 
            (uint32 >> 24) & 0xff]

def uint16_to_bytes_le(value):
    return [(value >> 0 & 0xFF),
            (value >> 8 & 0xFF)]

def zero_pad_array_le(data, padsize):
    for i in range(0, padsize):
        data.insert(0, 0)

def array_to_hex_string(arr):
    hex_str = ""
    for val in arr:
        if val > 255:
            raise Exception("Value is greater than it is possible to represent with one byte")
        hex_str += "%02x" % val

    return hex_str

def crc32_unsigned(bytestring):
    return binascii.crc32(bytestring) % (1 << 32)

def mac_string_to_uint(mac):
    parts = list(re.match('(..):(..):(..):(..):(..):(..)', mac).groups())
    ints = map(lambda x: int(x, 16), parts)

    res = 0
    for i in range(0, len(ints)):
        res += (ints[len(ints)-1 - i] << 8*i)

    return res

def uint_to_mac_string(mac):
    ints = [0, 0, 0, 0, 0, 0]
    for i in range(0, len(ints)):
        ints[len(ints)-1 - i] = (mac >> 8*i) & 0xff

    return ':'.join(map(lambda x: '{:02x}'.format(x).upper(), ints))

# Print a nice console progress bar
def print_progress(iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = 'x' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s (%d of %d bytes)' % (prefix, bar, percents, '%', suffix, iteration, total)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

import os
import pexpect
import re
import json
from abc   import ABCMeta, abstractmethod
from array import array
#from util  import *


class NrfBleDfuController(object):
    __metaclass__ = ABCMeta

    # Class instance variables
    ctrlpt_handle        = 0
    ctrlpt_cccd_handle   = 0
    data_handle          = 0

    pkt_receipt_interval = 10
    pkt_payload_size     = 20

    # --------------------------------------------------------------------------
    #  Start the firmware update process
    # --------------------------------------------------------------------------
    @abstractmethod
    def start(self):
        pass

    # --------------------------------------------------------------------------
    #  Check if the peripheral is running in bootloader (DFU) or application mode
    #  Returns True if the peripheral is in DFU mode
    # --------------------------------------------------------------------------
    @abstractmethod
    def check_DFU_mode(self):
        pass

    @abstractmethod
    # --------------------------------------------------------------------------
    #  Switch from application to bootloader (DFU)
    # --------------------------------------------------------------------------
    def switch_to_dfu_mode(self):
        pass

    # --------------------------------------------------------------------------
    #  Parse notification status results
    # --------------------------------------------------------------------------
    @abstractmethod
    def _dfu_parse_notify(self, notify):
        pass

    # --------------------------------------------------------------------------
    #  Wait for a notification and parse the response
    # --------------------------------------------------------------------------
    @abstractmethod
    def _wait_and_parse_notify(self):
        pass

    def __init__(self, target_mac, firmware_path, datfile_path, manfile_path):
        self.target_mac = target_mac

        self.firmware_path = firmware_path
        self.datfile_path = datfile_path
        self.manfile_path = manfile_path

        self.ble_conn = pexpect.spawn("%s -b '%s' -t random --interactive" % (gatttool, target_mac))
        self.ble_conn.delaybeforesend = 0

    # --------------------------------------------------------------------------
    #  Start the firmware update process
    # --------------------------------------------------------------------------
    def start(self):
        (_, self.ctrlpt_handle, self.ctrlpt_cccd_handle) = self._get_handles(self.UUID_CONTROL_POINT)
        (_, self.data_handle, _) = self._get_handles(self.UUID_PACKET)

        if verbose:
            print 'Control Point Handle: 0x%04x, CCCD: 0x%04x' % (self.ctrlpt_handle, self.ctrlpt_cccd_handle)
            print 'Packet handle: 0x%04x' % (self.data_handle)

        # Subscribe to notifications from Control Point characteristic
        self._enable_notifications(self.ctrlpt_cccd_handle)

        # Set the Packet Receipt Notification interval
        prn = uint16_to_bytes_le(self.pkt_receipt_interval)
        self._dfu_send_command(Procedures.SET_PRN, prn)

        self._dfu_send_init()

        self._dfu_send_image()

    # --------------------------------------------------------------------------
    # Initialize: 
    #    Hex: read and convert hexfile into bin_array 
    #    Bin: read binfile into bin_array
    # --------------------------------------------------------------------------
    def input_setup(self):
        print "Sending file " + os.path.split(self.firmware_path)[1] + " to " + self.target_mac

        if self.firmware_path == None:
            raise Exception("input invalid")

        if self.manfile_path != None:
            j = json.load(open(self.manfile_path, 'r'))
            self.manifest = j["manifest"] if "manifest" in j else None
        else:
            self.manifest = None

        name, extent = os.path.splitext(self.firmware_path)

        if extent == ".bin":
            self.bin_array = array('B', open(self.firmware_path, 'rb').read())

            self.image_size = len(self.bin_array)
            print "Binary imge size: %d" % self.image_size
            print "Binary CRC32: %d" % crc32_unsigned(array_to_hex_string(self.bin_array))

            return

        if extent == ".hex":
            intelhex = IntelHex(self.firmware_path)
            self.bin_array = intelhex.tobinarray()
            self.image_size = len(self.bin_array)
            print "bin array size: ", self.image_size
            return

        raise Exception("input invalid")

    # --------------------------------------------------------------------------
    # Perform a scan and connect via gatttool.
    # Will return True if a connection was established, False otherwise
    # --------------------------------------------------------------------------
    def scan_and_connect(self, timeout=3, mtu=247):
        if verbose: print "scan_and_connect"
        self.handles = None
        print "Connecting to %s" % (self.target_mac)

        try:
            self.ble_conn.expect('\[LE\]>', timeout=timeout)
        except pexpect.TIMEOUT, e:
            return False

        self.ble_conn.sendline('connect')

        try:
            res = self.ble_conn.expect('.*Connection successful.*', timeout=timeout)
        except pexpect.TIMEOUT, e:
            return False

        print "Connected"
        if mtu>23:
            #MTU negotiation
            self.ble_conn.sendline('mtu %d' % mtu)
            res=self.ble_conn.expect('.*MTU was exchanged successfully: (.+)\r.*', timeout=timeout)
            res=re.findall('.*MTU was exchanged successfully: (.+)\r.*',self.ble_conn.after)
            self.mtu=int(res[0])
        else:
            self.mtu=mtu
        #get handles for all characteristics
        self.ble_conn.sendline("characteristics")
        # self.ble_conn.sendline("   ")
        # res=self.ble_conn.expect('.*uuid: ........-....-....-....-............\r\n.*\[LE\]>',timeout=3)
        # sadly there is nothing to match for, no end marker
        # you get prompt immediatelly and data comes later
        # even matchin for next command with spaces ends earlier than list of characteristics
        # also the [LE]> prompt is written on each line and then erased
        # so we just wait 3 seconds and hope to get all of them
        res=self.ble_conn.expect(pexpect.TIMEOUT,timeout=3)
        #get all output until timeout and match all handles
        self.handles=re.findall('.*handle: (0x....),.*char value handle: (0x....),.*uuid: (........-....-....-....-............)', self.ble_conn.before)
        return True

    # --------------------------------------------------------------------------
    #  Disconnect from the peripheral and close the gatttool connection
    # --------------------------------------------------------------------------
    def disconnect(self):
        self.ble_conn.sendline('exit')
        self.ble_conn.close()
        self.handles = None

    def target_mac_increase(self, inc):
        self.target_mac = uint_to_mac_string(mac_string_to_uint(self.target_mac) + inc)

        # Re-start gatttool with the new address
        self.disconnect()
        self.ble_conn = pexpect.spawn("%s -b '%s' -t random --interactive" % (gatttool, self.target_mac))
        self.ble_conn.delaybeforesend = 0

    # --------------------------------------------------------------------------
    #  Fetch handles for a given UUID.
    #  Will return a three-tuple: (char handle, value handle, CCCD handle)
    #  Will raise an exception if the UUID is not found
    # --------------------------------------------------------------------------
    def _get_handles(self, uuid):
        for h in self.handles:
            if h[2] == uuid:
                return (int(h[0], 16), int(h[1], 16), int(h[1], 16)+1)
        raise Exception("UUID not found: {}".format(uuid))
        #return (None, None, None)
        #below old code discovering just one handle from all characteristics below
        #now all are cached at connect time into self.handles
        #as scanning for more like this was slow
        self.ble_conn.before = ""
        self.ble_conn.sendline('characteristics')
        try:
            self.ble_conn.expect([uuid], timeout=2)
            handles = re.findall('.*handle: (0x....),.*char value handle: (0x....)', self.ble_conn.before)
            (handle, value_handle) = handles[-1]
        except pexpect.TIMEOUT, e:
            raise Exception("UUID not found: {}".format(uuid))
        return (int(handle, 16), int(value_handle, 16), int(value_handle, 16)+1)

    # --------------------------------------------------------------------------
    #  Wait for notification to arrive.
    #  Example format: "Notification handle = 0x0019 value: 10 01 01"
    # --------------------------------------------------------------------------
    def _dfu_wait_for_notify(self):
        while True:
            if verbose: print "dfu_wait_for_notify"

            if not self.ble_conn.isalive():
                print "connection not alive"
                return None

            try:
                index = self.ble_conn.expect('Notification handle = .*? \r\n', timeout=10)

            except pexpect.TIMEOUT:
                #
                # The gatttool does not report link-lost directly.
                # The only way found to detect it is monitoring the prompt '[CON]'
                # and if it goes to '[   ]' this indicates the connection has
                # been broken.
                # In order to get a updated prompt string, issue an empty
                # sendline('').  If it contains the '[   ]' string, then
                # raise an exception. Otherwise, if not a link-lost condition,
                # continue to wait.
                #
                self.ble_conn.sendline('')
                string = self.ble_conn.before
                if '[   ]' in string:
                    print 'Connection lost! '
                    raise Exception('Connection Lost')
                return None

            if index == 0:
                after = self.ble_conn.after
                hxstr = after.split()[3:]
                handle = long(float.fromhex(hxstr[0]))
                return hxstr[2:]

            else:
                print "unexpected index: {0}".format(index)
                return None

    # --------------------------------------------------------------------------
    #  Send a procedure + any parameters required
    # --------------------------------------------------------------------------
    def _dfu_send_command(self, procedure, params=[], nowait=False):
        if verbose: print '_dfu_send_command'

        cmd  = 'char-write-req 0x%04x %02x' % (self.ctrlpt_handle, procedure)
        cmd += array_to_hex_string(params)

        if verbose: print cmd

        self.ble_conn.sendline(cmd)

        if nowait: return
        # Verify that command was successfully written
        try:
            res = self.ble_conn.expect('Characteristic value was written successfully.*', timeout=5)
        except pexpect.TIMEOUT, e:
            print "State timeout"

    # --------------------------------------------------------------------------
    #  Send an array of bytes
    # --------------------------------------------------------------------------
    def _dfu_send_data(self, data):
        cmd  = 'char-write-cmd 0x%04x' % (self.data_handle)
        cmd += ' '
        cmd += array_to_hex_string(data)

        if verbose: print cmd

        self.ble_conn.sendline(cmd)

    # --------------------------------------------------------------------------
    #  Enable notifications from the Control Point Handle
    # --------------------------------------------------------------------------
    def _enable_notifications(self, cccd_handle):
        if verbose: print '_enable_notifications'

        cmd  = 'char-write-req 0x%04x %s' % (cccd_handle, '0100')

        if verbose: print cmd

        self.ble_conn.sendline(cmd)

        # Verify that command was successfully written
        try:
            res = self.ble_conn.expect('Characteristic value was written successfully.*', timeout=5)
        except pexpect.TIMEOUT, e:
            print "State timeout"

import math
import pexpect
import time
from array import array
#from util  import *
#from nrf_ble_dfu_controller import NrfBleDfuController

class Procedures:
    START_DFU                   = 1
    INITIALIZE_DFU              = 2
    RECEIVE_FIRMWARE_IMAGE      = 3
    VALIDATE_FIRMWARE           = 4
    ACTIVATE_IMAGE_AND_RESET    = 5
    RESET_SYSTEM                = 6
    REPORT_RECEIVED_IMAGE_SIZE  = 7
    PRN_REQUEST                 = 8
    RESPONSE                    = 16
    PACKET_RECEIPT_NOTIFICATION = 17

    string_map = {
        START_DFU                   : "START_DFU",
        INITIALIZE_DFU              : "INITIALIZE_DFU",
        RECEIVE_FIRMWARE_IMAGE      : "RECEIVE_FIRMWARE_IMAGE",
        VALIDATE_FIRMWARE           : "VALIDATE_FIRMWARE",
        ACTIVATE_IMAGE_AND_RESET    : "ACTIVATE_IMAGE_AND_RESET",
        RESET_SYSTEM                : "RESET_SYSTEM",
        REPORT_RECEIVED_IMAGE_SIZE  : "REPORT_RECEIVED_IMAGE_SIZE",
        PRN_REQUEST                 : "PACKET_RECEIPT_NOTIFICATION_REQUEST",
        RESPONSE                    : "RESPONSE",
        PACKET_RECEIPT_NOTIFICATION : "PACKET_RECEIPT_NOTIFICATION",
    }

    @staticmethod
    def to_string(proc):
        return Procedures.string_map[proc]

    @staticmethod
    def from_string(proc_str):
        return int(proc_str, 16)

class Responses:
    SUCCESS                     = 1
    INVALID_STATE               = 2
    NOT_SUPPORTED               = 3
    DATA_SIZE_EXCEEDS_LIMITS    = 4
    CRC_ERROR                   = 5
    OPERATION_FAILED            = 6

    string_map = {
        SUCCESS                     : "SUCCESS",
        INVALID_STATE               : "INVALID_STATE",
        NOT_SUPPORTED               : "NOT_SUPPORTED",
        DATA_SIZE_EXCEEDS_LIMITS    : "DATA_SIZE_EXCEEDS_LIMITS",
        CRC_ERROR                   : "CRC_ERROR",
        OPERATION_FAILED            : "OPERATION_FAILED",
    }

    @staticmethod
    def to_string(res):
        return Responses.string_map[res]

    @staticmethod
    def from_string(res_str):
        return int(res_str, 16)


class BleDfuControllerLegacy(NrfBleDfuController):
    # Class constants
    UUID_DESAY_AT_WRITE         = "00000003-0000-1000-8000-00805f9b34fb"
    UUID_DESAY_AT_READ          = "00000004-0000-1000-8000-00805f9b34fb"
    UUID_DESAY_PACKET           = "00000005-0000-1000-8000-00805f9b34fb"
    UUID_DESAY_CONTROL_POINT    = "00000006-0000-1000-8000-00805f9b34fb"
    UUID_DESAY_VERSION          = "00000008-0000-1000-8000-00805f9b34fb"
    UUID_CONTROL_POINT          = "00001531-1212-efde-1523-785feabcd123"
    UUID_PACKET                 = "00001532-1212-efde-1523-785feabcd123"
    UUID_VERSION                = "00001534-1212-efde-1523-785feabcd123"
    UUID_NORDIC_UART_RX         = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    UUID_NORDIC_UART_TX         = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
    # Constructor inherited from abstract base class

    # --------------------------------------------------------------------------
    #  Start the firmware update process
    # --------------------------------------------------------------------------
    def start(self, test=False):
        self.pkt_receipt_interval = 15 #5

        if verbose:
            print 'Control Point Handle: 0x%04x, CCCD: 0x%04x' % (self.ctrlpt_handle, self.ctrlpt_cccd_handle)
            print 'Packet handle: 0x%04x' % (self.data_handle)

        if test:
            # Reset Command
            print "Test mode finished - restarting"
            self._dfu_send_command(Procedures.RESET_SYSTEM,nowait=False)
            return

        if self.mtu > 23: self.pkt_payload_size = self.mtu-3
        # Subscribe to notifications from Control Point characteristic
        if verbose: print "Enabling notifications"
        self._enable_notifications(self.ctrlpt_cccd_handle)

        # Send 'START DFU' + Application Command
        # 1 SD, 2 bootloader, 3 SD+BL, 4 application
        alen = blen = slen = 0
        if self.manifest:
            if "bootloader" in self.manifest:
                t=0x02
                blen=len(self.bin_array)
            if "softdevice" in self.manifest:
                t=0x01
                slen=len(self.bin_array)
            if "softdevice_bootloader" in self.manifest:
                t=0x03
                blen=int(self.manifest["softdevice_bootloader"]["bl_size"])
                slen=int(self.manifest["softdevice_bootloader"]["sd_size"])
            if "application" in self.manifest:
                t=0x04
                alen=len(self.bin_array)
        else:
            t=0x04
            alen=len(self.bin_array)
        # image size 3x uint32
        # <Length of SoftDevice><Length of bootloader><Length of application>
        hex_size_array_lsb = uint32_to_bytes_le(slen)+uint32_to_bytes_le(blen)+uint32_to_bytes_le(alen)

        if verbose: print "Sending START_DFU ",t,hex_size_array_lsb
        self._dfu_send_command(Procedures.START_DFU, [t])
        self._dfu_send_data(hex_size_array_lsb)

        # Wait for response to Image Size
        print "Waiting for Image Size notification"
        try:
            self._wait_and_parse_notify()
        except Exception as e:
            if "INVALID_STATE" in str(e):
                print "INVALID_STATE error, resetting device, please retry"
                self._dfu_send_command(Procedures.RESET_SYSTEM)
            raise e
        # Send 'INIT DFU' + Init Packet Command
        self._dfu_send_command(Procedures.INITIALIZE_DFU, [0x00])

        # Transmit the Init image (DAT).
        self._dfu_send_init()

        # Send 'INIT DFU' + Init Packet Complete Command
        self._dfu_send_command(Procedures.INITIALIZE_DFU, [0x01])

        print "Waiting for INIT DFU notification"
        # Wait for INIT DFU notification (indicates flash erase completed)
        self._wait_and_parse_notify()

        # Set the Packet Receipt Notification interval
        if verbose: print "Setting pkt receipt notification interval"
        prn = uint16_to_bytes_le(self.pkt_receipt_interval)
        self._dfu_send_command(Procedures.PRN_REQUEST, prn)

        # Send 'RECEIVE FIRMWARE IMAGE' command to set DFU in firmware receive state. 
        self._dfu_send_command(Procedures.RECEIVE_FIRMWARE_IMAGE)

        # Send bin_array contents as as series of packets (burst mode).
        # Each segment is pkt_payload_size bytes long.
        # For every pkt_receipt_interval sends, wait for notification.
        segment_count = 0
        segment_total = int(math.ceil(self.image_size/float(self.pkt_payload_size)))
        time_start = time.time()
        last_send_time = time.time()
        print "Begin DFU (MTU %d, packet size %d)" % (self.mtu, self.pkt_payload_size)
        i=0
        while i < self.image_size:
            segment = self.bin_array[i:i + self.pkt_payload_size]
            self._dfu_send_data(segment)
            #check if longer first packet worked
            if i==0 and self.mtu>23 and self.pkt_payload_size>20:
                self._dfu_send_command(Procedures.REPORT_RECEIVED_IMAGE_SIZE)
                (proc, res, imgsize) = self._wait_and_parse_notify()
                if res == Responses.SUCCESS:
                    if imgsize==0:
                        #longer packet didn't get through
                        print 'Failed to send first long packet, falling back to 20 byte packet size'
                        self.pkt_payload_size=20
                        segment_total = int(math.ceil(self.image_size/float(self.pkt_payload_size)))
                        segment_count = 0
                        continue
                    else:
                        if verbose: print "First long packet worked, offset now %d" % imgsize

            segment_count += 1
            i+=self.pkt_payload_size

            # print "segment #{} of {}, dt = {}".format(segment_count, segment_total, time.time() - last_send_time)
            # last_send_time = time.time()

            if (segment_count == segment_total):
                print_progress(self.image_size, self.image_size, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

                duration = time.time() - time_start
                print "\nUpload complete in {} minutes and {} seconds".format(int(duration / 60), int(duration % 60))
                if verbose: print "segments sent: {}".format(segment_count)

                print "Waiting for DFU complete notification"
                # Wait for DFU complete notification
                self._wait_and_parse_notify()

            elif (segment_count % self.pkt_receipt_interval) == 0:
                try:
                    (proc, res, pkts) = self._wait_and_parse_notify()
                    if verbose: print "\nNotification got %d, segment %d offset %d" % (pkts,segment_count,i)
                    if pkts != i: print "\nNotification offset=%d, we have %d x %d = %d" % (pkts,segment_count,self.pkt_payload_size,i)
                except Exception as e:
                    if str(e) != "No notification received":
                        raise
                    print "\nNotification timeout, trying to recover"
                    self._dfu_send_command(Procedures.REPORT_RECEIVED_IMAGE_SIZE)
                    (proc, res, imgsize) = self._wait_and_parse_notify()
                    if res == Responses.SUCCESS:
                        i=imgsize
                        print 'OK, resuming at offset %d' % (imgsize)
                        continue
                    raise Exception("No notification received and retry failed")

                if res != Responses.SUCCESS:
                    raise Exception("bad notification status: {}".format(Responses.to_string(res)))

                print_progress(pkts, self.image_size, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        # Send Validate Command
        self._dfu_send_command(Procedures.VALIDATE_FIRMWARE)

        print "Waiting for Firmware Validation notification"
        # Wait for Firmware Validation notification
        self._wait_and_parse_notify()

        # Wait a bit for copy on the peer to be finished
        time.sleep(1)

        # Send Activate and Reset Command
        print "Activate and reset"
        self._dfu_send_command(Procedures.ACTIVATE_IMAGE_AND_RESET)

    # --------------------------------------------------------------------------
    #  Check if the peripheral is running in bootloader (DFU) or application mode
    #  Returns True if the peripheral is in DFU mode
    #  Presets handles for data and control poits
    # --------------------------------------------------------------------------
    def check_DFU_mode(self):
        if verbose: print "Checking DFU State..."
        try: #try nordic DFU guids
            (_, bl_value_handle, _) = self._get_handles(self.UUID_VERSION)
            (_, self.data_handle, _) = self._get_handles(self.UUID_PACKET)
            (_, self.ctrlpt_handle, self.ctrlpt_cccd_handle) = self._get_handles(self.UUID_CONTROL_POINT)
            return True
        except:
            try: #now try desay DFU guids
                (_, bl_value_handle, _) = self._get_handles(self.UUID_DESAY_VERSION)
                (_, self.ctrlpt_handle, self.ctrlpt_cccd_handle) = self._get_handles(self.UUID_DESAY_CONTROL_POINT)
                (_, self.data_handle, _) = self._get_handles(self.UUID_DESAY_PACKET)
                return True
            except:
                pass
        #no known guids
        return False
        # below is unused code that could check version characteristics value
        # however in code above we are happy enough that service exists

        #if verbose: print bl_value_handle
        #cmd = 'char-read-uuid %s' % self.UUID_VERSION
        cmd = 'char-read-hnd %s' % bl_value_handle
        if verbose: print cmd
        self.ble_conn.sendline(cmd)
        try:
            #res = self.ble_conn.expect('handle:.*', timeout=3)
            res = self.ble_conn.expect('Characteristic value/descriptor:.*', timeout=3)
        except pexpect.TIMEOUT, e:
            print "State timeout"
            return False
        except:
            pass
        return self.ble_conn.after.find(": 08 00")!=-1

    def switch_to_dfu_mode(self):

        try:
            #(_, bl_value_handle, bl_cccd_handle) = self._get_handles(self.UUID_DESAY_AT_READ)
            ## Enable notifications - not needed
            #cmd = 'char-write-req 0x%02x 0100' % (bl_cccd_handle)
            #if verbose: print cmd
            #self.ble_conn.sendline(cmd)
            (_, bl_value_handle, _) = self._get_handles(self.UUID_DESAY_AT_WRITE)
            # Reset the board in DFU mode. After reset the board will be disconnected
            print "Found Desay firmware, rebooting to bootloader"
            cmd = 'char-write-req 0x%02x ' % (bl_value_handle)
            self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("BT+UPGB:1\r\n")))
            self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("BT+RESET\r\n")))
        except:
            try:
                (_, bl_value_handle, bl_cccd_handle) = self._get_handles(self.UUID_CONTROL_POINT)
                print "Found Nordic Buttonless service, rebooting to bootloader"
                # Enable notifications
                cmd = 'char-write-req 0x%02x 0100' % (bl_cccd_handle)
                if verbose: print cmd
                self.ble_conn.sendline(cmd)
                # Reset the board in DFU mode. After reset the board will be disconnected
                cmd = 'char-write-req 0x%02x 0104' % (bl_value_handle)
                if verbose: print cmd
                self.ble_conn.sendline(cmd)
            except:
                try:
                    (_, bl_value_handle, bl_cccd_handle) = self._get_handles(self.UUID_NORDIC_UART_TX)
                    print "Found Nordic UART, inviting monkeys with typewriters"
                    #enable notifications on read otherwise it does not work for micropython
                    cmd = 'char-write-req 0x%02x 0100' % (bl_cccd_handle)
                    self.ble_conn.sendline(cmd)
                    (_, bl_value_handle, _) = self._get_handles(self.UUID_NORDIC_UART_RX)
                    # nordic uart - can be espruino or micropython
                    cmd = 'char-write-req 0x%02x ' % (bl_value_handle)
                    self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("poke32(0x4000051c,1)")))
                    self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("\r\n")))
                    self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("import machine\r\n")))
                    self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("machine.enter")))
                    self.ble_conn.sendline(cmd + array_to_hex_string(bytearray("_ota_dfu()\r\n")))
                    self._dfu_wait_for_notify()
                except:
                    return False
        time.sleep(0.5)

        self.target_mac_increase(1)
        # Reconnect the board.
        ret = self.scan_and_connect()
        if verbose: print "Connected " + str(ret)
        if ret:
            return self.check_DFU_mode()
        return ret


    # --------------------------------------------------------------------------
    #  Parse notification status results
    # --------------------------------------------------------------------------
    def _dfu_parse_notify(self, notify):
        if len(notify) < 3:
            print "notify data length error"
            return None

        if verbose: print notify

        dfu_notify_opcode = Procedures.from_string(notify[0])

        if dfu_notify_opcode == Procedures.RESPONSE:

            dfu_procedure = Procedures.from_string(notify[1])
            dfu_response  = Responses.from_string(notify[2])

            procedure_str = Procedures.to_string(dfu_procedure)
            response_str  = Responses.to_string(dfu_response)

            if verbose: print "opcode: 0x%02x, proc: %s, res: %s" % (dfu_notify_opcode, procedure_str, response_str)
            if dfu_procedure == Procedures.REPORT_RECEIVED_IMAGE_SIZE:
                receipt = bytes_to_uint32_le(notify[3:7])
                return (dfu_procedure, dfu_response, receipt)

            return (dfu_procedure, dfu_response)

        if dfu_notify_opcode == Procedures.PACKET_RECEIPT_NOTIFICATION:
            receipt = bytes_to_uint32_le(notify[1:5])
            return (dfu_notify_opcode, Responses.SUCCESS, receipt)

    # --------------------------------------------------------------------------
    #  Wait for a notification and parse the response
    # --------------------------------------------------------------------------
    def _wait_and_parse_notify(self):
        if verbose: print "Waiting for notification"
        notify = self._dfu_wait_for_notify()

        if notify is None:
            raise Exception("No notification received")

        if verbose: print "Parsing notification"

        result = self._dfu_parse_notify(notify)
        if result[1] != Responses.SUCCESS:
            raise Exception("Error in {} procedure, reason: {}".format(
                Procedures.to_string(result[0]),
                Responses.to_string(result[1])))

        return result

    #--------------------------------------------------------------------------
    # Send the Init info (*.dat file contents) to peripheral device.
    #--------------------------------------------------------------------------
    def _dfu_send_init(self):
        if verbose: print "dfu_send_init"

        # Open the DAT file and create array of its contents
        init_bin_array = array('B', open(self.datfile_path, 'rb').read())

        # Transmit Init info
        self._dfu_send_data(init_bin_array)

import os, re
import sys
import optparse
import time
import math
import traceback

#from unpacker import Unpacker
#from ble_legacy_dfu_controller import BleDfuControllerLegacy
#from ble_desay_dfu_controller import BleDfuControllerDesay

def main():

    try:
        parser = optparse.OptionParser(usage='%prog -f <hex_file> -a <dfu_target_address>\n\nExample:\n\t%prog -f application.hex -d application.dat -a cd:e3:4a:47:1c:e4',
                                       version='0.5')

        parser.add_option('-a', '--address',
                  action='store',
                  dest="address",
                  type="string",
                  default=None,
                  help='DFU target address.'
                  )
        ''' to remove, needs intelhex package and is not that useful
        '''
        parser.add_option('-f', '--file',
                  action='store',
                  dest="hexfile",
                  type="string",
                  default=None,
                  help='hex file to be uploaded.'
                  )

        parser.add_option('-d', '--dat',
                  action='store',
                  dest="datfile",
                  type="string",
                  default=None,
                  help='dat file to be uploaded.'
                  )
        parser.add_option('-z', '--zip',
                  action='store',
                  dest="zipfile",
                  type="string",
                  default=None,
                  help='zip file to be used.'
                  )
        parser.add_option('-t', '--test',
                  action='store_true',
                  dest='test_dfu',
                  help='test bootloader without flashing.'
                  )
        parser.add_option('-v', '--verbose',
                  action='store_true',
                  dest='verbose',
                  help='verbose output.'
                  )

        test_dfu = False
        options, args = parser.parse_args()

        global verbose
        verbose=options.verbose
#        options, args = parser.parse_args()

    except Exception, e:
        print e
        print "For help use --help"
        sys.exit(2)

    try:

        ''' Validate input parameters '''

        if not options.address:
            parser.print_help()
            exit(2)

        unpacker = None
        manfile  = None
        hexfile  = None
        datfile  = None

        if options.zipfile != None:

            if (options.hexfile != None) or (options.datfile != None):
                print "Conflicting input directives"
                exit(2)

            unpacker = Unpacker()
            #print options.zipfile
            try:
                hexfile, datfile, manfile = unpacker.unpack_zipfile(options.zipfile)
            except Exception, e:
                print "ERR"
                print e
                pass

        else:
            if (not options.hexfile) or (not options.datfile):
                parser.print_help()
                exit(2)

            if not os.path.isfile(options.hexfile):
                print "Error: Hex file doesn't exist"
                exit(2)

            if not os.path.isfile(options.datfile):
                print "Error: DAT file doesn't exist"
                exit(2)

            hexfile = options.hexfile
            datfile = options.datfile


        ''' Start of Device Firmware Update processing '''

        ble_dfu = BleDfuControllerLegacy(options.address.upper(), hexfile, datfile, manfile)

        # Initialize inputs
        ble_dfu.input_setup()

        # Connect to peer device. Assume application mode.
        if ble_dfu.scan_and_connect():
            if not ble_dfu.check_DFU_mode():
                print "Trying to switch to DFU mode"
                success = ble_dfu.switch_to_dfu_mode()
                if not success:
                    raise Exception("Couldn't switch")
                else:
                    ble_dfu.start(test=options.test_dfu)
            else:
                ble_dfu.start(test=options.test_dfu)
        else:
            # The device might already be in DFU mode (MAC + 1)
            ble_dfu.target_mac_increase(1)

            # Try connection with new address
            print "Couldn't connect, will try DFU MAC"
            if not ble_dfu.scan_and_connect():
                raise Exception("Can't connect to device")
            if not ble_dfu.check_DFU_mode():
                raise Exception("Not in DFU mode")
            ble_dfu.start(test=options.test_dfu)

        # Disconnect from peer device if not done already and clean up.
        ble_dfu.disconnect()

    except Exception, e:
        # print traceback.format_exc()
        print "Exception at line {}: {}".format(sys.exc_info()[2].tb_lineno, e)
        pass

    except:
        pass

    # If Unpacker for zipfile used then delete Unpacker
    if unpacker != None:
       unpacker.delete()

    print "DFU done"

if __name__ == '__main__':
    # Do not litter the world with broken .pyc files.
    sys.dont_write_bytecode = True
    main()
