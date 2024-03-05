import struct
import binascii


def parse_be_uint8(buffer):
    return struct.unpack(">B", bytes(buffer))[0]


def parse_be_uint32(buffer):
    return struct.unpack(">I", bytes(buffer))[0]


def parse_be_bytes(buffer):
    return binascii.b2a_hex(bytes(buffer))


def to_be_uint32(val):
    return binascii.b2a_hex(struct.pack(">I", val))


def to_be_uint8(val):
    return binascii.b2a_hex(struct.pack(">B", val))


def to_be_bytes(hex_str):
    return binascii.a2b_hex(hex_str)
