import ctypes
import struct


def mem(address, size):
    f = ctypes.pythonapi.PyMemoryView_FromMemory
    f.argtypes, f.restype = [ctypes.c_ssize_t, ctypes.c_ssize_t, ctypes.c_int], ctypes.py_object
    return f(address, size, 0x200)


def unpack(address, fmt):
    return struct.unpack(fmt, mem(address, struct.calcsize(fmt)))


def py(address):
    f = ctypes.pythonapi.Py_NewRef
    f.argtypes, f.restype = [ctypes.c_ssize_t], ctypes.py_object
    return f(address)
