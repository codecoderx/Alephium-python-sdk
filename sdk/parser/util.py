import struct
import binascii


def parse_be_uint8(buffer):
    return struct.unpack(">B", bytes(buffer))[0]


def parse_be_uint32(buffer):
    return struct.unpack(">I", bytes(buffer))[0]


def parse_be_bytes(buffer):
    return binascii.b2a_hex(bytes(buffer))
