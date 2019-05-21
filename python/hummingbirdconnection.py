# This module implements connection of a Hummingbird controller via USB. It is used by
# hummingbird.py to send and receive commands from the Hummingbird.
# The Hummingbird is a robotics kit to promote engineering and arts education, resulting from
# the Arts & Bots research program at Carnegie Mellon's CREATE lab.
# http://www.hummingbirdkit.com

import atexit 
import os
import ctypes
import threading
import time
import platform
import sys

VENDOR_ID = 0x2354
DEVICE_ID = 0x2222

HIDAPI_LIBRARY_PATH = os.environ.get('HIDAPI_LIB_PATH', '/usr/lib/')
PING_FREQUENCY_SECONDS = 2.0 # seconds

# Detect which operating system is present and load corresponding library

hid_api = ctypes.CDLL(os.path.join(HIDAPI_LIBRARY_PATH, "libhidapi32.so"))
    
def _inherit_docstring(cls):
    def doc_setter(method):
        parent = getattr(cls, method.__name__)
        method.__doc__ = parent.__doc__
        return method
    return doc_setter

class HummingbirdConnection:
    """ USB connection to the Hummingbird robot. Uses the HID API
        to read and write from the controller. """

    c_humm_handle = ctypes.c_void_p(None)
    c_io_buffer = ctypes.c_char_p(None)
    cmd_id = 0

    def is_open(self):
        """Returns True if connected to the controller."""
        return bool(self.c_humm_handle)

    def open(self):
        """ Connect to the robot.

        This method looks for a USB port the Hummingbird is connected to. """
        
        _before_new_humm_connection(self)
        if self.is_open():
            self.close()
        try:
            hid_api.hid_open.restype = ctypes.c_void_p
            self.c_humm_handle = hid_api.hid_open(
                ctypes.c_ushort(VENDOR_ID),
                ctypes.c_ushort(DEVICE_ID),
                ctypes.c_void_p(None))
            self.c_io_buffer = ctypes.create_string_buffer(9)
            _new_humm_connected(self)

      	    self.cmd_id = self.read_cmd_id()
        except:
            raise Exception("Failed to connect to the Hummingbird robot.")

    def close(self):
        """ Disconnect the robot. """
        
        if self.c_humm_handle:
            self.send(b'R', [0]) # exit to idle (rest) mode
            hid_api.hid_close.argtypes = [ctypes.c_void_p]
            hid_api.hid_close(self.c_humm_handle)
        self.c_humm_handle = ctypes.c_void_p(None)
        self.c_io_buffer = ctypes.c_char_p(None)
        
        global _open_humms
        if self in _open_humms:
            _open_humms.remove(self)

    def read_cmd_id(self):
        """ Read the controller's internal command counter. """
        
        #self.send('z', receive = True)
        self.send(b'z')
        data = self.receive()
        return data[0]

    def send(self, command, payload=()):
        """Send a command to the controller (internal).

        command: The command ASCII character
        payload: a list of up to 6 bytes of additional command info
        """
        
        if not self.is_open():
            raise Exception("Connection to Hummingbird was closed.")
        
        # Format the buffer to contain the contents of the payload.
        for i in range(7):
            self.c_io_buffer[i] = b'\x00'
        self.c_io_buffer[1] = command[0]

        python_version = sys.version_info[0]

        if payload:
            for i in range(len(payload)):
                if python_version >= 3:
                    self.c_io_buffer[i+2] = payload[i]
                else:
                    self.c_io_buffer[i+2] = bytes(chr(payload[i]))
        # Make sure command id is incremented if this is a receive case
        if command == b's' or command == b'G':
            self.cmd_id = (self.cmd_id + 1) % 256
                
        if python_version >= 3:
            self.c_io_buffer[8] = self.cmd_id
        else:
            self.c_io_buffer[8] = bytes(chr(self.cmd_id))
        
        # Write to the Hummingbird bufffer
        res = 0
        while not res:
            hid_api.hid_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            res = hid_api.hid_write(self.c_humm_handle,
                                    self.c_io_buffer,
                                    ctypes.c_size_t(9))
       
    def receive(self):
        """ Read the data from the Hummingbird buffer. """
        
        res = 9
        while res > 0:
            hid_api.hid_read.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
	    res = hid_api.hid_read_timeout(self.c_humm_handle,
                                    self.c_io_buffer,
                                    ctypes.c_size_t(9),
				    50)
	    if self.cmd_id == ord(self.c_io_buffer[8]):
                break
            else:
                print("mismatch ")
                print(self.cmd_id)
                print(" ")
                print(ord(self.c_io_buffer[8]))
	return [ord(self.c_io_buffer[i]) for i in range(9)]
    
class ThreadedHummConnection(HummingbirdConnection):
    """Threaded implementation of Hummingbird Connection"""
    
    lock = None
    thread = None
    main_thread = None
    last_cmd_sent = time.time()

    @_inherit_docstring(HummingbirdConnection)
    def open(self):
        HummingbirdConnection.open(self)
        if not self.is_open():
            return
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.__class__._pinger, args=(self, ))
        self.main_thread = threading.current_thread()
        self.thread.start()

    @_inherit_docstring(HummingbirdConnection)
    def send(self, command, payload=(), receive=False):
        try:
            if self.lock is not None:
                self.lock.acquire()
            HummingbirdConnection.send(self, command, payload=payload)
            self.last_cmd_sent = time.time();
        finally:
            if self.lock is not None:
                self.lock.release()

    @_inherit_docstring(HummingbirdConnection)
    def receive(self):
        try:
            if self.lock is not None:
                self.lock.acquire()
            data = HummingbirdConnection.receive(self)
        finally:
            if self.lock is not None:
                self.lock.release()
        return data
    
    def _pinger(self):
        """ Sends keep-alive commands every few secconds of inactivity. """

        while True:
            if not self.lock:
                break
            if not self.c_humm_handle:
                break
            if not self.main_thread.isAlive():
                break
            try:
                self.lock.acquire()
                now = time.time()
                if self.last_cmd_sent:
                    delta = now - self.last_cmd_sent
                else:
                    delta = PING_FREQUENCY_SECONDS
                if delta >= PING_FREQUENCY_SECONDS:
                    HummingbirdConnection.send(self, b'z')
                    HummingbirdConnection.receive(self)
                    self.last_cmd_sent = now
            finally:
                self.lock.release()
            time.sleep(0.1)

    @_inherit_docstring(HummingbirdConnection)
    def close(self):
        HummingbirdConnection.close(self)
        self.thread.join()
        self.lock = None
        self.thread = None

# Functions that handle the list of open hummingbirds

_open_humms = []

def _before_new_humm_connection(humm):
    global _open_humms
    # close other connections
    for robot in _open_humms:
        if robot.is_open():
            robot.close()


def _new_humm_connected(humm):
    global _open_humms
    if humm not in _open_humms:
        _open_humms.append(humm)


def _close_all_humms():
    global _open_humms
    if not _open_humms:
        return
    for humm in _open_humms:
        if humm.is_open():
            humm.close()

atexit.register(_close_all_humms)



    
