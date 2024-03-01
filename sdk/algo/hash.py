import binascii

from sdk import util
from blake3 import blake3
import math

GROUP_SIZE = 4


def pow_hash(nonce, headerBlob):
    nonce_bytes = util.to_be_bytes(nonce)
    headerBlob_bytes = util.to_be_bytes(headerBlob)

    header = nonce_bytes + headerBlob_bytes
    return blake3(blake3(header).digest()).digest()


def get_block_chain_index(pow_hash):
    pow_hash_bytes = util.to_be_bytes(pow_hash)
    before_last = pow_hash_bytes[len(pow_hash_bytes) - 2] & 0xff
    last = pow_hash_bytes[len(pow_hash_bytes) - 1] & 0xff
    big_index = before_last << 8 | last
    chain_num = GROUP_SIZE * GROUP_SIZE
    index = big_index % chain_num
    fromGroup = math.floor(index / GROUP_SIZE)
    toGroup = index % GROUP_SIZE
    return fromGroup, toGroup
